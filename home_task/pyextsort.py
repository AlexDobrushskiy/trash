#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alex Dobrushskiy'

from datetime import datetime
from time import time
# from argparse import ArgumentParser
#
# parser = ArgumentParser(description='PyExtSort arguments parser')


def write_tmp_file(file_no, buff, file_list):
    filename = 'tmp_file' + str(file_no)
    f = open(filename, 'w')
    f.write(buff)
    f.close()
    file_list[file_no] = filename


def separate_to_small_parts(input_file, memory_limit):
    input = open(input_file)
    mem_in_use = 0
    tmp_file_index = 0
    tmp_files = {}
    buff = ''
    for line in input:
        mem_in_use += len(line)
        if mem_in_use >= memory_limit:
            write_tmp_file(tmp_file_index, buff, tmp_files)

            mem_in_use = len(line)
            tmp_file_index += 1
            buff = ''
        buff += line
    write_tmp_file(tmp_file_index, buff, tmp_files)
    return tmp_files


def sort_file_by_timestamp(filename):
    f = open(filename)
    tmp_file = f.readlines()
    f.close()

    convert_to_dt = lambda date_string: datetime.strptime(date_string,
                                                          '%Y-%m-%dT%H:%M:%S')
    tmp_file.sort(key=lambda x: convert_to_dt(x.split()[1]))

    f = open(filename, 'w')
    f.writelines(tmp_file)
    f.close()    

if __name__ == '__main__':
    #--------------------------
    #Global config
    # TODO Move to command line parameters
    cpus = 1
    #in bytes
    memory_limit = 20000
    input_file = 'gen_data.dat'
    output_file = 'output.dat'
    #-------------------------------

    tmp_files = separate_to_small_parts(input_file, memory_limit)

    for tmp_file_name in tmp_files.values():
        # нужно распараллелить
        sort_file_by_timestamp(tmp_file_name)

    # # Now let's merge all sorted files into one
    # output = open('output_file', 'w')
    # sorted_files = []
    #
    # # можно распараллелить
    # for small in tmp_files:
    #     sorted_files.append(open(small))
