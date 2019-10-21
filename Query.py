import os
import PARAMETER
import ast
from collections import OrderedDict


def or_query(query_list):
    return


def and_query(query_list):
    return


def deal_with_query(query):
    query_list = []
    operator = ""
    return query_list, operator

def load_dict():
    print("Loading best index into memory……")
    # dict_test = open("dict.txt","a+")
    search_index = PARAMETER.STOP_WORDS_150_MERGE_BLOCK_PATH
    global search_dict
    search_dict = OrderedDict()
    for file in os.listdir(search_index):
        # print(file)
        fo = open(search_index + file)
        line = fo.readline()
        while line:
            term, posting = line.rsplit(":", 1)
            search_dict[term] = ast.literal_eval(posting)
            # print(term)
            # dict_test.write(term+"\n")
            line = fo.readline()
    # print(search_dict)
    print("Finish loading ! ")

    start_query()


def start_query():
    print("Please input query: ")
    query = input().lower()
    while query.lower() != PARAMETER.EXIT:
        query_list, operator = deal_with_query(query)
        if operator == PARAMETER.QUERY_AND:
            and_query(query_list)
            query = input().lower()
        elif operator == PARAMETER.QUERY_OR:
            or_query(query_list)
            query = input().lower()
        else:
            print("Operator wrong! Input again!")
            query = input().lower()


load_dict()