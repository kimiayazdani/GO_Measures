#!/bin/bash

print_usage() {
    echo "USAGE: The directory 'alignments/data' must exist and contain the 'go.obo' file. Additionally, it should contain [tax_id].el files with the edge_list of the networks you want to process."
}

if [ ! -d "alignments/data" ] || [ ! -f "alignments/data/go.obo" ]; then
    print_usage
    exit 1
fi

python3 make_path_route.py


for file in *.el; do
    if [ -f "$file" ]; then
        tax_id="${file%.el}"
        awk 'BEGIN{OFS="\n"} {print $1, $2}' $file | sort -u > alignments/data/${tax_id}_prs
        python3 network_go.py "$tax_id"
    fi
done
