import pickle

m = 3
t = 0

with open(str(m)+"_NAF.pkl", "rb") as file:
    NAF_dict = pickle.load(file)


threshold_values = [6, 4, 2, 0]

predictions_dict = {}


# dictionary pgo multilevel pgo[network_index][pr]


def read_pgos(tids=['7227','9606','10090','10116','4932']):
    pgo = dict()
    for tid in tids:
        with open('./'+tid+'_gop', 'rb') as file:
            pgo[tid] = pickle.load(file)
        
    return pgo



pgo = read_pgos()
net_mapping = ['7227', '9606', '10090', '10116', '4932']
for threshold in threshold_values:
    predictions = {}

    for key, value in NAF_dict.items():
        if value >= threshold:
    
            for network_index, protein_name in key:
                
                
                if network_index == t:
                    continue  # Skip the target network index
                # Retrieve the GO terms associated with the protein from pgo dictionary

                if protein_name not in pgo[net_mapping[network_index]]:
                    # print(protein_name, "skipping")
                    continue

                go_terms = pgo[net_mapping[network_index]][protein_name]
                if protein_name in predictions:
                    predictions[protein_name].update(go_terms)
                else:
                    predictions[protein_name] = go_terms


    # Add the predictions to the secondary dictionary
    predictions_dict[threshold] = predictions


threshold_index = 0
predictions = {}
for key, value in NAF_dict.items():
    
    flag_target_in = False
    temp_predict = []
    for network_index, protein_name in key:
        if network_index == t:
            flag_target_in = True
            continue  

        if protein_name not in pgo[net_mapping[network_index]]:
                # print(protein_name, "skipping")
                continue
        
        go_terms = pgo[net_mapping[network_index]][protein_name]
        
        temp_predict.extend(go_terms)
    if flag_target_in:
        if protein_name not in predictions:
            predictions[protein_name] = go_terms
        else:
            predictions[protein_name].update(go_terms)

    if value >= threshold_values[threshold_index]:
        predictions_dict[threshold_values[threshold_index]] = predictions
    else:
        predictions = {}
        if threshold_values[threshold_index] not in predictions_dict:
            predictions_dict[threshold_values[threshold_index]] = {}
        threshold_index += 1 

# protein name ro az koja miarim dir tar? ? !

# Print the predictions for each threshold value
for threshold, predictions in predictions_dict.items():
    if threshold >1:
        print(f"Threshold {threshold}: {predictions}")
        print()
        print()


# for naf_dict e 

# protein_name = 0
# protein name 





# we should ADD PIP here or even later :: Predictable In Principle 

