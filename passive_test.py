import spacy

nlp = spacy.load('en_core_web_sm')
# doc = nlp("They make cars in Detroit")
# doc = nlp("In this lecture, we will cover problems with pronouns.")
doc = nlp("I works in the hospital.")
# doc = nlp("I go to hit the sack.")
# doc = nlp("I postpone my interview in to the subsequent week-postponed.")

s = list(doc)
tmp, temp, sub = "", "", -1
for i in doc:
    if i.pos_ == 'VERB':
        s[i.i] = i
    elif i.dep_ == 'nsubj':
        sub = i.i
        temp = i
    elif i.dep_ == 'dobj':
        tmp = i.text.capitalize()
        s[i.i] = temp
        s.insert(i.i, "by")

s[sub] = tmp
print(' '.join(str(e) for e in s))
