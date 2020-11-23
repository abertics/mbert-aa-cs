# coding=utf-8
from pytorch_pretrained_bert import BertForMaskedLM,tokenization
import torch
import argparse
import sys
import csv


parser = argparse.ArgumentParser(description='Multilingual BERT Evaluation')

parser.add_argument('--data', type=str, default='./evalsets/data/forbert.tsv',
                    help='location of data for evaluation')
args = parser.parse_args()

# MODIFIED BY AARON MUELLER
# MODIFICATIONS MODIFIED BY ABBY BERTICS

# Use multilingual model
model_name = 'bert-base-multilingual-cased'
print("using model:",model_name,file=sys.stderr)
bert=BertForMaskedLM.from_pretrained(model_name)
tokenizer=tokenization.BertTokenizer.from_pretrained(model_name, do_lower_case=False)
bert.eval()


#UGH https://www.aclweb.org/anthology/W19-4825.pdf
def look_at_confusion():
    pass

def get_probs_for_words(sent, w1, w2):
    pre, target, post=sent.split('***')

    if 'mask' in target.lower():
        target=['[MASK]']
    else:
        print("target not mask??",sent,file=sys.stderr)
        target=tokenizer.tokenize(target)
        
    tokens = ['[CLS]'] + tokenizer.tokenize(pre)
    target_index = len(tokens)
    tokens += target + tokenizer.tokenize(post) + ['[SEP]']
    input_ids=tokenizer.convert_tokens_to_ids(tokens)
    
    try:
        word_ids=tokenizer.convert_tokens_to_ids([w1,w2])
    except KeyError:
        w1_tokens = tokenizer.tokenize(w1)
        w2_tokens = tokenizer.tokenize(w2)

        if len(w1_tokens) != len(w2_tokens):
            print("token length mismatch:", w1, w2,file=sys.stderr)
            return None

        guess1_ids = tokenizer.convert_tokens_to_ids(w1_tokens)
        guess2_ids = tokenizer.convert_tokens_to_ids(w2_tokens)

        if w1_tokens[0] != w2_tokens[0] or len(w1_tokens) != 2 or len(w2_tokens) != 2 :
            print("first token mismatch:", w1, w2, file=sys.stderr)
            return None


        tokens = ['[CLS]'] + tokenizer.tokenize(pre) + [w1_tokens[0]]
        target_index = len(tokens)
        tokens += target + tokenizer.tokenize(post) + ['[SEP]']
        input_ids=tokenizer.convert_tokens_to_ids(tokens)
        
        # print("skipping",w1,w2,"bad wins")

        # The tricky thing is that words might be split into multiple subwords. 
        # You can simulate that be adding multiple [MASK] tokens, but then you have a 
        # problem of how to reliably compare the scores of prediction so different lengths. 
        # I would probably average the probabilities, but maybe there is a better way.

        # but how do we now get the probability of a multi-token word in a single-token position?

        print("going ahead", w1, w2, w1_tokens[0])
        word_ids = [guess1_ids[1], guess2_ids[1]]

    sentence_tensor = torch.LongTensor(input_ids).unsqueeze(0)
    result = bert(sentence_tensor)[0,target_index]
    scores = result[word_ids]
    return [float(x) for x in scores]

def load_data(data_file):
    out = []
    for line in open(data_file):
        case = line.strip().split("\t") 
        
        # 0: test type, 1: lang_s/p--lang_s/p--lang, 2: gram, 3: ungram
        test_type = case[0]
        lang_combo = case[1]

        g = case[2].split()
        ug = case[3].split()
        assert(len(g)==len(ug)),(g,ug) # sentences must be same length

        # should only have difference in one spot (i.e. the verb)
        diffs = [i for i,pair in enumerate(zip(g,ug)) if pair[0]!=pair[1]]
        assert(len(diffs)==1),diffs 

        grammatical_answer   = g[diffs[0]]   # good
        ungrammatical_answer = ug[diffs[0]] # bad

        # mask it, make it sentence
        g[diffs[0]] = "***mask***"
        g.append(".")

        out.append((test_type, lang_combo, " ".join(g), grammatical_answer, ungrammatical_answer))

    return out

def eval_data(data_file):
    prepped_data = load_data(data_file)
    print(len(prepped_data),file=sys.stderr)

    import time
    start = time.time()
    for i, (test_type, lang_combo, sentence, good_answer, bad_answer) in enumerate(prepped_data):
        probs =  get_probs_for_words(sentence, good_answer, bad_answer)

        if probs is None:
            # ignore cases where token number doesn't align :'(
            print(None, test_type, lang_combo, good_answer, bad_answer, sentence)
            continue

        prob_good, prob_bad = probs[0], probs[1]
        correct_prediction = prob_good>prob_bad

        print(correct_prediction, test_type, lang_combo, good_answer, bad_answer, sentence)
        if i % 100==0:
            print(i, time.time()-start, file=sys.stderr)
            start=time.time()
            sys.stdout.flush()

eval_data(args.data)

