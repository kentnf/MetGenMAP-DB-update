#!/usr/bin/python

import sys, string, re

ifile1, ifile2, ofile = sys.argv[1], sys.argv[2], sys.argv[-1]

gene_list = {}

def load_genes(filename):
	input=open(filename,'r')

	pid = []
	gid = ''
	aid = ''
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'PRODUCT':
				pid.append(id)
			elif idf == 'COMMON-NAME':
				gid = id
			elif idf == 'UNIQUE-ID':
				if id[:2] == 'G-':
					pid.append(id)
			else:
				pass

			try:
				tmp = re.search('A[A-Z][0-9A-Z][A-Z]\d\d\d\d\d',line)
				aid = tmp.group(0)
			except:
				pass
				
		if line[:2] == '//':
			if len(pid) > 0 and (len(gid) > 0 or len(aid) > 0):
				for I in pid:	
					if gene_list.has_key(I) == 0:
						if len(aid) > 0:
							gene_list[I] = aid
						else:
							gene_list[I] = gid	
			pid = []
			gid = ''
			aid = ''

	input.close()

def load_proteins(filename):
	input=open(filename,'r')
	output=open(ofile,'w')

	pid = ''
	gid = []
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				pid = id
			elif idf == 'GENE':
				if id[:2] == 'G-':
					if gene_list.has_key(id) == 1:
						id = gene_list[id]
				gid.append(id)

			elif idf == 'COMPONENTS':
				if id[0] == 'A':
					id = id[:9]
					gid.append(id)
				else:
					if gene_list.has_key(id) == 1:
						id = gene_list[id]
						gid.append(id)
			else:
				pass
		if line[:2] == '//':
			if len(pid) > 0 and len(gid) > 0:
				#print pid, '\t', gid 
				output.write(pid)
				output.write('\t')
				for L in gid:
					output.write(L)
					output.write(' ')
				output.write('\n')

			pid = ''
			gid = []

	input.close()
	output.close()

load_genes(ifile1)
load_proteins(ifile2)
