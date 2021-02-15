import sys, re
from Bio import SeqIO

diamond_file = sys.argv[1]
fasta_file = sys.argv[2]

rx_hitname = re.compile(r'gi\|\d+\|\w+?\|\S+?\|(\S+?)\[(\S+?)\]')

previous_contig = ""


left_item = SeqIO.parse(fasta_file, "fasta")

for line in open(diamond_file, 'r'):
	line = line.strip()
	fields = line.split("\t")
	#print (fields)

	contig_name = fields[0]
	evalue = float(fields[-2])

	if contig_name != previous_contig:
		previous_contig = contig_name

		if evalue <= 1e-10:
			#print ("hello")
			match_hit = rx_hitname.match(fields[1])

			if match_hit:
				annotation = match_hit.group(1).replace("_", " ").strip()
				taxon = match_hit.group(2).replace("_", " ").strip()


				try:
					found = False
					while found == False:
						item = next(left_item)

						description = item.description

						item_contig_name = description.split(" ")[0]

						if item_contig_name == contig_name:
							found = True

							print (">" + contig_name + "|" + annotation + "|" + taxon + "\n" + item.seq[:-1] + "\n")
				except StopIteration:
					pass


