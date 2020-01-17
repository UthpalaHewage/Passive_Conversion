import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u"after although as because before even since than that though till unless untill when whenever where wherever while ")
for i in range(len(doc)):
    print(f'{i:{10}} {doc[i].text:{10}} {doc[i].pos_:{8}} {doc[i].tag_:{6}} {doc[i].dep_:{10}} {spacy.explain(doc[i].tag_)}')


