#!/usr/bin/python

import sys, os, urllib, urlparse, string, re

ifile, ofile = sys.argv[1], sys.argv[-1]

r_list = []

def load_reaction(filename):
	input=open(filename,'r')
	rid = ''
	enz_list = []
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				rid = id
			elif idf == 'ENZYMATIC-REACTION':
				enz_list.append(id)
			else:
				pass
		if line[:2] == '//':
			if len(rid) > 0 and len(enz_list) > 0:
				r_list.append([rid, enz_list])
			rid = ''
			enz_list = []
	input.close()

def save_reaction(filename):
	output=open(filename,'w')
	for list in r_list:
		id = list[0]
		enz_list = list[1]
		output.write(id)
		for enzs in enz_list:
			output.write('\t')
			output.write(enzs)
		output.write('\n')
	output.close()

load_reaction(ifile)
save_reaction(ofile)
