#!/usr/bin/python
# TODO: Some ideas on how to make more efficient on link below:
# http://pythonfiddle.com/huffman-coding-text/
from collections import Counter
import math
import queue as q


def main():
    test_str = "Milk, milk, lemonade;\n" + \
                "'round the corner, fudge is made.\n" + \
                "Push the button, pull the chain,\n" + \
                "out comes chocolate choo-choo train."
    # test_list = [100, 80, 90, 22, 64, 32, 72, 90, 123, 45, 23, 100, 23]
    huffer = HuffmanCodec(uncompressed_str=test_str)
    print("Test string:")
    print("================================================================")
    print(test_str)
    print()
    symbol_count = huffer.uncompressed_symbols_count
    print("Symbol frequencies of test_str: Symbol count: " + str(symbol_count))
    print("================================================================")
    sorted_freqs = huffer.frequencies_list
    print(sorted_freqs)
    print()
    print(huffer.frequncies_table_str)
    print()
    print("Huffman Codes:")
    print("================================================================")
    print(str(huffer.huffman_code_dict))


def lazy_property(fn):
    '''Decorator that makes a property lazy-evaluated.
    '''
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class HuffmanNode(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def nodes(self):  # TODO: Is this needed?! same as childre()
        return (self.left, self.right)

    def children(self):
        return((self.left, self.right))

    def __str__(self):
        return "%s_%s" % (self.left, self.right)


class HuffmanCodec(object):
    def __init__(self,
                 uncompressed_file=None,
                 uncompressed_str=None,
                 uncompressed_list=None):
        # Semantic should be to generate a str, from a file,
        # and potentially a list of codes from a string.
        # To preserve that, if a file is given, all other values are optional.
        # Then if a string is given, the list is optional
        # If a file is given, send an empty string or list to chose which type
        # to encode to/ decode from.
        if uncompressed_file is not None:
            self.__uncompressed_file = uncompressed_file
            if uncompressed_str is not None:
                self.__uncompressed_str = uncompressed_file.read()
                self.__uncompressed_list = None
            elif uncompressed_list is not None:
                self.__uncompressed_str = uncompressed_file.read()
                self.__uncompressed_list = []
                index = 0
                for character in uncompressed_str:
                    self.__uncompressed_list[index] = int(uncompressed_list)
                    index += 1
                self.__uncompressed_str = None
            else:
                self.__uncompressed_str = uncompressed_file.read()
                self.__uncompressed_list = None
        elif uncompressed_str is not None:
            self.__uncompressed_file = None
            self.__uncompressed_str = uncompressed_str
            self.__uncompressed_list = None
        else:
            self.__uncompressed_file = None
            self.__uncompressed_str = None
            self.__uncompressed_list = uncompressed_list

    @lazy_property
    def frequencies_list(self):
        if self.__uncompressed_list is not None:
            self._frequencies_list = Counter(self.__uncompressed_list)

        elif self.__uncompressed_str is not None:
            self._frequencies_list = Counter(self.__uncompressed_str)
        else:
            error_msg = "Error: HuffmanCodec.frequencies_list() " + \
                "can't run before initialization!"
            raise AttributeError(error_msg)
        return self._frequencies_list

    @lazy_property
    def uncompressed_symbols_count(self):
        if self.__uncompressed_list is not None:
            self._uncompressed_symbols_count = len(self.__uncompressed_list)
        elif self.__uncompressed_str is not None:
            self._uncompressed_symbols_count = len(self.__uncompressed_str)
        else:
            error_msg = "Error: HuffmanCodec.uncompressed_symbols_count " + \
                "can't be accessed before initialization!"
            raise AttributeError(error_msg)
        return self._uncompressed_symbols_count

    # def __huffman_code(self, node, left=True, binString=""):
    #     if type(node) is str:  # TODO: Why this?
    #         return {node: binString}
    #     (left, right) = node.children()
    #     code_dict = dict()
    #     code_dict.update(self.__huffman_code(), True, binString + "0")
    #     code_dict.update(self.__huffman_code(), False, binString + "1")
    #     return code_dict
    #
    # @lazy_property
    # def huffman_tree(self, debug=False):
    #     nodes = self.frequencies_list.most_common()
    #     # pq = q.PriorityQueue()
    #     # for symbol, count in nodes:  # 1. Make leaf nodes for codes
    #     #     pq.put((count, symbol))             # 2. put them into the
    #     # while pq.qsize() > 1:
    #     #     left, right = pq.get(), pq.get()
    #     #     node = HuffmanNode(left=left, right=right, symbol=symbol)
    #     #     pq.put((left[0] + right[0], node))
    #     # self._huffman_tree = pq.get()
    #     # return self._huffman_tree
    #     while len(nodes) > 1:
    #         code1, count1 = nodes[-1]
    #         code2, count2 = nodes[-2]
    #         nodes = nodes[:-2]
    #         node = HuffmanNode(left=code1, right=code2)
    #         nodes.append((node, count1 + count2))
    #     if debug:
    #         print("left: " + nodes[0][0].nodes()[0])
    #         print("right: " + nodes[0][0].nodes()[1])
    #     nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    #     self._huffman_tree = nodes
    #     return self._huffman_tree

    @lazy_property
    def huffman_code_dict(self):
        self._huffman_code_dict = self.__huffman_code(self.huffman_tree[0][0])
        return self._huffman_code_dict

    def print_huffman_tree(self):
        tree = self.huffman_tree
        print(str(tree))

    @lazy_property
    def frequncies_table_str(self, width=80, row_major=True):
        # First ensure that all the data necessary is already present
        if self.__uncompressed_list is None and \
             self.__uncompressed_str is None:
            error_msg = "Error: HuffmanCodec.frequencies_table_str() " + \
                "attempted to print list without a given data stream."
            raise AttributeError(error_msg)
            # Is this a list or string, important distinction on how
            #   printing is handled
        is_a_list = True
        if self.__uncompressed_list is None:
            is_a_list = False

        # Acquire the frequencies_list
        # frequencies_list is a lazy_property so if this is the first access,
        #   then it is going to be computed
        freq_dict = self.frequencies_list
        freq_dict = Counter(freq_dict)
        freq_dict = freq_dict.most_common()

        # Create string for header of the printed table
        header_str = "Sorted Codeset & Their Counts:\n"
        for i in range(0, width):
            header_str += "="

        # Find the symbols and codes with the most digits/chars
        # Necessary to format table with fixed widths
        max_symbol_digits = 1
        max_count_digits = 1
        if is_a_list:
            index = 0
            for symbol, count in freq_dict:
                hex_digits = math.ceil(symbol / 16) + 2
                symbol = hex(symbol)
                freq_dict[index] = symbol
                count_digits = math.ceil(count / 10)
                if hex_digits > max_symbol_digits:
                    max_symbol_digits = hex_digits
                if count_digits > max_count_digits:
                    max_count_digits = count_digits
                index += 1
        else:
            index = 0
            for symbol, count in freq_dict:
                if symbol == '\n':
                    freq_dict[index] = "\\n", count
                    symbol = "\\n"
                if symbol == ' ':
                    freq_dict[index] = "sp", count
                    symbol = "sp"
                if symbol == '\t':
                    freq_dict[index] = "\\t", count
                    symbol = "\\t"
                count_digits = math.ceil(count / 10)
                symbol_digits = len(str(symbol))
                if count_digits > max_count_digits:
                    max_count_digits = count_digits
                if symbol_digits > max_symbol_digits:
                    max_symbol_digits = symbol_digits
                index += 1

        # Calculate cell width based on:
        # -- largest symbols/codes, visual delimiters, TODO: padding
        # Calculate cells per row based on specified table width
        cell_width = width / (max_symbol_digits + max_count_digits + 5)
        cell_width = math.ceil(cell_width)
        cells_per_row = math.floor(width / cell_width)
        cells_in_row = 1
        table_str = ""

        # Iterate all frequencies entries:
        # - Calculate extra padding for shorter codes/symbols if needed
        # - Concatenate padding, delimiters and codes/symbols to string
        # - Add newlines once the max number of cells per row reached
        for symbol, count in freq_dict:
            if cells_in_row > cells_per_row:
                cells_in_row = 1
                table_str += "\n"
            cells_in_row += 1
            table_str += "  "
            for i in range(0, max_symbol_digits - len(str(symbol))):
                table_str += " "
            table_str += str(symbol)
            table_str += " : "
            for i in range(0, max_count_digits - len(str(count))):
                table_str += " "
            table_str += str(count)
            table_str += "  "
        self._frequncies_table_str = header_str + "\n" + table_str
        return self._frequncies_table_str


# execute main to handle program order while maintaining forward declarations
main()
