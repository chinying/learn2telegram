import re 

import spacy
nlp = spacy.load('en')

def parseText(s):
    return

def extract_entity(s):
    doc = nlp(s)
    entities = []
    for ent in doc.ents:
        print(ent.label_, ent.text)
        entities.append(ent.text)
    return entities