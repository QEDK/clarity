#!/usr/bin/env python3
import asyncio
import json
import keras.preprocessing
import numpy as np
import re
import spacy
import sys
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy import displacy
from spacy.matcher import Matcher
from textblob import TextBlob

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class ProcessText():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.model = tf.keras.models.load_model("model.h5")
        self.uncontracter = RegexpReplacer()
        self.unpunctuator = re.compile(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]")
        self.tokenizer = keras.preprocessing.text.Tokenizer(num_words=None)
        self.tokenizer.fit_on_texts(list(np.genfromtxt("vocab.txt", dtype="str", delimiter="\n")))
        self.sentiments = [
            "empty",
            "sadness",
            "enthusiasm",
            "neutral",
            "worry",
            "surprise",
            "love",
            "fun",
            "hate",
            "happiness",
            "boredom",
            "relief",
            "anger"
        ]

    async def process(self, text: str):
        self.doc = self.nlp(text)
        self.blob = TextBlob(text)
        sentiment, fmt_ents, (tf_idf, word_associations) = await asyncio.gather(
            self.get_sentiment(self.doc, self.blob),
            self.get_formatted_entities(self.doc),
            self.get_word_associations(self.doc)
        )
        return json.dumps({
            "ents": fmt_ents,
            "tf_idf": tf_idf,
            "word_associations": word_associations,
            "sentiment": sentiment
            })

    async def get_formatted_entities(self, doc: spacy.tokens.Doc):
        return displacy.render(doc, style="ent")

    async def get_word_associations(self, doc: spacy.tokens.Doc):
        async def get_tfidf():
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1), max_features=10,
                stop_words=self.nlp.Defaults.stop_words)
            vectorizer.fit_transform([span.text for span in doc.sents])
            tf_idf = dict(
                feature for feature in zip(vectorizer.get_feature_names(), vectorizer.idf_)
                if not feature[0].isnumeric()
            )
            return tf_idf
        tf_idf = await get_tfidf()
        matcher = Matcher(self.nlp.vocab)
        for token in tf_idf.keys():  # transform tokens to similarity matrix
            matcher.add(token, None, [{"LOWER": token}])
        spanlist = [doc[match[1]:match[2]] for match in matcher(doc)]
        word_associations = {}
        for span in spanlist[:-1]:
            word_associations[span.text] = [
                {otherspan.text: str(span.similarity(otherspan))} for otherspan in spanlist
                if otherspan.text != span.text and otherspan.text not in word_associations
            ]
        return (tf_idf, word_associations)

    async def get_sentiment(self, doc: spacy.tokens.Doc, blob: TextBlob):
        async def sanitize(text: str):
            text = text.lower()  # lowercase string
            text = str(blob.correct())  # spellcheck
            text = await self.uncontracter.replace(text)  # replace contractions with regex
            text = self.unpunctuator.sub("", text)
            text = " ".join(
                [word for word in text.split() if word not in self.nlp.Defaults.stop_words]
            )  # remove stopwords
            return text

        async def predict_sentence_mood(text: str):
            seq = self.tokenizer.texts_to_sequences([text])
            seq = keras.preprocessing.sequence.pad_sequences(seq, maxlen=160, dtype="int32")
            sentiment = self.model.predict(seq, batch_size=1, verbose=2)
            sentiment = np.round(np.dot(sentiment, 100).tolist(), 0)[0]  # convert to percentage
            return sentiment

        mood = dict(
            zip(
                self.sentiments,
                ((sum(val)/len(list(doc.sents))) for val in zip(
                    *[await predict_sentence_mood(await sanitize(span.text))
                        for span in doc.sents]))
            )
        )
        return {
            "mood": mood,  # 12 emotions + 1 empty
            "polarity": self.blob.sentiment.polarity,  # [-1, +1]
            "subjectivity": self.blob.sentiment.subjectivity  # [0, 1]
        }


class RegexpReplacer():
    replacement_patterns = [
        (r'won\'t', 'will not'),
        (r'can\'t', 'cannot'),
        (r'i\'m', 'i am'),
        (r'ain\'t', 'is not'),
        (r'(\w+)\'ll', r'\g<1> will'),
        (r'(\w+)n\'t', r'\g<1> not'),
        (r'(\w+)\'ve', r'\g<1> have'),
        (r'(\w+)\'s', r'\g<1> is'),
        (r'(\w+)\'re', r'\g<1> are'),
        (r'(\w+)\'d', r'\g<1> would')
    ]

    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    async def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s


if __name__ == "__main__":
    proc = ProcessText()
    import time
    start = time.perf_counter()
    print(asyncio.run(proc.process(sys.argv[1])))
    end = time.perf_counter()
    print(f"Time elapsed: {end - start}")
