#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module generates test data for PyExtSort and puts it to gen_data.dat file
"""
__author__ = 'Alex Dobrushskiy'

from string import letters, digits, lowercase
from random import choice, randint
from time import time
from datetime import datetime

data = []
now = int(time())
for i in range(10000):
    uname_len, domain_len = randint(3, 20), randint(3, 20)
    rand_word = lambda x: ''.join(choice(letters+digits) for i in range(x))
    email = rand_word(uname_len) + '@' + rand_word(domain_len) + '.' + \
            ''.join(choice(lowercase) for i in range(3))
    rand_time = datetime.fromtimestamp(randint(1, now)).isoformat()
    data.append(email + ' ' + rand_time + ' ' + str(i) + '\n')

f = open('gen_data.dat', 'w')
for st in data:
    f.write(st)
