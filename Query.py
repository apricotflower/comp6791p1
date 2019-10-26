import os
import PARAMETER
import ast
from collections import OrderedDict
import itertools

search_dict = dict()


def single(query_list):
    # print("Keyword: " + str(query_list))
    try:
        result = search_dict[query_list[0]]
    except KeyError:
        print("Not such keyword in dictionary ! ")
        start_query()
    return result


def check_and_query(query_list, result):
    if len(result) == 0:
        print("**"*20)
        print("No result for this AND query, start to print results of smaller size in this query ……")
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
                    print("Result: " + str(result))
                    print("**"*10)
            i = i + 1
            shorter_lists = list(itertools.combinations(query_list, len(query_list) - i))
            # print(shorter_lists)


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
    # print("Result for " + str(p1) + " or " + str(p2) + " is " + str(answer))
    return answer


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
    # print("Result for " + str(p1) + " and " + str(p2) + " is " + str(answer))
    return answer


def multiple_query(query_list, operator):
    # print("Keyword: " + str(query_list))
    try:
        query_list.sort(key=lambda x: len(search_dict[x]))
    except KeyError:
        print("Not such keyword in dictionary ! ")
        start_query()
    # print("sorted: " + str(query_list))
    result = search_dict[query_list[0]]
    rest_list = query_list[1:]
    # print("rest list: " + str(rest_list))
    while len(result) != 0 and len(rest_list) != 0:
        if operator == PARAMETER.QUERY_AND:
            result = and_query_each(result, search_dict[rest_list[0]])
        elif operator == PARAMETER.QUERY_OR:
            result = or_query_each(result, search_dict[rest_list[0]])
        rest_list = rest_list[1:]
        # print("rest list: " + str(rest_list))
    return result


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
    print("**"*40)
    print("Please input query: ")
    query = input().lower().strip()
    while query.lower() != PARAMETER.EXIT:
        query_list, operator = deal_with_query(query)
        print("Start " + operator.upper() + " query")
        print("Keyword: " + str(query_list))
        if operator == PARAMETER.QUERY_AND:
            result = multiple_query(query_list,operator)
            print("Total result: " + str(result))
            check_and_query(query_list, result)
            print("**" * 40)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_OR:
            result = multiple_query(query_list, operator)
            print("Total result: " + str(result))
            doc_id_sorted(query_list, result)
            print("**" * 40)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_SINGLE:
            result = single(query_list)
            print("Total result: " + str(result))
            print("**" * 40)
            query = input().lower().strip()
        else:
            print("**" * 40)
            print("Operator wrong! Input again!")
            query = input().lower().strip()

    os._exit(0)

load_dict()