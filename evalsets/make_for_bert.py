import os
# from pytorch_pretrained_bert import tokenization

# # first ensure that all tokens are in BERT's vocabulary
# model_name = 'bert-base-multilingual-cased'
# tokenizer=tokenization.BertTokenizer.from_pretrained(model_name, do_lower_case=False)
# s = "je veux parler. voici la jupe que j'aime"


# tokenizer.tokenize()
# input_ids=tokenizer.convert_tokens_to_ids(tokens)


for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        case = filename.split('.txt')[0]
        with open(filename, 'r') as infile:
            g = ""
            ug = ""
            for line in infile:
                line_tuple = line.strip().split('\t')
                if line_tuple[0] == "True":
                    is_grammatical = True
                else:
                    is_grammatical = False

                tag = line_tuple[1]
                sentence = line_tuple[2]

                if is_grammatical:
                    g = sentence
                else:
                    ug = sentence
                    print(case+'\t'+tag+'\t'+g+'\t'+ug)
