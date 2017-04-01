from nltk.corpus import wordnet as wn  

def hyponym_paths(c):

    paths = []
    hyponyms = c.hyponyms()
    for hyponym in hyponyms:
        paths.append(hyponym)
        for descendants in hyponym_paths(hyponym):
            paths.append(descendants)
    return (paths)

def leaf_nodes(c):
    ln=[]
    for j in hyponym_paths(c):
        if len(j.hyponyms())==0:
            ln.append(j)
    return ln
