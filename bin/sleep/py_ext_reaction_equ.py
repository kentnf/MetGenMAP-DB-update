#!/usr/bin/python

import sys, os, string

ifile1 = sys.argv[1]

compound_list = {}

def load_compound():
	input=open('compound_class_list.txt','r')
	for line in input.readlines():
		list = string.split(line, '\t')
		if len(list) > 1:
			id1 = string.strip(list[0])
			id2 = string.strip(list[1])
			compound_list[id1] = id2
	input.close()

def load_reactions_left_right(filename):
	input=open(filename,'r')
	output=open('left_right.txt','w')
	cid = ''
	lefts = []
	rights = []
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				cid = id
			elif idf == 'LEFT':
				left_id = string.replace(line,'LEFT - ', '')
				left_id = string.strip(left_id)
				lefts.append(left_id)
			elif idf == 'RIGHT':
				right_id = string.replace(line,'RIGHT - ', '')
				right_id = string.strip(right_id)
				rights.append(right_id)
			else:
				pass
		if line[:2] == '//':
			if len(cid) > 0 and len(lefts) > 0 and len(rights) > 0:
				output.write(cid)
				output.write('\t')
				count = 1
				for L in lefts:
					#output.write(L)
					if L[0] == '|':
						L = L[1:]
					if L[-1] == '|':
						L = L[:-1]

					if compound_list.has_key(L) == 1:
						#output.write('[')
						output.write(compound_list[L])
						#output.write(']')
					else:
						#output.write('[')
						output.write(L)
						#output.write(']')
					count += 1
					if count > 1 and count <= len(lefts):
						output.write(' + ')			
				count = 1
				output.write(' = ')
				for R in rights:
					#output.write(R)
					if R[0] == '|':
						R = R[1:]
					if R[-1] == '|':
						R = R[:-1]

					if compound_list.has_key(R) == 1:
						#output.write('[')
						output.write(compound_list[R])
						#output.write(']')
					else:
						#output.write('[')
						output.write(R)
						#output.write(']')
					count += 1
					if count > 1 and count <= len(rights):
						output.write(' + ')

				output.write('\n')
			cid = ''
			lefts = []
			rights = []
	output.close()
	input.close()


load_compound()
load_reactions_left_right(ifile1)
