import os
import PARAMETER
import ast
from collections import OrderedDict
import itertools

search_dict = dict()


def check_and_query(query_list, result):
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
                    print(str(len(result)) + " documents was found." + "Result: " + str(result))
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


def check_exist(query_list):
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
    # print("Keyword: " + str(query_list))
    query_list.sort(key=lambda x: len(search_dict[x]))
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
    search_index = PARAMETER.STOP_WORDS_150_MERGE_BLOCK_PATH
    global search_dict
    search_dict = OrderedDict()
    try:
        if not os.listdir(search_index):
            print("The index for dictionary is empty, please generate it first! ")
            os._exit(0)
    except FileNotFoundError:
        print("The index for dictionary is empty, please generate it first! ")
        os._exit(0)

    for file in os.listdir(search_index):
        # print(file)
        fo = open(search_index + file)
        line = fo.readline()
        while line:
            term, posting = line.rsplit(":", 1)
            search_dict[term] = ast.literal_eval(posting)
            line = fo.readline()
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
        query_list = check_exist(query_list)
        if operator == PARAMETER.QUERY_AND:
            result = multiple_query(query_list, operator)
            print(str(len(result)) + " documents was found." + " Total result: " + str(result))
            check_and_query(query_list, result)
            print("**" * 40)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_OR:
            result = multiple_query(query_list, operator)
            print(str(len(result)) + " documents was found." + "Total result: " + str(result))
            doc_id_sorted(query_list, result)
            print("**" * 40)
            query = input().lower().strip()
        elif operator == PARAMETER.QUERY_SINGLE:
            result = multiple_query(query_list, operator)
            print(str(len(result)) + " documents was found." + "Total result: " + str(result))
            print("**" * 40)
            query = input().lower().strip()
        else:
            print("**" * 40)
            print("Operator wrong! Input again!")
            query = input().lower().strip()

    os._exit(0)


if __name__ == '__main__':
    load_dict()