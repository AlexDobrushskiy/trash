import re
import random
from string import lowercase, uppercase, digits
from time import time

precompiled_pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-\.]{0,18}[a-zA-Z0-9]$|^[a-zA-Z]$')

def validate_precompiled(login):

	return re.match(precompiled_pattern, login)

def validate_re_compile(login):

	pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-\.]{0,18}[a-zA-Z0-9]$|^[a-zA-Z]$')
	return re.match(pattern, login)

def validate_re_simple(login):

	pattern = r'^[a-zA-Z][a-zA-Z0-9\-\.]{0,18}[a-zA-Z0-9]$|^[a-zA-Z]$'
	return re.match(pattern, login)

def manual_validate(login):
	abc = lowercase + uppercase
	abcnum = abc + digits
	all_symbols = abcnum + '.' + '-'
	if not login or len(login) > 20:
		return False
	if login[0] not in abc:
		return False
	if login[-1] not in abcnum:
		return False
	for char in login[1:-1]:
		if char not in all_symbols:
			return False
	return True



# test stuff
right_logins = ['a','b','c','a9', 'b1', 'z0', 'a.1', 'a-54', 'asdfkh237wer7.-11']
wrong_logins = ['1', '.1', '-1', 'a-', 'b.', '1aasd', 'aaaaaaaaaaaaaaaaaaaaaaaaaaa', '...']


def generate_right_login():
	abc = lowercase + uppercase
	abcnum = abc + digits
	all_symbols = abcnum + '.' + '-'

	choice = random.randint(1, 20)
	if choice == 1:
		return random.choice(abc)
	elif choice == 2:
		return random.choice(abc) + random.choice(abcnum)
	else:
		middle = ''
		for i in range(choice-2):
			middle += random.choice(all_symbols)
		return random.choice(abc) + middle + random.choice(abcnum)

	#TODO create right-login generator
	#TODO create wrong-login generator


# if __name__ == '__main__':
# 	for login in right_logins:
# 		assert manual_validate(login) 
# 	for login in wrong_logins:
# 		assert not manual_validate(login) 
right_logins = []
for i in range(100000):
	right_logins.append(generate_right_login())

start = time()
for login in right_logins:
	assert validate_precompiled(login)
print time()-start

start = time()
for login in right_logins:
	assert validate_re_simple(login)
print time()-start

start = time()
for login in right_logins:
	assert validate_re_compile(login)
print time()-start

start = time()
for login in right_logins:
	assert manual_validate(login)
print time()-start