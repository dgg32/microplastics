#split_fasta

import sys, os

file = sys.argv[1]
size = sys.argv[2]

subs = {"M":"000000", "m":"000000", "k":"000", "K":"000"}

for sub in subs:
    size = size.replace(sub, subs[sub])
    

size = int(size)

content = ""
file_counter = 0
#print os.getcwd()
for line in open(file, 'r'):
    if line.startswith(">"):
        if len(content) > size:
            filename =    file + "_" + str(file_counter)
            output = open(filename, 'w')
            output.write(content)
            
            content = ""
            file_counter += 1
        content += line
    else:
        content += line
        




filename =  file + "_" + str(file_counter)
output = open(filename, 'w')
output.write(content)