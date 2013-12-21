#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alex Dobrushskiy'

from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Process
from heapq import heapify, heappush, heappop


class CustomHeap(object):
    """
    A simple class for usign custom predicate (key) with standart heapq module.
    (c) http://stackoverflow.com/questions/8875706/python-heapq-with-custom-compare-predicate
    """

    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        if initial:
            self._data = [(key(item), item) for item in initial]
            heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heappush(self._data, (self.key(item), item))

    def pop(self):
        return heappop(self._data)[1]


def process_args():
    parser = ArgumentParser(description='PyExtSort args parser')
    parser.add_argument('-c', action='store', dest='cpus', help="Number of CPU's",
                        type=int)
    parser.add_argument('-l', action='store', dest='memory_limit',
                        help='Memory limit, bytes', type=int)
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()
    if args.cpus < 1:
        print "Number of CPU's should be at least 1!"
        exit()
    return args


def write_tmp_file(file_no, buff, file_list):
    """
    This method just writes 'buff' string array to file with name "tmp_file" + if
    provided if 'file_no'. It updates 'file_list' dictionary with just created file name.
    """
    filename = 'tmp_file' + str(file_no)
    f = open(filename, 'w')
    f.write(buff)
    f.close()
    file_list[file_no] = filename


def separate_to_small_parts(input_file, memory_limit):
    """
    This method reads 'input_file' and separates it to several files,
    each is less or equal to 'memory_limit' bytes.
    Returns dictionary with created file names as values and IDs as keys.
    """
    try:
        input = open(input_file)
    except IOError:
        print "Please provide valid file name as input_file"
        exit()
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
    try:
        result = convert_to_dt(record.split()[1])
    except (IndexError, ValueError):
        print "Some data in input file is incorrect. Please check your data."
        exit()

    return result


def sort_file_by_timestamp(filename):
    """
    This method takes a file as an input and sorts it in RAM, overwriting.
    It's assumed that file consists of records like '<email> <ISO timestamp> <id>'.
    This uses ISO timestamp as sort key.
    """
    f = open(filename)
    tmp_file = f.readlines()
    f.close()

    tmp_file.sort(key=record_timestamp)

    f = open(filename, 'w')
    f.writelines(tmp_file)
    f.close()    


def merge_sorted_files(input_files, output_file):
    """
    This method merges files from 'input_files' dict {id:filename} (
    which are assumed already sorted) to one file name 'output_file' which is sorted too.

    This can be upgraded by using heap instead of list in 'local_list' variable.
    Now complexity is O(l*n*log(n)), where l - total number of records, n - number of
    temporary files.
    In case of using heap complexity will be O(l*n).
    """
    output = open(output_file, 'w')

    sorted_files = {}
    for index, filename in input_files.items():
        sorted_files[index] = open(filename)

    local_list = CustomHeap(key=lambda x: record_timestamp(x[1]))
    #initially fill local_list
    for index, file_obj in sorted_files.items():
        # don't care about StopIteration exception. There is not empty files.
        local_list.push((index, file_obj.next()))

    while sorted_files:
        # # Complexity of this loop in O(l*n*log(n))  - see function docstring
        # local_list.sort(key=lambda x: record_timestamp(x[1]))
        index, string_to_write = local_list.pop()
        output.write(string_to_write)
        try:
            local_list.push((index, sorted_files[index].next()))
        except StopIteration:
            del sorted_files[index]
    output.close()


def sort_several_files(files):
    for tmp_file_name in files.values():
        sort_file_by_timestamp(tmp_file_name)


def pack_files_for_processes(cpus, all_files):
    """
    This method puts 'all_files' into several heaps according to CPU's number
        received.
    """
    files_for_processes = {}
    for id, filename in all_files.items():
        if id % cpus not in files_for_processes:
            files_for_processes[id % args.cpus] = {id: filename}
        else:
            files_for_processes[id % args.cpus][id] = filename
    return files_for_processes


if __name__ == '__main__':
    from time import time
    start = time()
    args = process_args()

    tmp_files = separate_to_small_parts(args.input_file, args.memory_limit)

    files_for_processes = pack_files_for_processes(args.cpus, tmp_files)

    processes = []
    for i in range(args.cpus):
        if files_for_processes.get(i):
            processes.append(Process(target=sort_several_files, args=(files_for_processes[i],)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()
    # TODO merge_sorted_files можно сделать параллельным

    tmp_merged_files = {}
    processes = []
    for i in range(args.cpus):
        if files_for_processes.get(i):
            tmp_output_name = 'tmp_output' + str(i)
            processes.append(Process(target=merge_sorted_files,
                                     args=(files_for_processes[i], tmp_output_name)))
            tmp_merged_files[i] = tmp_output_name

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    merge_sorted_files(tmp_merged_files, args.output_file)

    print "time of running: {}".format(time()-start)