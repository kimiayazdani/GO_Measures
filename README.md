# GO_Measures
New GO Based Measures for Multiple Network Alignments. It can be used for any type of network alignment when nodes have annotations. The annotations can have their own hierarchial structure like Protein Protein Interaction networks and GO terms. 

## EGS_SGS.py 
This file can be used to calculate Squared GO Score (SGS) or Exposed GO Score (EGS). 
```
./EGS_SGS.py alignment_file base_dir ['SGS'/'EGS'] [tax_ids]
```
base_dir should contain files in format [tax_id]_pgo [tax_id]_golambda

The tax_ids should appear in the same order that they appear in the alignment.
Prints the score as the output.
Example usage:
```
python3 EGS_SGS.py ../alignments/real_alignments/5/0.9/alignment.tsv ../stuff/alignments/data EGS 9606 10090 10196 7227 
```
### Alignment File
Alignment file is a space or tab separated file, with each line containing a cluster of aligned nodes. The first column should contribute to the first tax_id (or Edge List) and so on.
If there is no node for an Edge List in a cluster of aligned node, the file should have a "_" in that space.

### PGO File
The PGO file should contain the mapping from the proteins (nodes) to the GO Terms (annotation). The code reads a binary file that can be generated using the `process_go/process_go.sh` file.

### GOLAMBDA File
golambda file is used for efficiency, it contains the frequency of a GO term (annotaion) in each network. It is generated using the same `process_go/process_go.sh` file.

## process_go/
This directory contains the pre-processing specific to the networks and GO term hierarchy. It requires a subdirectory `alignments/data/...` which includes at least a go.obo file. The go.obo file should contain the hierarchial structure of the GO terms. It has the normal formatting of an obo file. 

The `process_go.sh` first runs `make_path_route.py` that processes the GO terms themselves regardless of the network.
Then for each EdgeList file available in the directory (which is the network, tab/space separated nodes that are connected), it creates the list of proteins ([tax_id]_prs).
Then for every EdgeList file, it creates the `pgo` and `golambda` file used by the main script. 

## predictGOs/
This directory contains files needed to make Edge predictions using the measures. Making changes to the code to work on the specific alignments are needed. It uses Network Alignment Frequency for multiple network alignment based on the `${m}-combination` of the aligned networks appearing in the network alignments created. 

For using the measures, the `EGS_SGS.py` file should be run on the output of the alignments and `Predictable.sh` can be used to find the predictions that were correct based on the correct file.
