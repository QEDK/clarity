import spacy
from spacy import displacy
import sys


def get_formatted_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return displacy.render(doc, style="ent")


if __name__ == "__main__":
    print(get_formatted_entities(sys.argv[1]))
