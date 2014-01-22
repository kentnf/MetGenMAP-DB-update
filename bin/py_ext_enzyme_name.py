#!/usr/bin/python

import sys, string

ifile1 = sys.argv[1]

def load_enzyme(filename):
	input=open(filename,'r')
	cid = ''
	cname = ''
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				cid = id
			elif idf == 'COMMON-NAME':
				L = string.replace(line, 'COMMON-NAME - ', '')
				L = string.strip(L)
				cname = L
			else:
				pass
		if line[:2] == '//':
			if len(cid) > 0 and len(cname) > 0:
				print cid, '\t', cname 
			cid = ''
			cname = ''
	input.close()

load_enzyme(ifile1)
