import itertools
import numpy as np
import seaborn as sns; sns.set(style="white", color_codes=True)
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import argparse



parser = argparse.ArgumentParser(description='Multilingual BERT Evaluation Analysis')

parser.add_argument('--data', type=str, default='./results/bert_guesses.txt',
                    help='location of data for analysis')
parser.add_argument('--numbers', action='store_true',
                    help='show me NUMBERS!')
parser.add_argument('--lang1', type=str, default='en',
					help='first language')
parser.add_argument('--lang2', type=str, default='fr',
					help='second language')
parser.add_argument('--lang3', type=str, default='ru',
					help='third language')
parser.add_argument('--output_dir', type=str, default='./results/',
                    help='place to dump graphs')
parser.add_argument('--bigboy', action='store_true',
                    help='plot bigboy, with all data')
parser.add_argument('--attractoragreement', action='store_true',
                    help='plot graph assuming correct means agreeing with attractor')
parser.add_argument('--onlyfirst', action='store_true',
                    help='plot only first language verb data')
parser.add_argument('--onlysecond', action='store_true',
                    help='plot only second language verb data')
parser.add_argument('--onlythird', action='store_true',
                    help='plot only second language verb data')
args = parser.parse_args()

def do_numbers(df):
	print(df)


verbs = [{'en_s': 'has flowers', 'en_p': 'have flowers', 'fr_s': 'a des fleurs', 'fr_p': 'ont des fleurs',	'ru_s': 'похотел цветы', 'ru_p': 'похотели цветы'}, 
         {'en_s': 'talks',       'en_p': 'talk', 		 'fr_s': 'va parler', 	 'fr_p': 'vont parler',   	'ru_s': 'говорит', 		 'ru_p': 'говорят'}, 
         {'en_s': 'is waiting',  'en_p': 'are waiting',  'fr_s': 'attends',      'fr_p': 'attendent', 	  	'ru_s': 'будет ждать',	 'ru_p': 'будут ждать'}, 
         {'en_s': 'exists',      'en_p': 'exist', 		 'fr_s': 'existe', 		 'fr_p': 'existent', 	  	'ru_s': 'существует', 	 'ru_p': 'существуют'}, 
         {'en_s': 'is',          'en_p': 'are', 		 'fr_s': 'est', 		 'fr_p': 'sont', 	      	'ru_s': 'жил',			 'ru_p': 'жили'}, 
         {'en_s': 'carries',     'en_p': 'carry', 		 'fr_s': 'porte', 		 'fr_p': 'portent', 	  	'ru_s': 'носил',			'ru_p': 'носили'}, 
         {'en_s': 'wants to eat','en_p': 'want to eat',  'fr_s': 'a voulu manger', 'fr_p': 'ont voulu manger', 'ru_s': 'хочет кушать',	'ru_p': 'хотят кушать'},
         {'en_s': 'goes', 		 'en_p': 'go', 		 	 'fr_s': 'va', 			 'fr_p': 'vont',		  	'ru_s': 'ездит',			'ru_p': 'ездят'}]
inv_verbs = {}
for verb in verbs:
	name = verb['en_p'].split()[0]
	for v in verb:
		inv_verbs[verb[v].split()[0]] = name

# print(inv_verbs)

def load_data_into_df(filename, lang1, lang2, lang3):
	lines = open(args.data, 'r').readlines()

	counts = {}
	sents = {}
	throw_outs = {}

	lcodes = {0: 'en', 1: 'fr', 2: 'ru'}
	gcodes = {0: '_s', 1: '_p'}

	lcombos = list(itertools.product([0, 1, 2], repeat=3))
	gcombos = list(itertools.product([0, 1], repeat=2))

	for lc in lcombos:
		for gc in gcombos:
			tag = lcodes[lc[0]]+gcodes[gc[0]] + "--" + lcodes[lc[1]]+gcodes[gc[1]] + "--" + lcodes[lc[2]]
			
			counts[tag] = []
			sents[tag] = []
			throw_outs[tag] = []


	count = 0
	verbs = {}
	for line in lines:
		# ugh fix this
		if "going ahead" in line: 
			print("JDSKLFJSDF")
			continue 


		
		spl = line.split()
		if spl[0] == "None":  # issue with tokens, BERT as LM. skip example
			throw_outs[tag].append(" ".join(spl))
			continue

		good = 1 if spl[0] == "True" else 0
		tag = spl[2]

		# counts[tag].append((inv_verbs[spl[3]], good)) # (1 + int(count / (3**3 * 4))

		counts[tag].append((1 + int(count / (3**3 * 4)), good)) # (1 + int(count / (3**3 * 4))

		sents[tag].append(" ".join(spl))

		count += 1

	print(len(lines)/64, len(lines))


	dic = {'SubjAttractor': [],'SentIds': [], 'Langs': [], 'Accuracies': []}
	ll = {lang1: lang1[0].upper(), lang2:lang2[0].upper(), lang3:lang3[0].upper(), 's':"S", 'p':"P"}
	for m in counts:
		sa_tag = ll[m[3:4]] + ll[m[9:10]]
		l_tag = ll[m[0:2]] + ll[m[6:8]] + ll[m[12:14]] 

		for xx in counts[m]:
			id = xx[0]
			x = xx[1]

			dic['SubjAttractor'].append(sa_tag)
			dic['Langs'].append(l_tag)

			dic['Accuracies'].append(x)
			dic['SentIds'].append(id)

	df = pd.DataFrame(dic)
	return df


# df = load_data_into_df(args.data, args.lang1, args.lang2, args.lang3)
# input(df)
# df.to_csv('results/cached_df_alt.csv')
df = pd.read_csv('results/cached_df.csv')
# input()# print(df)

# if args.numbers:
# 	do_numbers(df)



# print(df.columns)
# df["match"] = df.SubjAttractor.str[0] == df.SubjAttractor.str[1]
# # df = df[~df.mismatch]
# df["Vlang"] = df.Langs.str[2]
# df["SVsame"] = df.Langs.str[0] == df.Langs.str[2]
# df = df[df.Vlang == "F"]
# df["AVsame"] = df.Langs.str[1] == df.Langs.str[2]
# df["svmatch"] =  df.SVsame.astype(int)*.5 + df.match.astype(int)
# df = df.groupby(['Langs','Vlang']).mean().reset_index()
# print(df.sort_values("Accuracies"))
# print(df)
# input()


# fig, ax = plt.subplots(figsize=(15, 8))
# sns.barplot(data=df.reset_index(), x="svmatch", y="Accuracies",
#             hue="Vlang", ax=ax, ci=None)
# plt.title("Only {}".format(args.lang1))
# plt.savefig(args.output_dir+'svmatchcombo.png')

# input()




if args.bigboy:
	# big boy
	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Big Boy")
	plt.savefig(args.output_dir+'bigboy.png')

if args.attractoragreement:
	# pretend accuracy is agreeing with attractor
	def agrees_with_attractor(name, accuracy):
		agrees = []
		for i in range(len(name)):
			a = accuracy[i]
			n = name[i]

			agree = a if n in ["SS", "PP"] else (a+1)%2
			agrees.append(agree)
		return agrees
		
	df["AttractorAgreementAccuracy"] = agrees_with_attractor(df.SubjAttractor, df.Accuracies)

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df.reset_index(), x="SubjAttractor", y="AttractorAgreementAccuracy",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Agrees with Attractor")
	plt.savefig(args.output_dir+'attractor_agreement.png')

if args.onlyfirst:
	args.lang1 = "R"
	# only first verb
	df_en = df[df.Langs.str[-1] == "R"]#[df.Langs.str[-1] == args.lang1[0].upper()]

	# fig, ax = plt.subplots(figsize=(15, 8))
	# sns.barplot(data=df_en.reset_index(), x="SubjAttractor", y="Accuracies",
	#             hue="Langs", ax=ax, ci=None)
	# plt.title("Only {}".format(args.lang1))
	# plt.savefig(args.output_dir+args.lang1+'_agreement.png')

	convert = {"EEE": "AAA", "FFF": "AAA", "RRR": "AAA",
			   "ERE": "ABA", "EFE": "ABA", "FEF": "ABA", "FRF": "ABA", "RER": "ABA", "RFR": "ABA",
			   "RRE": "BBA", "FFE": "BBA", "EEF": "BBA", "RRF": "BBA", "EER": "BBA", "FFR": "BBA",
			   "ERR": "ABB", "EFF": "ABB", "FEE": "ABB", "FRR": "ABB", "REE": "ABB", "RFF": "ABB",
			   "ERF": "ABC", "EFR": "ABC", "FER": "ABC", "FRE": "ABC", "REF": "ABC", "RFE": "ABC"}

	# df_en["Langs"] = df_en['Langs'].apply(lambda x: convert[x])
	df_en = df_en.groupby(['SubjAttractor','Langs']).mean().reset_index()

	ss = df_en[df_en.SubjAttractor == "SS"].loc[:,['Langs', 'Accuracies']].reset_index()
	sp = df_en[df_en.SubjAttractor == "SP"].loc[:, ['Langs', 'Accuracies']].reset_index()

	ss['diff'] = ss.Accuracies - sp.Accuracies
	ss['SubjAttractor'] = "SS"

	pp = df_en[df_en.SubjAttractor == "PP"].loc[:,['Langs', 'Accuracies']].reset_index()
	ps = df_en[df_en.SubjAttractor == "PS"].loc[:, ['Langs', 'Accuracies']].reset_index()

	pp['diff'] = pp.Accuracies - ps.Accuracies
	pp['SubjAttractor'] = "PP"

	al = ss.append(pp)
	print(al.sort_values("Accuracies"))
	# return
	print(al.sort_values("diff"))
	input()
	df["VerbLang"] = df.Langs.str[-1]
	df["Monolingual"] = df.Langs.isin(['EEE', "RRR", 'FFF'])


	df = df.groupby(['SubjAttractor', 'VerbLang', "Monolingual"]).mean().reset_index()
	print(df)
	# input()


	df["Hue"] = df.VerbLang.astype(str) + df.Monolingual.astype(str)

	print(df)

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Hue", ax=ax, ci=None)
	plt.title("Only {}".format(args.lang1))
	plt.savefig(args.output_dir+'agreement_monoling_sep_all.png')
	input()

if args.onlysecond:
	# only second verb
	df_fr = df[df.Langs.str[-1] == args.lang2[0].upper()]

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df_fr.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Only {}".format(args.lang2))
	plt.savefig(args.output_dir+args.lang2+'_agreement.png')

if args.onlythird:
	# only third verb
	df_fr = df[df.Langs.str[-1] == args.lang3[0].upper()]

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df_fr.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Only {}".format(args.lang3))
	plt.savefig(args.output_dir+args.lang3+'_agreement.png')

