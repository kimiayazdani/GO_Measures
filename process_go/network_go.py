import pickle 
import os 

def network_pgo(tax_id, force=False):
    tax_id = str(tax_id)
    path = os.path.join(f"alignments/data/{tax_id}_pgo".format(tax_id=tax_id))
    if not force and os.path.exists(path):
        print("The file already exists. @network_pgo -", tax_id)
        return 

    go_trace = pickle.load(open(os.path.join("alignments/data/go_trace"),"rb"))

    pgo_dict = {}
    with open('alignments/data/gene2go.allGO', 'r') as f:
        lines = f.readlines()


    with open('alignments/data/'+tax_id+'prs', 'r') as f:
        prs = list(map(lambda x: x[:-1], f.readlines()))


    for l in lines[1:]:
        fields = l.split()
        if len(fields) < 3:
            continue
        if fields[0] == tax_id:
            if fields[1] not in prs:
                continue
            if fields[1] not in pgo_dict:
                pgo_dict[fields[1]] = set()
            pgo_dict[fields[1]].add(fields[2])
            if fields[2] in go_trace:
                pgo_dict[fields[1]].update(go_trace[fields[2]])


    with open(path, "wb") as f:
        pickle.dump(pgo_dict, f)

    print("network pgo generated for", tax_id)

            

def network_lambda(tax_id, force=False):
    tax_id=str(tax_id)
    path = os.path.join(f"alignments/data/{tax_id}_golambda".format(tax_id=tax_id))
    if not force and os.path.exists(path):
        print("The file already exists. @network_lambda -", tax_id)
        return
        

    pgo = pickle.load(open(os.path.join(f"alignments/data/{tax_id}_pgo".format(tax_id=tax_id)),"rb"))


    g_lambda = {}
    for _,val in pgo.items():
        for g in val:
            if g not in g_lambda:
                g_lambda[g] = 0
            g_lambda[g]+=1
    
    with open(path, "wb") as f:
        pickle.dump(g_lambda, f)

    print("network lambda generated for", tax_id)




def process_network(tax_id, force=True):
    network_pgo(tax_id,force)
    network_lambda(tax_id,force)


if __name__ == "__main__":
        if (len(sys.argv) < 2):
        print("USAGE: takes an argument tax_id, creates pgo and golambda file in the alignment/data directory. Assumes make_path_route is run before this.")
        exit(1)
    process_network(int(sys.argv[1]))
