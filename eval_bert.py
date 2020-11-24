# coding=utf-8
import argparse
import sys
import torch

from pytorch_pretrained_bert import BertForMaskedLM,tokenization


parser = argparse.ArgumentParser(description='Multilingual BERT Evaluation')

parser.add_argument('--data', type=str, default='./data/prep_anim.txt',
                    help='location of data for evaluation')
args = parser.parse_args()


# Use multilingual model
model_name = 'bert-base-multilingual-cased'
print("using model:",model_name,file=sys.stderr)

bert=BertForMaskedLM.from_pretrained(model_name)
tokenizer = tokenization.BertTokenizer.from_pretrained(model_name, do_lower_case=False)
bert.eval()


#UGH https://www.aclweb.org/anthology/W19-4825.pdf
def look_at_confusion():
    pass

def get_target_logprob(target_tokens, pre, post):
  ## Sequentially generate log probability of target.
  ##  ex: target is two tokens, t1 & t2
  ##        product of (or sum of logs of):
  ##           prob t1 given w0 [MASK] [MASK] w3
  ##           prob t2 given w0 t1 [MASK] w3

  target_ids = tokenizer.convert_tokens_to_ids(target_tokens)
  target_len = len(target_tokens)

  tokens = ['[CLS]'] + tokenizer.tokenize(pre)
  target_index = len(tokens)
  tokens += ['[MASK]']*target_len + tokenizer.tokenize(post) + ['[SEP]']

  logprob = 0
  for i in range(target_len):
    input_ids=tokenizer.convert_tokens_to_ids(tokens)
    sentence_tensor = torch.tensor([input_ids])

    with torch.no_grad():
      predictions = bert(sentence_tensor)
      softmaxed = torch.nn.functional.softmax(predictions, dim=2)

    prob_word = softmaxed[0, target_index, target_ids[i]]
    logprob += prob_word.log().item()

    # update mask with word for next prediction
    tokens[target_index] = target_tokens[i]
    target_index += 1
  
  return logprob
  
def get_probs_for_words(sent, w1, w2):
    pre, target, post = sent.split('***')

    if 'mask' in target.lower():
        target=['[MASK]']
    else:
        print("target not mask??",sent,file=sys.stderr)
        target=tokenizer.tokenize(target)
    
    w1_tokens = tokenizer.tokenize(w1)
    w2_tokens = tokenizer.tokenize(w2)

    if len(w1_tokens) != len(w2_tokens):
        print("token length mismatch:", w1, w2,file=sys.stderr)
        return None

    # not super efficient, but makes sense
    logprob1 = get_target_logprob(w1_tokens, pre, post)
    logprob2 = get_target_logprob(w2_tokens, pre, post)

    # sanity check
    if len(w1_tokens) == 1:
        tokens=['[CLS]']+tokenizer.tokenize(pre)
        target_idx=len(tokens)
        tokens+=target+tokenizer.tokenize(post)+['[SEP]']
        input_ids=tokenizer.convert_tokens_to_ids(tokens)

        word_ids=tokenizer.convert_tokens_to_ids([w1,w2])
        tens=torch.LongTensor(input_ids).unsqueeze(0)
        res=bert(tens)[0,target_idx]
        scores = res[word_ids]

        if scores[0] > scores[1] and logprob1 < logprob2:
            print("FUCKMEUP", file=sys.stderr)
        return [float(x) for x in scores]

    return [logprob1, logprob2]

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

        # should only have difference in one word (i.e. the verb)
        diffs = [i for i,pair in enumerate(zip(g,ug)) if pair[0]!=pair[1]]
        assert(len(diffs)==1),diffs 

        grammatical_answer   = g[diffs[0]]   # good
        ungrammatical_answer = ug[diffs[0]]  # bad

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

