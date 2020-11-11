#!/usr/bin/env python3
import preprocessor as p
import numpy as np
import pandas as pd
import emoji
import spacy
import tensorflow as tf
from keras.layers import Bidirectional, Dropout, SpatialDropout1D
from keras.layers.core import Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence, text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# In comparison, the model takes 2 seconds per epoch  to train on a Google TPU v3-8
# It increases to minutes on a GPU and and even more duration on a CPU.
tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(tpu)
tf.tpu.experimental.initialize_tpu_system(tpu)

# Instantiate a distribution strategy:
tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu)
print("All devices: ", tf.config.list_logical_devices("TPU"))

# This is the primary dataset:
data = pd.read_csv("/kaggle/input/figure-eight-labelled-textual-dataset/text_emotion.csv")

# spaCy provides a large set of useful stopwords we can use to clean up prediction text as well:
sp = spacy.load("en_core_web_sm")
spacy_stopwords = sp.Defaults.stop_words

# We are using only the GNU spellchecker data from the dataset, more is available:
misspell_data = pd.read_csv(
    "/kaggle/input/spelling/aspell.txt", sep=":", names=["correction", "misspell"]
)
misspell_data.misspell = misspell_data.misspell.str.strip()
misspell_data.misspell = misspell_data.misspell.str.split()
misspell_data = misspell_data.explode("misspell").reset_index(drop=True)
misspell_data.drop_duplicates("misspell", inplace=True)
corrections = dict(zip(misspell_data.misspell, misspell_data.correction))

contractions = pd.read_csv("/kaggle/input/contractions/contractions.csv")
cont_dict = dict(zip(contractions.Contraction, contractions.Meaning))


def spelling_correction(val):
    for x in val.split():
        if x in corrections.keys():
            val = val.replace(x, corrections[x])
    return val


def expand_contractions(val):
    for x in val.split():
        if x in cont_dict.keys():
            val = val.replace(x, cont_dict[x])
    return val


def unpunctuate(val):
    punctuations = '''()-[]{};:'"\\,<>./@#$%^&_~'''
    for x in val:
        if x in punctuations:
            val = val.replace(x, " ")
    return val


def remove_stopwords(val):
    return " ".join([word for word in val.split() if word not in spacy_stopwords])


p.set_options(p.OPT.MENTION, p.OPT.URL)


def clean_text(val):
    val = spelling_correction(val)
    val = expand_contractions(val)
    val = p.clean(val)
    val = unpunctuate(emoji.demojize(val))
    val = remove_stopwords(val)
    return val


# Apply function as a map across the column:
data["clean_content"] = data.content.apply(clean_text)

# Delete empty cells from dataset:
data = data[data.clean_content != ""]

sent_to_id = {
    "empty": 0,
    "sadness": 1,
    "enthusiasm": 2,
    "neutral": 3,
    "worry": 4,
    "surprise": 5,
    "love": 6,
    "fun": 7,
    "hate": 8,
    "happiness": 9,
    "boredom": 10,
    "relief": 11,
    "anger": 12
}

data["sentiment_id"] = data["sentiment"].map(sent_to_id)

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(data.sentiment_id)
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
Y = onehot_encoder.fit_transform(integer_encoded)

X_train, X_test, y_train, y_test = train_test_split(
    data.clean_content, Y, random_state=42, test_size=0.2, shuffle=True
)

# Tokenize using Keras' tokenizer
tokenizer = text.Tokenizer(num_words=None)
# Modify this according to your dataset:
max_len = 160
tokenizer.fit_on_texts(list(X_train) + list(X_test))
# This saves our Keras vocab into a vocab.txt file for use in later encoding
np.savetxt("/kaggle/working/vocab.txt", np.array(list(X_train) + list(X_test)), fmt="%s")
# Pad sequences < 160 characters
X_train_pad = sequence.pad_sequences(tokenizer.texts_to_sequences(X_train), maxlen=max_len)
X_test_pad = sequence.pad_sequences(tokenizer.texts_to_sequences(X_test), maxlen=max_len)

word_idx = tokenizer.word_index


def get_sentiment(model, text):
    text = clean_text(text)
    seq = tokenizer.texts_to_sequences([text])
    seq = sequence.pad_sequences(seq, maxlen=max_len, dtype="int32")
    sentiment = model.predict(seq, batch_size=1, verbose=2)
    sentiment = np.round(np.dot(sentiment, 100).tolist(), 0)[0]  # convert to percentage
    return sentiment


def parse_vectors(file_name):
    with open(file_name, "r") as f:
        word_vocab = set()
        word2vector = {}
        for line in f:
            line_ = line.strip()
            words_Vec = line_.split()
            word_vocab.add(words_Vec[0])
            word2vector[words_Vec[0]] = np.array(words_Vec[1:], dtype=float)
    print("Total words in dataset:", len(word_vocab))
    return word_vocab, word2vector


# GloVe dataset: 6B vectors with 300 dimensions, 400K unique words
# Larger datasets with more vectors/dims will give better results
vocab, word_to_idx = parse_vectors("/kaggle/input/glove6b300dtxt/glove.6B.300d.txt")

# Set this according to the number of dims of the vectors:
embed_dim = 300

embedding_matrix = np.zeros((len(word_idx) + 1, embed_dim))
for word, i in word_idx.items():
    embedding_vector = word_to_idx.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# Compile the model in TPU for faster training, comment this to compile with GPU/CPU:
with tpu_strategy.scope():
    model = Sequential()
    model.add(Embedding(
        len(word_idx) + 1, embed_dim,
        input_length=X_test_pad.shape[1],
        weights=[embedding_matrix],
        trainable=False)
    )
    model.add(SpatialDropout1D(0.1))
    model.add(Bidirectional(LSTM(600, dropout=0.5, recurrent_dropout=0.5)))
    model.add(Dense(300, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(13, activation="softmax"))
    model.compile(
        loss="categorical_crossentropy",
        optimizer=tf.keras.optimizers.Nadam(
            learning_rate=0.00009, beta_1=0.9, beta_2=0.999, epsilon=1e-09
        ),
        metrics=["accuracy"]
    )
print(model.summary())

# If training on a GPU/CPU, you might want to use smaller batches:
model.fit(
    X_train_pad, y_train, epochs=100,
    batch_size=4096,
    validation_data=(X_test_pad, y_test)
)

# Save the model to disk
model.save("/kaggle/working/model.h5")
