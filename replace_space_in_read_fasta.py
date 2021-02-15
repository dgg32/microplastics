#!/usr/bin/env python


import sys
from Bio import SeqIO

read_file = sys.argv[1]



for record in SeqIO.parse(read_file, 'fasta'):
	print (">" + str(record.description).replace(" ", "_") + "\n" + str(record.seq))









