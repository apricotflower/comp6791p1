import os
import PARAMETER
import ast
from collections import OrderedDict
import itertools
import re
import Deal_File
import math
import json
import copy

search_dict = dict()


def check_and_query(query_list, result):
    """  Check the result from and query. If the result is empty, query the combinations of the terms. """
    if len(result) == 0:
        print("No result for this AND query: " + str(query_list) + ", start printing results of smaller size terms in this query ……")
        print("**" * 20)
        i = 1
        shorter_lists = list(itertools.combinations(query_list, len(query_list) - i))
        # print(shorter_lists)
        while len(shorter_lists[0]) > 0:
            results = []
            for shorter_list in shorter_lists:
                shorter_list = list(shorter_list)
                result = multiple_query(shorter_list, PARAMETER.QUERY_AND)
                results.append(result)
                if len(result) != 0:
                    print("Keyword: " + str(shorter_list))
                    for (i1,v) in enumerate(result):
                        result[i1] = v[0]
                    print(str(len(result)) + " documents was found." + "Result: " + str(result))
                    print("**"*10)
            i = i + 1
            shorter_lists = list(itertools.combinations(query_list, len(query_list) - i))
            # print(shorter_lists)


def doc_id_sorted(query_list, result):
    """  In or query, sort the document according to the number of keywords. """
    id_dict = {}
    for id in result:
        for term in query_list:
            for list in search_dict[term]:
                if list[0] == id :
                    if id not in id_dict:
                        id_dict[id] = 1
                    else:
                        id_dict[id] = id_dict[id] + 1
    sorted_id = sorted(id_dict.items(), key= lambda x:x[1],reverse=True)
    print("Order: " + str(sorted_id))


def or_query_each(p1, p2):
    """  or operation of two terms """
    answer = []
    p1_pointer = 0
    p2_pointer = 0

    while len(p1) > p1_pointer and len(p2) > p2_pointer:
        if p1[p1_pointer][0] == p2[p2_pointer][0]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
            p2_pointer = p2_pointer + 1
        elif p1[p1_pointer][0] < p2[p2_pointer][0]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
        else:
            answer.append(p2[p2_pointer])
            p2_pointer = p2_pointer + 1
    if p1_pointer == len(p1):
        answer = answer + p2[p2_pointer:]
    elif p2_pointer == len(p2):
        answer = answer + p1[p1_pointer:]
    # for (i,v) in enumerate(answer):
    #     answer[i] = v[0]
    return answer


def and_query_each(p1, p2):
    """ and operation of two terms """
    answer = []
    p1_pointer = 0
    p2_pointer = 0
    while len(p1) > p1_pointer and len(p2) > p2_pointer:
        if p1[p1_pointer][0] == p2[p2_pointer][0]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
            p2_pointer = p2_pointer + 1
        elif  p1[p1_pointer][0] < p2[p2_pointer][0]:
            p1_pointer = p1_pointer + 1
        else:
            p2_pointer = p2_pointer + 1
    return answer


def check_exist(query_list):
    """ Check if every terms is existed in the dictionary. """
    exist_list = []
    every_term_exist = True
    for term in query_list:
        posting = search_dict.get(term, None)
        if posting is None:
            print("[ " + str(term) + " ] does not exist in the dictionary! ")
            every_term_exist = False
        else:
            exist_list.append(term)

    if not exist_list:
        print(str(len(exist_list)) + " result exist! input again ……")
        return start_query()
    if not every_term_exist:
        print("Only found " + str(exist_list) + " in the dictionary. \n" + "Start querying result with these " + str(len(exist_list)) + " terms ……" )
        print("**"*30)
        print("Keyword: " + str(exist_list))
    return exist_list


def multiple_query(query_list, operator):
    query_list.sort(key=lambda x: len(search_dict[x]))
    result = search_dict[query_list[0]]
    rest_list = query_list[1:]
    while len(result) != 0 and len(rest_list) != 0:
        if operator == PARAMETER.QUERY_AND:
            result = and_query_each(result, search_dict[rest_list[0]])
        elif operator == PARAMETER.QUERY_OR:
            result = or_query_each(result, search_dict[rest_list[0]])
        rest_list = rest_list[1:]
    return result


def compute_RSVd(document, query_list,k1,b):
    l_d = int(tokens_number[document])
    temp = 0
    for t in query_list:
        tftd = 0
        for newid_pair in search_dict[t]:
            # print(newid_pair[0])
            # print(document)
            if str(newid_pair[0]) == str(document):
                # print("in")
                tftd = newid_pair[1]
        dft = len(search_dict[t])

        temp = temp+((math.log((n/dft), 10))*(((k1+1)*tftd)/(k1*((1-b)+b*(l_d/l_avc))+tftd)))
    RSVd = temp
    # print("document " + str(document) + " RSVd is " + str(RSVd))
    return RSVd


def compute_l_avc(n):
    sum = 0
    for token_number in tokens_number.values():
        sum = sum + int(token_number)
    return sum/n


def bm25_query(query_list):
    # k1 = 1.2 #1.2
    # b = 0.75 #0 to 1
    print("Input k1: ")
    k1=float(input())
    print("Input b: ")
    b =float(input())

    documents = multiple_query(query_list, PARAMETER.QUERY_OR)
    # print(documents)
    for (i,v) in enumerate(documents):
        documents[i] = v[0]
    documents_RSVd = {}
    for document in documents:
        documents_RSVd[document] = compute_RSVd(str(document), query_list,k1,b)
    sorted_RSVd = sorted(documents_RSVd.items(), key=lambda x: x[1], reverse=True)
    print(str(len(sorted_RSVd)) + " documents were ranked.")
    print(sorted_RSVd)


def deal_with_query(query):
    """  Decide the terms and operator in the query. """
    query_list = []
    query_list_or = []
    query_list_and = []
    operator = ""
    query_raw = query.split(" ")
    if len(query_raw) == 1:
        query_list = query_raw
        operator = PARAMETER.QUERY_SINGLE
    elif query_raw[0] == PARAMETER.QUERY_BM25:
        query_list = query_raw[1:]
        operator = PARAMETER.QUERY_BM25
    else:
        if query_raw[1] == PARAMETER.QUERY_OR:
            query_list_or.append(query_raw[0])
            for (i, v) in enumerate(query_raw):
                if v == PARAMETER.QUERY_OR:
                    query_list_or.append(query_raw[i + 1])
            operator = PARAMETER.QUERY_OR
            query_list = query_list_or
        elif query_raw[1] == PARAMETER.QUERY_AND:
            query_list_and.append(query_raw[0])
            for (i, v) in enumerate(query_raw):
                if v == PARAMETER.QUERY_AND:
                    query_list_and.append(query_raw[i + 1])
            operator = PARAMETER.QUERY_AND
            query_list = query_list_and
    query_list = [re.sub(r'[\W\s]', '', token) for token in query_list]
    return query_list, operator


def get_search_dict(query_list):
    print("Getting ……")
    search_index = PARAMETER.STOP_WORDS_150_MERGE_BLOCK_PATH
    global search_dict
    search_dict = {}
    try:
        if not os.listdir(search_index):
            print("The index for dictionary is empty, please generate it first! ")
            os._exit(0)
    except FileNotFoundError:
        print("The index for dictionary is empty, please generate it first! ")
        os._exit(0)
    for term in query_list:
        for file in os.listdir(search_index):
            fo = open(search_index + file)
            line = fo.readline()
            has_term = False
            while line:
                line_term, posting = line.rsplit(":", 1)
                if line_term == term:
                    search_dict[term] = ast.literal_eval(posting)
                    has_term = True
                    break
                line = fo.readline()
            if has_term:
                break
    # print(search_dict)


def get_tokens_number_dict():
    global tokens_number
    if os.path.isfile("tokens_number.json"):
        fo = open("tokens_number.json", 'r')
        tokens_number =json.load(fo)
    else:
        print("No tokens record! Creat it first!")
        os._exit(0)
    global n
    global l_avc
    n = len(tokens_number)
    l_avc = compute_l_avc(n)


def start_query():
    print("**"*40)
    print("Please input query: ")
    query = input().lower().strip()
    while query.lower() != PARAMETER.EXIT:
        try:
            query_list, operator = deal_with_query(query)
            get_search_dict(query_list)
            get_tokens_number_dict()
        except IndexError:
            print("Wrong query format! Input again!")
            start_query()
        print("Start " + operator.upper() + " query")
        print("Keyword: " + str(query_list))
        query_list = check_exist(query_list)
        if operator == PARAMETER.QUERY_AND or operator == PARAMETER.QUERY_OR or operator == PARAMETER.QUERY_SINGLE:
            result = multiple_query(query_list, operator)
            for (i, v) in enumerate(result):
                result[i] = v[0]
            print(str(len(result)) + " documents were found." + "Total result: " + str(result))
            if operator == PARAMETER.QUERY_AND:
                check_and_query(query_list, result)
            elif operator == PARAMETER.QUERY_OR:
                doc_id_sorted(query_list, result)
        elif operator == PARAMETER.QUERY_BM25:
            bm25_query(query_list)
        else:
            print("Operator wrong! Input again!")
        print("**" * 40)
        query = input().lower().strip()

    os._exit(0)


if __name__ == '__main__':
    start_query()