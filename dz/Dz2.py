def maximum (spisok):
	max = spisok[1]
	for i in spisok:
		if max<i:
			max = i 
	return max

list = [1,2,3,11,5,7,9,0]
print maximum (list)