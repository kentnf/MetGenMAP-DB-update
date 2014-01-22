#!/usr/bin/python

import sys, os, urllib, urlparse, string, re

ifile1 = sys.argv[1]

def load_protein(filename):
	input=open(filename,'r')
	eid = ''
	rid = ''
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				eid = id
			elif idf == 'ENZYME':
				rid = id
			else:
				pass
		if line[:2] == '//':
			if len(eid) > 0 and len(rid) > 0:
				print eid, '\t', rid 
			eid = ''
			rid = ''
	input.close()


load_protein(ifile1)
