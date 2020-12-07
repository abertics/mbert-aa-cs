# mbert-aa-cs
# Multilingual BERT Evaluation

Assessing patterns of agreement across monolingual and codeswitched data.

Model: https://github.com/google-research/bert/blob/master/multilingual.md

## Dependencies
use python3 pls
pip3 install {pytorch_pretrained_bert, seaborn, pandas}

## Creating the data
### Agreement Attraction with Prep Phrases & Animate Nouns (English, Russian, French)
from mbert-aa-cs:
python3 generate_data.py > data/prep_anim.txt
>> Data will now be in mbert-aa-cs/data/prep_anim.txt

## Making mBERT do the experiment
from mbert-aa-cs:
python3 eval_bert.py --data data/prep_anim.txt > results/enfrru_prep_anim_bert.txt
>> Results will now be in mbert-aa-cs/results


## Analyzing mBERT's predictions 
R code is also located here: https://colab.research.google.com/drive/1t2p3bejrjSH45UPFDMUrXSL4W5MBSRCF?usp=sharing
play around with analyze_results.py
my sincerest apologies for the messiness

