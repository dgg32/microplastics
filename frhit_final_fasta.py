#!/usr/bin/env python

import sys
from Bio import SeqIO
import os
#import json

frhit_file = sys.argv[1]
total_read_file = sys.argv[2]
contig_file = sys.argv[3]


#only assembled contigs have contig_read info, singletons have only one read


#output_file = contig_file.replace(".fasta", "_total_contig.fasta")

mappable_reads = set()
#contig_read = {}


content = ""


previous_read = ""
previous_evalue = 100
previous_contig = ""
previous_start = 0
previous_stop = 0

for line in open(frhit_file):
	line = line.strip()


	fields = line.split("\t")

	if len(fields) >= 11:
		read = fields[0]
		contig = fields[8]
		start = fields[9]
		stop = fields[10]
		evalue = float(fields[2])

		mappable_reads.add(read)

		if read != previous_read:

			if previous_read != "":

				content += "\t".join([previous_contig, str(previous_start), str(previous_stop)]) + "\n"

			previous_read = read
			previous_evalue = evalue
			previous_contig = contig
			previous_start = start
			previous_stop = stop
		else:
			if evalue < previous_evalue:
				previous_evalue = evalue
				previous_contig = contig
				previous_start = start
				previous_stop = stop
		# if contig not in contig_read:
		# 	contig_read[contig] = []

		# contig_read[contig].append([start, stop])
content += "\t".join([previous_contig, str(previous_start), str(previous_stop)]) + "\n"

with open(contig_file.replace(".fasta", ".tsv"), 'w') as output:
	output.write(content)


content = ""

for record in SeqIO.parse(total_read_file, 'fasta'):
	if record.description not in mappable_reads:
		content += ">" + str(record.id) + "\n" + str(record.seq) + "\n"



with open(contig_file.replace(".fasta", "_singletons.fasta"), 'w') as output:
	output.write(content)


command = "cat " + contig_file + " " + contig_file.replace(".fasta", "_singletons.fasta") + " > " + contig_file.replace(".fasta", "_final.fasta")

os.system(command)



# with open(contig_file.replace(".fasta", ".json"), 'w') as output:
# 	output.write(json.dumps(contig_read, indent = 4))





