import PARAMETER
import Deal_File
from collections import OrderedDict
import os
import ast
import copy

terms_num = 0
nonpositional_postings_num = 0


def seperate_block():
    block_document = {}
    i = 0
    len_size_leave = len(deal_all_document)
    for (key, value) in deal_all_document.items():
        block_document[key] = value
        len_size_leave = len_size_leave - 1
        i = i + 1
        if i >= PARAMETER.BLOCK_SIZE or len_size_leave == 0:
            i = 0
            break
    for key in block_document:
        del deal_all_document[key]
    return block_document


def spimi_invert(block_document, block_number, block_index):
    block_dict = {}
    fo = open(block_index + "BLOCK" + str(block_number) + ".txt", "a+")

    for (key, value) in block_document.items():
        # print("Search in article " + key)
        for term in value:
            if term not in block_dict:
                index_list = [key]
                block_dict[term] = index_list
            else:
                if key not in block_dict[term]:
                    block_dict[term].append(key)

    print("Sorting……")
    keys_list = sorted(block_dict.keys())
    sorted_block_dict = OrderedDict()
    for key in keys_list:
        sorted_block_dict[key] = block_dict[key]

    for (key, value) in sorted_block_dict.items():
        fo.write(key + ":" + str(value) + "\n")
    print("Generate BLOCK" + str(block_number) + " successfully!")


def merge_spimi(block_index,merge_block):
    print("Start merging ……")
    final_i = 0
    fo = open(merge_block + "II"+ str(final_i) + ".txt", "a+")
    final_file_line = 0
    blocks = OrderedDict()
    buffer = OrderedDict()

    for file in os.listdir(block_index):
        # print(type(file))
        blocks[block_index + file] = open(block_index + file)

    remain_block_number = len(blocks)

    for block in blocks.values():
        first_line = block.readline()
        term, posting = first_line.rsplit(":", 1)
        buffer[block.name] = [term, ast.literal_eval(posting)]
       #  buffer[block.name] = [term, posting]
        # print(type(buffer[block.name]))
        # print(block.name + " : " + str(buffer[block.name]))

    while remain_block_number > 0:
        lowest_terms = buffer[min(buffer, key=lambda a: buffer[a][0])][0]
        # print(type(lowest_terms))
        # print(str(lowest_terms))
        lowest_block_names = []
        write_down_posting = []
        # write_down_posting = ""
        write_down_line = lowest_terms + ":"
        for (block_name, all_line) in buffer.items():
            if all_line[0] == lowest_terms:
                lowest_block_names.append(block_name)
                write_down_posting = write_down_posting + all_line[1]
        write_down_posting = list(map(int, write_down_posting))
        write_down_posting.sort()
        # print(write_down_line + str(write_down_posting))

        if final_file_line == PARAMETER.FINAL_TERMS_SIZE - 1:
            fo.write(write_down_line + str(write_down_posting))
            final_i = final_i + 1
            fo = open(merge_block + "II" + str(final_i) + ".txt", "a+")
            final_file_line = 0
        else:
            fo.write(write_down_line + str(write_down_posting) + "\n")

        global terms_num
        global nonpositional_postings_num
        terms_num = terms_num + 1
        nonpositional_postings_num = nonpositional_postings_num + len(write_down_posting)
        final_file_line = final_file_line + 1

        for lowest_block_name in lowest_block_names:
            line = blocks[lowest_block_name].readline()
            if line:
                term, posting = line.rsplit(":", 1)
                buffer[lowest_block_name] = [term, ast.literal_eval(posting)]
                # buffer[lowest_block_name] = [term, posting]
            else:
                del buffer[lowest_block_name]
                print(lowest_block_name + " merge finish!")
                remain_block_number = remain_block_number - 1


def start_spimi(block_index, merge_block):
    global deal_all_document
    deal_all_document = copy.deepcopy(Deal_File.all_document)

    if not os.path.exists(block_index):
        os.makedirs(block_index)

    if not os.path.exists(merge_block):
        os.makedirs(merge_block)

    i = 0
    while len(deal_all_document) > 0:
        block_document = seperate_block()
        # print(len(block_dict))
        spimi_invert(block_document, i, block_index)
        i = i + 1

    merge_spimi(block_index,merge_block)

