from collections import Counter
from itertools import combinations
import pickle 

def count_m_tuples(m):
    counter = Counter()
    file_base = "/home/wayne/src/bionets/SANA/MBioGRID/multi/3.0.064/openlab-"
    file_ext = "/1000s/24/multiAlign.tsv"

    for i in range(100):
        filename = file_base + '{:02d}'.format(i) + file_ext
        # print(filename)
        with open(filename, "r") as file:
            for line in file:
                proteins = [(i, x) for i, x in enumerate(line.strip().split()) if x != "_" ]
                tuples = combinations(proteins, m)

                for t in tuples:
                    counter[t] += 1 # keeps the count of every combination of proteins across all alignments

    
    sorted_counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}

    return sorted_counter








m = 5
NAFMulti = count_m_tuples(m)
for k, v in NAFMulti.items():
    if v == 1:
        break
    print(f"{k}: {v}")


with open("data/for100/"+str(m)+"_NAF_forSGSNAF.pkl", "wb") as file:
    pickle.dump(NAFMulti, file)
    

