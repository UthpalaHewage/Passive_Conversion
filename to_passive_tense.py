import spacy
import inflect
from pyinflect import getInflection

inflect = inflect.engine()
# from nltk import tokenize
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher(nlp.vocab)

with open('question.txt', 'r') as file:
    data = file.readlines()

word_list = ["I", "She", "He", "We", "You"]
aux_pattern_list = ["do not", "does not"]

# terms = ["det dative compound dobj","det dative compound obj","det amod dobj", "det compound dobj", "predet det dobj", "nummod quantmod dobj","det amod obj", "det compound obj", "predet det obj", "nummod quantmod obj","nummod dobj", "det dobj", "poss dobj", "amod dobj", "nummod obj", "det obj", "poss obj", "amod obj","dobj", "obj"]


# need to declare different patterns for objects
phrase_list = []
# get use of obj_patterns_for identification of patterns of  object occurrences
with open('obj_patterns', 'r') as file:
    phrase_list = ["" + line.strip() + "" for line in file]

object_patterns = [nlp(text) for text in phrase_list]
matcher.add('Object_Matcher', None, *object_patterns)

aux_patterns = [nlp(text) for text in aux_pattern_list]
matcher.add('Aux_Matcher', None, *aux_patterns)


def get_object_bound(sentence):
    new_sentence = ""
    for token in sentence:
        new_sentence = new_sentence + token.dep_ + " "
    new_sentence = nlp(new_sentence)
    matches = matcher(new_sentence)

    if len(matches) != 0:
        for match in matches:
            if nlp.vocab.strings[match[0]] == "Object_Matcher":
                return [match[1], match[2]]
    return 0


def create_passive(doc, sub_idx, root_idx, obj_index, obj_start, obj_end, negation_availability):
    # if str(doc[obj_start:obj_end]

    if len(doc) > obj_end + 2:
        if negation_availability:
            if inflect.singular_noun(str(doc[obj_index])) is False:
                # sentence[root_verb].lemma_
                print(str(doc[obj_start:obj_end]) + " is not " + str(
                    getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:]))
            else:
                print(str(doc[obj_start:obj_end]) + " are not " + str(
                    getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:]))
        else:
            if inflect.singular_noun(str(doc[obj_index])) is False:
                print(str(doc[obj_start:obj_end]) + " is " + str(
                    getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:]))
            else:
                print(str(doc[obj_start:obj_end]) + " are " + str(
                    getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:]))
        # print(negation_availability)
    else:
        if negation_availability:
            if inflect.singular_noun(str(doc[obj_index])) is False:
                print(str(doc[obj_start:obj_end]) + " is not " + str(
                    getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + ".")
            else:
                print(str(doc[obj_start:obj_end]) + " are not" + str(getInflection(doc[root_idx].lemma_, tag='VBN')[0])+".")
        else:
            if inflect.singular_noun(str(doc[obj_index])) is False:
                print(str(doc[obj_start:obj_end]) + " is " + str(getInflection(doc[root_idx].lemma_, tag='VBN')[0])+".")
            else:
                print(str(doc[obj_start:obj_end]) + " are " + str(getInflection(doc[root_idx].lemma_, tag='VBN')[0])+".")
        # print(negation_availability)
    print(" ")


subject_idx = None
root_idx = None
object_start_idx = None
object_end_idx = None


def check_negation(sentence):
    matches = matcher(nlp(sentence))
    if len(matches) != 0:
        for match in matches:
            if nlp.vocab.strings[match[0]] == "Aux_Matcher":
                return True
    return False


for i in data:

    doc = nlp(i)

    # check for the dep_=ROOT and pos_=VERB combination to get as the base root of the sentence
    root_verb_index = [idx for idx in range(len(doc)) if
                       str(doc[idx].dep_) == "ROOT" and str(doc[idx].pos_) == "VERB"]

    # ----another else statement should be developed to make personal_pronouns of sent without a verb into 'it'
    if len(root_verb_index) != 0:
        root_idx = root_verb_index[0]

        # print(doc[root_verb_index[0]])
        sub_index = [idx for idx in range(len(doc)) if
                     (str(doc[idx].dep_) == "nsubj" or
                      str(doc[idx].dep_) == "nsubjpass")
                     and (idx < root_idx and str(doc[idx]) in word_list)]

        if len(sub_index) != 0:
            subject_idx = sub_index[0]

            # check for the availability of obj-object/dobject-direct object/pobj-object
            # preposition and availability of NOUN/PROPN
            obj_index = [idx for idx in range(len(doc)) if
                         (str(doc[idx].dep_) == "obj" or
                          str(doc[idx].dep_) == "dobj")
                         and idx > root_idx and (
                                 str(doc[idx].pos_) == "NOUN" or str(doc[idx].pos_) == "PROPN")]
            if len(obj_index) != 0:
                result = get_object_bound(doc)

                if result != 0:
                    object_start_idx = result[0]
                    object_end_idx = result[1]
                    negation_availability = check_negation(str(doc[:root_idx]))
                    create_passive(doc, int(subject_idx), int(root_idx), int(obj_index[0]),
                                   int(object_start_idx), int(object_end_idx),
                                   negation_availability)
        else:
            # -- this is allocated for the replacement of personalpronouns with 'it'
            pass

            # for sent in doc.sents:
            #     print(sent)
