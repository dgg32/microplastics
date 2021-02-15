import pyphy
import re
import sys
from threading import Thread
import queue

from bs4 import BeautifulSoup

from threading import Semaphore

dictLock = Semaphore(value=1)
writeLock = Semaphore(value=1)

diamond_input_file = sys.argv[1]

desired_ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]

rx_taxon = re.compile(r'\[(\S+?)\]')


taxon_content = {}

in_queue = queue.Queue()


def work ():
    while True:
        content = in_queue.get()
        nonsense = True
        
        #print ("initial", content)
        for line in content.split("\n"):
            fields = line.split("\t")
            temp_content = ["-1"] * 7
            if nonsense == True:
                search_taxon = rx_taxon.search(line)
                
                if search_taxon:
                    taxon = search_taxon.group(1).replace("_", " ")

                    

                    if "sp." in taxon:
                        taxon = taxon.split("sp.")[0] + "sp. " + taxon.split("sp.")[1].strip().replace(" ", "_")

                    if taxon not in taxon_content:

                        taxid = pyphy.getTaxidByName(taxon)[0]

                        path = pyphy.getPathByTaxid(taxid)

                        
                        for item in path:
                            rank = pyphy.getRankByTaxid(item)

                            if rank in desired_ranks:
                                index = desired_ranks.index(rank)

                                temp_content[index] = pyphy.getNameByTaxid(item)
                        

                        dictLock.acquire()
                        taxon_content[taxon] = temp_content
                        dictLock.release()



                    else:
                        temp_content = taxon_content[taxon]

                if temp_content.count("-1") < 7:
                    nonsense = False 
            
                    writeLock.acquire()
                    #print ()
                    print (fields[0] + "\t" + "\t".join(temp_content))
                    writeLock.release()

        in_queue.task_done()

for i in range(10):
    t = Thread(target=work)
    t.daemon = True
    t.start()


previous = ""
content = ""

for line in open(diamond_input_file, 'r'):
    

    fields = line.split("\t")

    
    if fields[0] != previous:
        

        previous = fields[0]
        
        if content != "":
            #print (fields[0])
            in_queue.put(content)
        content = line
    else:
        content += line


in_queue.put(content)

            



in_queue.join()