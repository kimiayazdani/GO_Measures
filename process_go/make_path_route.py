import pickle
import os

# -------------------------------------------------------------------------------------------


def go_trace(g, g1, data_dict, go_hierarchy):
    if g1 != g:
        data_dict[g].append(g1)
    if g1 not in go_hierarchy:
        return
    for p in go_hierarchy[g1]:
        go_trace(g, p, data_dict,go_hierarchy)

def go_trace_path_to_root(force=False):
    if not force and os.path.exists('alignments/data/go_trace'):
        print("The file already exists. @go_trace_path_to_root")
        return 

    go_hierarchy = pickle.load(open(os.path.join("alignments/data/go_hierarchy"),"rb"))

    data_dict = {}

    counter = 0

    for g in go_hierarchy.keys():
        data_dict[g] = []
        for g1 in go_hierarchy[g]:
            go_trace(g,g1,data_dict,go_hierarchy)
        counter += 1
        print(counter, g, "is done")

    with open('alignments/data/go_trace', "wb") as f:
        pickle.dump(data_dict, f)

    print("go trace done.")

# -------------------------------------------------------------------------------------------


def create_go_struct(force=False):
    if not force and os.path.exists('alignments/data/go_hierarchy'):
        print("The file already exists. @create_go_struct")
        return


    counter = 0
    data_dict = {}
    go = '1'

    with open('alignments/data/go.obo', 'r') as f:
        all = f.readlines()

    while True:
        if all[counter] == '\n':
            temp = all[counter + 2].split()[1]
            if temp[3:].isnumeric():
                go = temp
                counter += 1
                path_route = set()

                
                flag=False

                if counter >= len(all):
                    break

                while all[counter] != '\n':
                    if counter >= len(all):
                        break

                    temp = all[counter].split()
                    if temp[0] == 'is_obsolete:' and temp[1] == 'true':
                        flag=True
                    if temp[0] == 'is_a:':
                        path_route.add(temp[1])
                    counter += 1
                if not flag and len(path_route):
                    data_dict[go] = path_route
            else:
                if temp == 'ends_during':
                    counter = len(all)
                    break
        else:
            counter += 1


        if counter >= len(all):
            break
    

    with open('alignments/data/go_hierarchy', "wb") as f:
        pickle.dump(data_dict, f)

    print(len(data_dict), "length of dictionary. go create struct done.")



if __name__ == "__main__":
    print("USAGE: assumes there is subdirectory called alignments/data that contains go.obo file and also creates the output in the same directory. The output has two files: one is go_hierarchy and one is go_trace")
    create_go_struct()
    go_trace_path_to_root()
