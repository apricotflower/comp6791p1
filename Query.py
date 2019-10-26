import os
import PARAMETER
import ast
from collections import OrderedDict

search_dict = dict()


def single(query_list):
    print("Keyword: " + str(query_list))
    print("Total result: " + str(search_dict[query_list[0]]))


def or_query_each(p1, p2):
    answer = []
    p1_pointer = 0
    p2_pointer = 0
    while len(p1) > p1_pointer and len(p2) > p2_pointer:
        if p1[p1_pointer] == p2[p2_pointer]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
            p2_pointer = p2_pointer + 1
        elif p1[p1_pointer] < p2[p2_pointer]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
        else:
            answer.append(p2[p2_pointer])
            p2_pointer = p2_pointer + 1
    if p1_pointer == len(p1):
        answer = answer + p2[p2_pointer:]
    elif p2_pointer == len(p2):
        answer = answer + p1[p1_pointer:]
    print("Result for " + str(p1) + " or " + str(p2) + " is " + str(answer))
    return answer


def doc_id_sorted(query_list, result):
    id_dict = {}
    for id in result:
        for term in query_list:
            if id in search_dict[term]:
                if id not in id_dict:
                    id_dict[id] = 1
                else:
                    id_dict[id] = id_dict[id] + 1
    sorted_id = sorted(id_dict.items(), key= lambda x:x[1],reverse=True)
    print("Order: " + str(sorted_id))


def or_query(query_list):
    print("Keyword: " + str(query_list))
    query_list.sort(key=lambda x: len(search_dict[x]))
    print("sorted: " + str(query_list))
    result = search_dict[query_list[0]]
    rest_list = query_list[1:]
    print("rest list: " + str(rest_list))
    while len(result) != 0 and len(rest_list) != 0:
        result = or_query_each(result, search_dict[rest_list[0]])
        rest_list = rest_list[1:]
        print("rest list: " + str(rest_list))
    print("Total result: " + str(result))
    doc_id_sorted(query_list, result)


def and_query_each(p1, p2):
    answer = []
    p1_pointer = 0
    p2_pointer = 0
    while len(p1) > p1_pointer and len(p2) > p2_pointer:
        if p1[p1_pointer] == p2[p2_pointer]:
            answer.append(p1[p1_pointer])
            p1_pointer = p1_pointer + 1
            p2_pointer = p2_pointer + 1
        elif  p1[p1_pointer] < p2[p2_pointer]:
            p1_pointer = p1_pointer + 1
        else:
            p2_pointer = p2_pointer + 1
    print("Result for " + str(p1) + " and " + str(p2) + " is " + str(answer))
    return answer


def and_query(query_list):
    print("Keyword: " + str(query_list))
    query_list.sort(key=lambda x: len(search_dict[x]))
    print("sorted: " + str(query_list))
    result = search_dict[query_list[0]]
    rest_list = query_list[1:]
    print("rest list: " + str(rest_list))
    while len(result) != 0 and len(rest_list) != 0:
        result = and_query_each(result, search_dict[rest_list[0]])
        rest_list = rest_list[1:]
        print("rest list: " + str(rest_list))
    print("Total result: " + str(result))


def deal_with_query(query):
    query_list = []
    query_list_or = []
    query_list_and = []
    operator = ""
    query_raw = query.split(" ")
    print(query_raw)
    if len(query_raw) == 1:
        query_list = query_raw
        operator = PARAMETER.QUERY_SINGLE
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
    return query_list, operator


def load_dict():
    print("Loading ……")
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
    query = input().lower().strip()
    while query.lower() != PARAMETER.EXIT:
        query_list, operator = deal_with_query(query)
        if operator == PARAMETER.QUERY_AND:
            print(operator.lower() + " query")
            and_query(query_list)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_OR:
            print(operator.lower() + " query")
            or_query(query_list)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_SINGLE:
            print(operator.lower() + " query")
            single(query_list)
            query = input().lower().strip()
        else:
            print("Operator wrong! Input again!")
            query = input().lower().strip()


load_dict()