import nltk
import string
import PARAMETER
import MyParser
import re


all_document = dict()
tokens_num = 0


def break_clean(file_number):
    filename = PARAMETER.PATH + file_number
    f = open(filename, 'r', encoding='unicode_escape')
    parser = MyParser.MyParser()
    parser.feed(f.read())
    all_document.update(parser.one_dict)
    parser.close()


def allfiles_break_clean():
    for num in range(0, 22):#0-22
        print(str(num).zfill(2))
        break_clean(str(num).zfill(2) + ".sgm")


def tokenize():
    """ Tokenize the content. """
    global tokens_num
    for (key, value) in all_document.items():
        # # Deal with punctuation
        # value = value.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
        value =  re.sub(r'\W+', ' ', value)
        tokens = nltk.word_tokenize(value)
        # tokens = [re.sub(r'[\W\s]', '', token) for token in tokens]
        # empty_spaces = []
        # for token in tokens:
        #     if token == "":
        #         empty_spaces.append(token)
        # for e in empty_spaces:
        #     tokens.remove(e)

        all_document[key] = tokens
        tokens_num = tokens_num + len(tokens)



