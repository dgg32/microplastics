import sys

diamond_result_file = sys.argv[1]

ncbi_file = sys.argv[2]

accession_contig = {}

previous_contig = ""

for line in open(diamond_result_file, 'r'):
	fields = line.strip().split("\t")

	contig_name = fields[0]

	if contig_name != previous_contig:
		previous_contig = contig_name
		accession = fields[1]

		evalue = float(fields[-2])

		if evalue <= 1e-20:
			if accession not in accession_contig:
				accession_contig[accession] = []

			accession_contig[accession].append(contig_name)


from Bio import SeqIO

fasta_sequences = SeqIO.parse(open(ncbi_file),'fasta')

for fasta in fasta_sequences:
	name, sequence = fasta.description, str(fasta.seq)

	if name in accession_contig:
		#content = ">" + ";".join(accession_contig[name]) + "\n" + sequence + "\n"
		content = ">" + (accession_contig[name][0]) + "\n" + sequence + "\n"
		print (content)
		del accession_contig[name]

