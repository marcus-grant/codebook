#!/usr/bin/env python3

# import os
import math
# import numpy as np
# from sys import argv
# import pdb


def main():

    # script, input_path, output_path = argv

    # prt = "Script: " + str(script)
    # print(prt)
    # prt = "Filename: " + str(input_path)
    # print(prt)

    # prt = "Compressing file " + str(input_path) + " using LZW algorithm."
    # print(prt)
    # prt = "Here's the file (size: " + str(os.stat(input_path).st_size) + "):"
    # print(prt)

    input_file = open("a.yml", 'r')
    # output_file = open(output_path, 'w')

    uncompressed = input_file.read()
    print(uncompressed)
    # compressed, code_book, code_freq, dict_size = compress_lzw(uncompressed)
    # code_length = int(math.ceil(math.log(dict_size, 2)))
    # print(code_length)
    # print(compressed)
    print("==========================")
    print(str(decompress_lzw_to_str(compressed)))
    # compressed_hex_code = {}
    # for key, value in list(compressed.items()):
    #     prompt = "compressed[" + str(key) + "] = " + str(compressed[key])
    #
    #     compressed_hex_code[key] = hex(compressed[key])
    repr(compressed)
    # print("Generated Codes:")
    # print("==================================================================")
    # print(str(code_book))
    # print("Compressed coded sequence as hex-decimals:")
    # print("==================================================================")
    # print(str(compressed_hex_code))

    # prompt = "Compressed Code:\n" + str(compressed) + \
    #     "\n\n\nCode Book:\n" + str(code_book) + "\n\n\nCode Frequency:\n" + \
    #     str(code_freq) + "\n\ndict_size: " + str(dict_size) + \
    #     "\n\ncode-length: " + str(len(compressed))
    #
    # print(prompt)
    #
    # import operator
    # sorted_codes = sorted(code_freq.items(), reverse=True, key=operator.itemgetter(1))
    # print("Sorted Codes:\n" + repr(sorted_codes))


def compress_lzw(uncompressed_str):
    # start by preparing objects
    # uncompressed_str = in_file.read()
    compressed_code_list = []

    # create the lzw code dictionary
    # code_dictionary = {i: chr(i) for i in range(dict_size)}
    dict_size = 256
    # current_code = 256
    code_dictionary = {chr(i): i for i in range(dict_size)}
    # code_dictionary = {}
    code_frequency = {}

    # print("Single Char Codebook:\n" + repr(code_dictionary))
    # TODO: Check speedup/storage space for only using
    # single chars present in file in dictionary
    # also check if doing so while running regular lzw so you aren't storing
    # single chars that don't get used by themselves makes a big difference
    # for char in uncompressed_str:
    #     if char in code_dictionary:
    #         continue
    #     else:
    #         code_dictionary.append(char)

    # pdb.set_trace()

    current_permutation = ""  # variable to track permutations of characters
    for next_char in uncompressed_str:
        new_permutation = current_permutation + next_char

        # check if the combination of the current permutation + next character
        # are already present in the dictionary
        # pdb.set_trace()
        if new_permutation in code_dictionary:
            # if it already exists, it means a new code can be implemented and
            # stored, move on to add the next character to the permutation
            current_permutation = new_permutation
        else:
            # print("HERE!!!!!!!!!!!")
            # prompt = "Permutation: " + str(current_permutation) + \
            #    " | Code: " + str(code_dictionary[current_permutation])
            # print(prompt)
            compressed_code_list.append(code_dictionary[current_permutation])
            code_dictionary[new_permutation] = dict_size
            dict_size += 1
            if current_permutation in code_frequency:
                code_frequency[current_permutation] += 1
            else:
                code_frequency[current_permutation] = 1
            current_permutation = next_char

    if current_permutation != '':
        compressed_code_list.append(code_dictionary[current_permutation])

    # print("DONE!!!!!")
    return compressed_code_list, code_dictionary, code_frequency, dict_size


def decompress_lzw_to_str(lzw_codes):
    from cStringIO import StringIO
    # first build the initial UTF8 dictionary set so the first LZW sybols
    # can be gathered, and then used to create more complex stored permutations
    compressed = lzw_codes
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result.getvalue()


main()
