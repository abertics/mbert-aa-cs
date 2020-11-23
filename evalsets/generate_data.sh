#!/bin/bash

python3 generate_data.py > data/fren_prep_anim.txt

python3 make_for_bert.py > data/forbert.tsv
