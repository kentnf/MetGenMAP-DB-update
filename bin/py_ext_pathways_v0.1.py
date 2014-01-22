#!/usr/bin/env python

######## Configuration ########
enzyme_fn = 'enzrxns.dat'
reaction_fn = 'reactions.dat'
gene_fn = 'genes.dat'
protein_fn = 'proteins.dat'
compound_fn = 'compounds.dat'
class_fn = 'classes.dat'
reaction_fn = 'reactions.dat'
pathway_fn = 'pathways.dat'

temp_dir = 'tmp'

######## phtyon modules ########
import sys, string, os

######## ID lists ########
protein_list = {}
enzyme_list = {}
enzyme_name_list = {}
compound_list = {}
reaction_list = {}

######## Loading datasets #######
def load_enzyme(filename):
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
				enzyme_list[eid] = rid
				#print eid, '\t', rid 
			eid = ''
			rid = ''
	input.close()
	
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
				reaction_list[rid] = enz_list
				#print rid, '\t', enz_list
			rid = ''
			enz_list = []
	input.close()
		
def load_proteins(filename_gene, filename_protein):

	gene_list = {}
	input=open(filename_gene,'r')

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
	
	input=open(filename_protein,'r')
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
				protein_list[pid] = gid

			pid = ''
			gid = []
	input.close()
	
def load_enzyme_name(filename):
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
				enzyme_name_list[cid] = cname
				#print cid, '\t', cname 
			cid = ''
			cname = ''
	input.close()	
	
def load_compound(filename):
	input=open(filename,'r')
	cid = ''
	cname = ''
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 2:
			idf = string.strip(list[0])

			if idf == 'UNIQUE-ID':
				id = string.replace(line, 'UNIQUE-ID - ', '')
				id = string.strip(id)
				cid = id
			elif idf == 'COMMON-NAME':
				L = string.replace(line, 'COMMON-NAME - ', '')
				L = string.strip(L)
				cname = L
			else:
				pass
		if line[:2] == '//':
			if len(cid) > 0 and len(cname) > 0:
				#print cid, '\t', cname 
				compound_list[cid] = cname
			cid = ''
			cname = ''
	input.close()		
				
def load_datasets():
	print 'Creat enzyme ID - enzyme list.....' 
	load_enzyme(enzyme_fn)
	
	print 'Creat reaction ID - enzyme IDs list.....'
	load_reaction(reaction_fn)
	
	print 'Creat enzyme - genes list.....'
	load_proteins(gene_fn, protein_fn)
	
	print 'Creat enzyme ID - name list.....'
	load_enzyme_name(enzyme_fn)
	
	print 'Creat compound ID - name list.....' 
	load_compound(compound_fn)
	load_compound(class_fn)	


####### Making directory #######
def get_dirinfo(pname):
	find_dir = 0
	opath =''
	curr_dir = ''
	if os.name != 'posix':	
		curr_dir = '.\\'
	else:
		curr_dir = './'

	for f in os.listdir(curr_dir):
		if f == pname:
			find_dir = 1
			
			dir_path = ''
			if os.name != 'posix':	
				dir_path = '.\\'+pname+'\\'
			else:
				dir_path = './'+pname+'/'			
			for f in os.listdir(dir_path):
				f_name = dir_path+f
				os.remove(f_name)
			break
			
	if find_dir == 0:	
		os.mkdir(pname)

	if os.name != 'posix':	
		opath = '.\\'+pname+'\\'
	else:
		opath = './'+pname+'/'

	return opath

####### Remove temp directory ####### 	
def remove_tmp_dir():
	if os.name != 'posix':
		tmp_path = '.\\'+temp_dir+'\\'	
	else:
		tmp_path = './'+temp_dir+'/'
		
	for f in os.listdir(tmp_path):
		f_name = tmp_path+f
		os.remove(f_name)
	os.rmdir(tmp_path)	
	
####### Building pathways ####### 
def load_pathways(filename):

	dir_pname = temp_dir
	path_file_list = []
	output_path = get_dirinfo(dir_pname)

	input=open(filename,'r')
	file_count = 0
	pid = ''
	rec_count = 0

	rec_list = {}
	rec_equ_list = {}
	direction_list = {}
	for line in input.readlines():
		list = string.split(line)
		reaction_enzyme = ''
		if len(list) > 2:
			idf = string.strip(list[0])
			id = string.strip(list[2])

			if idf == 'UNIQUE-ID':
				pid = id

			elif idf == 'REACTION-LAYOUT':
				rid = string.strip(id)
				if rid[0] == '(':
					rid = rid[1:]
				if rid[0] == '|':
					rid = rid[1:]
				if rid[-1] == '|':
					rid = rid[:-1]
				if rec_list.has_key(rid) == 0:
					rec_count += 1
					rec_list[rid] = rec_count

					direction_flag = 0
					for L in list:
						if direction_flag == 1:
							if L[0] == ':':
								L = L[1:]
							if L[-1] == ')':
								L = L[:-1]
							direction_list[rid] = L
							break
						if L ==  '(:DIRECTION':
							direction_flag = 1
					
					equ = ''
					if list[3] == '(:LEFT-PRIMARIES)':
						L = string.replace(list[2], '(', '')
						equ += L 
					
					else:
						equ_left_flag = 0
						equ_right_flag = 0
						for L in list:
							if equ_left_flag == 1:
								if L[-1] == ')':
									L = L[:-1]
									L = string.replace(L, '|', '')
									if compound_list.has_key(L) == 1:
										equ += compound_list[L] 
									else:
										equ += ' ERROR '
									equ_left_flag = 0
								else:
									L = string.replace(L, '|', '')
									if compound_list.has_key(L) == 1:
										equ += compound_list[L]
									else:
										equ += ' ERROR '
									equ += ' + '
								
							if equ_right_flag == 1:
								equ += ' = '
								if L[-1] == ')':
									L = L[:-2]
									L = string.replace(L, '|', '')
									if compound_list.has_key(L) == 1:
										equ += compound_list[L]
									else:
										equ += '  ERROR ' 
									equ_right_flag = 0
								else:
									L = string.replace(L, '|', '')
									if compound_list.has_key(L) == 1:
										equ += compound_list[L]
									else:
										equ += '  ERROR '
									equ += ' + '

							if L ==  '(:LEFT-PRIMARIES':
								equ_left_flag = 1
							if L ==  '(:RIGHT-PRIMARIES':
								equ_right_flag = 1
					
							
					rec_equ_list[rid] = equ

		if line[:2] == '//':
			ofile = pid
			file_count += 1

			ofile = string.replace(ofile, '/', '_')
			ofile = output_path + ofile
			output=open(ofile,'w')
			
			print pid
			path_id = string.replace(pid, '/', '_')
			path_file_list.append(path_id)

			for i in range(len(rec_list)):
				rec_id = ''
				for rec in rec_list:
					c = rec_list[rec]
					if c == i+1:
						rec_id = rec
						break
				reaction_enzyme = ''
				
				enz_list = []
				if reaction_list.has_key(rec_id) == 1:
					enz_list = reaction_list[rec_id]

				gene_list = []
				enz_name_list ={}
				g_list_check = {}
				enz_count = 1
				if len(enz_list) > 0: 
					#genes = ''
					genes =[]
					protein = ''
					for E in enz_list:
						if enzyme_list.has_key(E) == 1:
							protein = enzyme_list[E]
						if len(protein) > 0:
							if protein_list.has_key(protein) == 1:
								genes = protein_list[protein]
						if len(genes) > 0:
							#g_list = string.split(genes)
							#for G in g_list:
							for G in genes:		
								if g_list_check.has_key(G) == 0:
									gene_list.append(G)
									g_list_check[G] = 1


						if enzyme_name_list.has_key(E) == 1:
							name = enzyme_name_list[E]
							if enz_name_list.has_key(name) == 1:
								value = enz_name_list[name]
								value += 1
								enz_name_list[name] = value
							else:
								enz_name_list[name] = 1
								
				if direction_list[rec_id] == 'NIL':
					rec_id = string.replace(rec_id, '/', '_')
					output.write(rec_id)
					output.write('\n')
				
				else:
					max_value = 0
					for enz in enz_name_list:
						value = enz_name_list[enz]
						if value > max_value:
							max_value = value
							reaction_enzyme = enz
					pid = string.replace(pid, '/', '_')
					output.write(pid)
					output.write('\t')
					output.write(rec_id)
					output.write('\t')
					output.write(reaction_enzyme)
					output.write('\t')
					if rec_equ_list.has_key(rec_id) == 1:
						output.write(rec_equ_list[rec_id])
					else:
						output.write(' ERROR')
					output.write('\t')
					g_count = 1
					for g in gene_list:
						if g_count > 1 and g_count <= len(gene_list):
							output.write('#')

						output.write(g)
						g_count += 1
					output.write('\n')

			output.close()

			pid = ''
			rec_count = 0
			rec_list = {}
			direction_list = {}
	input.close()
	print 'The number of fils: ', file_count
	return path_file_list
			

####### Cancatenate whole pathways whin a superpathway ####### 
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
	
def refine_pathway(filelist, dir_pname):

	output_path = get_dirinfo(dir_pname)

	for k in range(len(filelist)):
		reactions = ''
		
		input_path = ''
		if os.name != 'posix':
			input_path = '.\\'+temp_dir+'\\'	
		else:
			input_path = './'+temp_dir+'/'
		text_result = ext_subpathway(input_path, filelist[k], filelist[k], reactions)
		text_result = remove_red(text_result)

		ofn = output_path + filelist[k]
		print ofn

		output = open(ofn,'w')
		output.write(text_result)
		output.close()
		
	remove_tmp_dir()

####### Main procesure ####### 
if __name__ == '__main__':

	if len(sys.argv) < 2:  # Check arguments
		print '\n\nPlease try again!!!'
		print 'Usage:  python  py_ext_pathways_v0.1.py  [result directory]'
		sys.exit() 

	path_name = sys.argv[1]

	load_datasets() # loading datasets
	file_list = load_pathways(pathway_fn)  # building pathway 
	refine_pathway(file_list, path_name)   # refine pathways