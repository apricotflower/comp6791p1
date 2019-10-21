import nltk
import string
import PARAMETER
import MyParser

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
    global tokens_num
    for (key, value) in all_document.items():
        #处理标点
        value = value.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
        tokens = nltk.word_tokenize(value)

        # translator = str.maketrans(dict.fromkeys(string.punctuation))
        # tokens = nltk.word_tokenize(str(value.translate(translator)))

        all_document[key] = tokens
        # print(len(tokens))
        tokens_num = tokens_num + len(tokens)
        # print("Tokenizing " + key)
        # print(all_dict[key])

