import itertools
import numpy as np
import seaborn as sns; sns.set(style="white", color_codes=True)
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import argparse



parser = argparse.ArgumentParser(description='Multilingual BERT Evaluation Analysis')

parser.add_argument('--data', type=str, default='./results/bertevaldata.txt',
                    help='location of data for analysis')
parser.add_argument('--output_dir', type=str, default='./results/',
                    help='place to dump graphs')
parser.add_argument('--bigboy', action='store_true',
                    help='plot bigboy, with all data')
parser.add_argument('--attractoragreement', action='store_true',
                    help='plot graph assuming correct means agreeing with attractor')
parser.add_argument('--onlyenglish', action='store_true',
                    help='plot only english verb data')
parser.add_argument('--onlyfrench', action='store_true',
                    help='plot only french verb data')
args = parser.parse_args()


def load_data_into_df(filename):
	lines = open(args.data, 'r').readlines()

	counts = {}
	sents = {}
	throw_outs = {}

	lcodes = {0: 'en', 1: 'fr'}
	gcodes = {0: '_s', 1: '_p'}

	lcombos = list(itertools.product([0, 1], repeat=3))
	gcombos = list(itertools.product([0, 1], repeat=2))
	for lc in lcombos:
		for gc in gcombos:
			tag = lcodes[lc[0]]+gcodes[gc[0]] + "--" + lcodes[lc[1]]+gcodes[gc[1]] + "--" + lcodes[lc[2]]
			
			counts[tag] = []
			sents[tag] = []
			throw_outs[tag] = []


	for line in lines:
		# ugh fix this
		if "going ahead" in line: continue 

		spl = line.split()
		if spl[0] == "None":  # issue with tokens, BERT as LM. skip example
			throw_outs[tag].append(" ".join(spl))
			continue

		good = 1 if spl[0] == "True" else 0
		tag = spl[2]

		counts[tag].append(good)
		sents[tag].append(" ".join(spl))

	print(len(lines)/64, len(lines))


	dic = {'SubjAttractor': [],'Langs': [], 'Accuracies': []}
	ll = {'en': "E", 'fr':'F', 's':"S", 'p':"P"}
	for m in counts:
		sa_tag = ll[m[3:4]] + ll[m[9:10]]
		l_tag = ll[m[0:2]] + ll[m[6:8]] + ll[m[12:14]] 

		for x in counts[m]:
			dic['SubjAttractor'].append(sa_tag)
			dic['Langs'].append(l_tag)

			dic['Accuracies'].append(x)

	df = pd.DataFrame(dic)
	return df


df = load_data_into_df(args.data)

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

if args.onlyenglish:
	# only english verb
	df_en = df[df.Langs.str[-1] == "E"]

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df_en.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Only English")
	plt.savefig(args.output_dir+'english_agreement.png')

if args.onlyfrench:
	# only french verb
	df_fr = df[df.Langs.str[-1] == "F"]

	fig, ax = plt.subplots(figsize=(15, 8))
	sns.barplot(data=df_fr.reset_index(), x="SubjAttractor", y="Accuracies",
	            hue="Langs", ax=ax, ci=None)
	plt.title("Only French")
	plt.savefig(args.output_dir+'french_agreement.png')


