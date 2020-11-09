import asyncio
import json
import spacy
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy import displacy
from spacy.matcher import Matcher

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class processText():
    def __init__(self, text: str):
        self.text = text
        self.nlp = spacy.load("en_core_web_md")
        self.doc = self.nlp(text)

    async def process(self):
        fmt_ents, (tf_idf, word_associations) = await asyncio.gather(
            self.get_formatted_entities(self.doc),
            self.get_word_associations(self.doc)
        )
        return json.dumps({
            "ents": fmt_ents,
            "tf_idf": tf_idf,
            "word_associations": word_associations
            })

    async def get_formatted_entities(self, doc: spacy.tokens.Doc):
        return displacy.render(doc, style="ent")

    async def get_tfidf(self, doc: spacy.tokens.Doc):
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 1), max_features=10,
            stop_words=self.nlp.Defaults.stop_words)
        vectorizer.fit_transform([span.text for span in doc.sents])
        tf_idf = dict(
            feature for feature in zip(vectorizer.get_feature_names(), vectorizer.idf_)
            if not feature[0].isnumeric()
        )
        return tf_idf

    async def get_word_associations(self, doc: spacy.tokens.Doc):
        tf_idf = await self.get_tfidf(doc)
        matcher = Matcher(self.nlp.vocab)
        for token in tf_idf.keys():  # transform tokens to similarity matrix
            matcher.add(token, None, [{"LOWER": token}])
        spanlist = [doc[match[1]:match[2]] for match in matcher(doc)]
        word_associations = {}
        for span in spanlist:
            word_associations[span.text] = [
                {otherspan.text: str(span.similarity(otherspan))} for otherspan in spanlist
                if otherspan.text != span.text
            ]
        return (tf_idf, word_associations)


if __name__ == "__main__":
    proc = processText(sys.argv[1])
    print(asyncio.run(proc.process()))
