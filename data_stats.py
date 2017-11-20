#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def file_size(filestr):
    statinfo = os.stat(filestr)
    return statinfo.st_size


if __name__ == '__main__':
    import argparse
    DESCRIPTION = 'Get statistics about a datastream'
    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument('data')
    PARSER.add_argument('--bytesize', '-b',
                        action='store_true',
                        help='get the size in bytes of the file')

    ARGS = PARSER.parse_args()

    DATA = ""
    DATA_IS_FILE = os.path.isfile('test_markup.yml')

    if DATA_IS_FILE:
        DATA = open('test_markup.yml', 'r').read()
    else:
        DATA = ARGS.data

    if ARGS.bytesize:
        if DATA_IS_FILE:
            BYTES = file_size('./test_markup.yml')
            print('File Size(B): ' + str(BYTES))
