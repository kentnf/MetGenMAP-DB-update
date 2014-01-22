#!/usr/bin/python

import sys, os, string, re

prefix = ''

if os.name != 'posix':
	path_name = sys.argv[1]
	prefix = path_name+'\\python '
else:	
	prefix = './'

#1
print 'Creat enzyme ID - enzyme list.....' 

command = prefix+'py_ext_enzymes.py enzrxns.dat > enzyme_list.txt'

print command
print
print
os.system(command)

#2
print 'Creat reaction ID - enzyme IDs list.....' 
command = prefix+'py_ext_reactions.py reactions.dat reaction_list.txt'
print command
print	
print
os.system(command)

#3
print 'Creat enzyme - genes list.....'
command = prefix+'py_ext_proteins.py  genes.dat proteins.dat protein_list.txt'
print command
print	
print
os.system(command)

#4
print 'Creat enzyme ID - name list.....' 
command = prefix+'py_ext_enzyme_name.py enzrxns.dat > enzyme_name.txt'
print command
print	
print
os.system(command)

#5
print 'Creat compound ID - name list.....' 
command = prefix+'py_ext_compounds_classes.py compounds.dat classes.dat > compound_class_list.txt'
print command
print	
print
os.system(command)

#6
print 'Creat reaction ID - equation list.....'
command = prefix+'py_ext_reaction_equ.py reactions.dat'
print command
print	
print
os.system(command)

#7 
print 'Creat pathways.....'
command = prefix+'py_ext_pathway_entry.py pathways.dat result'
print command
print	
print
os.system(command)

#8
print
print	
print 'Include subpathways.....'
command = prefix+'py_int_pathways.py result pathway_inputs'
print command
print	
print
os.system(command)


