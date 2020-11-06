import asyncio
import json
import spacy
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy import displacy

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class processText():
    def __init__(self, text: str):
        self.text = text
        self.nlp = spacy.load("en_core_web_md")
        self.doc = self.nlp(text)

    async def process(self):
        fmt_ents, tf_idf = await asyncio.gather(
            self.get_formatted_entities(self.doc),
            self.get_tfidf(self.doc)
        )
        return json.dumps({
            "ents": fmt_ents,
            "tf_idf": tf_idf
            })

    async def get_formatted_entities(self, doc: spacy.tokens.Doc):
        return displacy.render(doc, style="ent")

    async def get_tfidf(self, doc: spacy.tokens.Doc):
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 1), max_features=20,
            stop_words=self.nlp.Defaults.stop_words)
        vectorizer.fit_transform([span.text for span in doc.sents])
        tf_idf = dict(
            feature for feature in zip(vectorizer.get_feature_names(), vectorizer.idf_)
            if not feature[0].isnumeric()
        )
        return tf_idf


if __name__ == "__main__":
    proc = processText(sys.argv[1])
    print(asyncio.run(proc.process()))
