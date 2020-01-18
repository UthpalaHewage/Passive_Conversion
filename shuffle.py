# Import spaCy and load the language library
import spacy
from nltk import tokenize
from random import shuffle

import Model.paragraph as para

# load small version of english library
# python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


class Shuffle(object):

    def __init__(self):
        pass

    def shuffle(self):
        # with open('files/tense conversion_2.txt', 'r') as file:
        with open('test.txt', 'r') as file:
            print("check1")
            # read the text file_transcript
            data = file.read()
            # tokenize the sent and replace the uneven line breaks
        all_sent_list = tokenize.sent_tokenize(data.replace("\n", " "))
        print("check2")
        # used to rewrite a file after shuffling for evaluation
        shuffle(all_sent_list)
        print("check3")
        with open('new_list.txt', 'w') as f:
            for item in all_sent_list:
                f.write("%s\n" % item)
            print("check4")
        self.print_para()

    @staticmethod
    def print_para():
        print(para.final_para)
        para.final_para = ""
