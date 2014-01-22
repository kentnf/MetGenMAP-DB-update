#!/usr/bin/python

import sys, string, os

ifile1, path_name = sys.argv[1], sys.argv[-1]

protein_list = {}
enzyme_list = {}
reaction_list = {}
left_right_list = {}
enzyme_name_list = {}

def load_datasets():
	input=open('protein_list.txt','r')
	for line in input.readlines():
		list = string.split(line, '\t')
		if len(list) > 1:
			id1 = string.strip(list[0])
			id2 = string.strip(list[1])
			protein_list[id1] = id2
	input.close()

	input=open('enzyme_list.txt','r')
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 1:
			id1 = string.strip(list[0])
			id2 = string.strip(list[1])
			enzyme_list[id1] = id2
	input.close()

	input=open('left_right.txt','r')
	for line in input.readlines():
		list = string.split(line, '\t')
		if len(list) > 1:
			id1 = string.strip(list[0])
			id2 = string.strip(list[1])
			left_right_list[id1] = id2
	input.close()

	input=open('enzyme_name.txt','r')
	for line in input.readlines():
		list = string.split(line, '\t')
		if len(list) > 1:
			id1 = string.strip(list[0])
			id2 = string.strip(list[1])
			enzyme_name_list[id1] = id2
	input.close()

	input=open('reaction_list.txt','r')
	for line in input.readlines():
		list = string.split(line)
		if len(list) > 1:
			id1 = string.strip(list[0])
			enzymes = []
			count = 1
			for L in list:
				if count > 1:
					enzymes.append(L)
				count += 1
			reaction_list[id1] = enzymes
	input.close()

def get_dirinfo():
	find_dir = 0

	output_path = ''

	for f in os.listdir('./'):
		if f == path_name:
			find_dir = 1
			break
	if find_dir == 0:	
		os.mkdir(path_name)

	opath = './'+path_name+'/'

	return opath


def load_pathways(filename):

	output_path = get_dirinfo()

	input=open(filename,'r')
	file_count = 0
	pid = ''
	edge_count = 0

	rec_count = 0

	rec_list = {}
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

		if line[:2] == '//':
			ofile = pid
			file_count += 1

			ofile = string.replace(ofile, '/', '_')
			ofile = output_path + ofile
			output=open(ofile,'w')

			print pid
			#print 'PREDE:', rec_list
			#print 'DIREC:', direction_list

			for i in range(len(rec_list)):
				rec_id = ''
				for rec in rec_list:
					c = rec_list[rec]
					if c == i+1:
						rec_id = rec
						break

				#print i+1, rec_id

				reaction_enzyme = ''
				left_right = ''		
				
				if left_right_list.has_key(rec_id) == 1:
					if direction_list[rec_id] == 'R2L':
						RL = string.split(left_right_list[rec_id], '=')
						left_right = string.strip(RL[1]) + ' = ' + string.strip(RL[0])
						#print left_right
					else:
						left_right = left_right_list[rec_id]

				else:
					if direction_list[rec_id] == 'NIL':
						rec_id = string.replace(rec_id, '/', '_')
						output.write(rec_id)
						output.write('\n')
				
				enz_list = []
				if reaction_list.has_key(rec_id) == 1:
					enz_list = reaction_list[rec_id]

				gene_list = []
				enz_name_list ={}
				g_list_check = {}
				enz_count = 1
				if len(enz_list) > 0: 
					genes = ''
					protein = ''
					for E in enz_list:
						if enzyme_list.has_key(E) == 1:
							protein = enzyme_list[E]
						if len(protein) > 0:
							if protein_list.has_key(protein) == 1:
								genes = protein_list[protein]
						if len(genes) > 0:
							g_list = string.split(genes)
							for G in g_list:
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

				if len(left_right) > 0:
					
					#print enz_name_list 
					max_value = 0
					for enz in enz_name_list:
						value = enz_name_list[enz]
						if value > max_value:
							max_value = value
							reaction_enzyme = enz

					#print pid, '\t', reaction_enzyme, '\t', left_right, '\t', gene_list 	

					pid = string.replace(pid, '/', '_')
					output.write(pid)
					output.write('\t')
					output.write(reaction_enzyme)
					output.write('\t')
					output.write(left_right)
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
			edge_count = 0
			rec_count = 0	
			rec_list = {}
			direction_list = {}


	#print 'PREDE:', rec_list
	input.close()
	#print 'The number of fils: ', file_count

if ifile1 == '':
	print 'Input pathway file!'
	sys.exit()

if path_name == '':
	print 'Input path name!'
	sys.exit()

if __name__ == '__main__':
	load_datasets()
	load_pathways(ifile1)
