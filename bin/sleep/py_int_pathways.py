#!/usr/bin/python

import sys, os, string, re

path_name, odir = sys.argv[1], sys.argv[-1]

def get_input_dirinfo(idir):

	find_dir = 0
	ipath = ''

	for f in os.listdir('./'):
		if f == idir:
			find_dir = 1
			break
	if find_dir == 0:	
		os.mkdir(idir)

	ipath = './'+idir+'/'

	return ipath


def get_output_dirinfo(odir):

	find_dir = 0
	opath = ''

	for f in os.listdir('./'):
		if f == odir:
			find_dir = 1
			break
	if find_dir == 0:	
		os.mkdir(odir)

	opath = './'+odir+'/'

	return opath

def ext_subpathway(ipath, fn, mp, texts):
	try:
		fn = ipath+fn
		input=open(fn,'r')
		for line in input.readlines():
			list = string.split(line, '\t')
			if len(list) > 1:
				pn = string.strip(list[0])
				line = string.replace(line, pn, mp)
				texts += line
			elif len(list) == 1:
				pn = string.strip(list[0])
				texts = ext_subpathway(ipath, pn, mp, texts)
		input.close()
	except:
		pass

	return texts

def remove_red(texts):
	dic = {}
	reactions = ''
	list = string.split(texts, '\n')
	for L in list:
		if dic.has_key(L) == 0:
			dic[L] = 1
			reactions = reactions+L+'\n'
	return reactions

def ins_pathway():
	
	print
	print

	input_path = get_input_dirinfo(path_name)
	print 'Input directory: ', input_path

	output_path = get_output_dirinfo(odir)
	print 'Output directory: ', output_path
	print

	filelist = os.listdir(input_path)

	for k in range(len(filelist)):	
		reactions = ''
		if filelist[k][-3:] != '.py':
			#input_path+filelist[k]
			text_result = ext_subpathway(input_path, filelist[k], filelist[k], reactions)
			text_result = remove_red(text_result)

			ofn = output_path + filelist[k]
			print ofn

			output = open(ofn,'w')
			output.write(text_result)
			output.close()

if __name__ == '__main__':
	ins_pathway()

