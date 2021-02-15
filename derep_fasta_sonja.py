import sys
from Bio import SeqIO


fasta_file = sys.argv[1]


sequence_name = {}

for record in SeqIO.parse(fasta_file, 'fasta'):
	sequence = str(record.seq)
	name = str(record.description)

	if sequence not in sequence_name:
		sequence_name[sequence] = set()


	sequence_name[sequence].add(name)





fasta_content = ""
mapping_content = ""

for index, sequence in enumerate(sequence_name):
	fasta_content += ">seq_" + str(index) + "\n" + sequence + "\n"

	mapping_content += "seq_" + str(index) + "\t" + ";".join(sequence_name[sequence]) + "\n"


output_fasta = open(fasta_file.replace(".fasta", "_derep.fasta"), 'w')
output_tsv = open(fasta_file.replace(".fasta", "_derep.tsv"), 'w')

output_fasta.write(fasta_content)
output_fasta.close()

output_tsv.write(mapping_content)
output_tsv.close()