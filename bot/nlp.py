import re 

import en_core_web_sm
nlp = en_core_web_sm.load()

import bot.duckduckgo

def parse_dep(text, merge=True):
    doc = nlp(text)
    if merge:
        for np in list(doc.noun_chunks):
            np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)
    return [(w.text, w.tag_) for w in doc]

def lemmatize(text):
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc]
    return tokens

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents] 
    return entities

# words to match
DDG_QUESTION_LEAD = ["what", "who", "when", "where"]

# patterns
A_THE = re.compile("(a|the) ")
POSSESSIVE_S = re.compile("'s\b")

def parse_chat(text):
    # remember to split into sentences first
    # tags = parse_dep(" ".join(lemmatize(text)))
    # print(tags)
    tags = parse_dep(text)
    ddg_flag = False
    ddg_position = []

    # TODO really you just want to do something like kmp on a list
    for idx, tag in enumerate(tags):
        if tag[1] == "WP" or tag[1] == "WRB":
            if tag[0].lower() in DDG_QUESTION_LEAD:
                if (idx + 1) < len(tags) and lemmatize(tags[idx + 1][0])[0] == "be":
                    ddg_flag = True
                    ddg_position.append(idx)

    ret = []
    if ddg_flag:
        # needs to parse this
        # wiki this 
        search_term = tags[ddg_position[0] + 2][0]
        search_term = re.sub(A_THE, "", search_term)
        # needs to retry if no results are found, eg. "The Chinese High School Singapore" will fail with this setting
        result = bot.duckduckgo.search(search_term)
        ret.append(result) # TODO check for no result
    
    if len(ret) > 0:
        return "\n".join(ret)
    else:
        return "Sorry I don't understand your query. Type /help for more commands"
