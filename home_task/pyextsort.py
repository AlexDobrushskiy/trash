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


def record_timestamp(record):
    """
    This method can be used as a key for compairing records by timestamp.
    :param arg: String of sotring file: '<email> <timestamp_iso> <id>'
    (i.e. record of our input file)
    :return: Datetime object representing second word of given string.
    """
    convert_to_dt = lambda date_string: datetime.strptime(date_string,
                                                          '%Y-%m-%dT%H:%M:%S')
    return convert_to_dt(record.split()[1])


def sort_file_by_timestamp(filename):
    f = open(filename)
    tmp_file = f.readlines()
    f.close()

    tmp_file.sort(key=record_timestamp)

    f = open(filename, 'w')
    f.writelines(tmp_file)
    f.close()    


def merge_sorted_files(input_files, output_file):
    # Now let's merge all sorted files into one
    output = open(output_file, 'w')

    # можно распараллелить
    # если всего n процессоров, то номер любого файла %n дает число от 0 до n-1
    # исходя из этого, выбираем ядра, которые будут обратывать конкретный файл
    sorted_files = {}
    for index, filename in input_files.items():
        sorted_files[index] = open(filename)

    local_list = []
    #initially fill local_list
    for index, file_obj in sorted_files.items():
        # don't care about StopIretation exception. Assume that files are big enought.
        local_list.append((index, file_obj.next()))

    while sorted_files:
        local_list.sort(key=lambda x: record_timestamp(x[1]))
        index, string_to_write = local_list[0]
        del local_list[0]
        output.write(string_to_write)
        try:
            local_list.append((index, sorted_files[index].next()))
        except StopIteration:
            del sorted_files[index]
    output.close()


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

    merge_sorted_files(tmp_files, output_file)


