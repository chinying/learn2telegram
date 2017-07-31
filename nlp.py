import re 

import en_core_web_sm
nlp = en_core_web_sm.load()

def parseText(s):
    return

def extract_entity(s):
    doc = nlp(s)
    entities = []
    for ent in doc.ents:
        print(ent.label_, ent.text)
        entities.append(ent.text)
    return entities

def extract_tags(s):
    doc = nlp(s)
    for word in doc:
        print(word.tag, word.tag_, word.pos, word.pos_)