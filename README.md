# mbert-aa-cs
# Multilingual BERT Evaluation

Assessing patterns of agreement across monolingual and codeswitched data.

Model: https://github.com/google-research/bert/blob/master/multilingual.md

## Dependencies
use python3 pls
pip3 install {pytorch_pretrained_bert, seaborn, pandas

## Creating the data
### Agreement Attraction with Prep Phrases & Animate Nouns (English & French)
from mbert-aa-cs/evalsets:
./generate_data.sh
>> Data will now be in mbert-aa-cs/evalsets/data

## Making mBERT do the experiment
from mbert-aa-cs:
./eval_bert.sh
>> Results will now be in mbert-aa-cs/results


## Analyzing mBERT's predictions 
from mbert-aa-cs:
./make_graphs.sh
>> Graphs will now be in mbert-aa-cs/results


