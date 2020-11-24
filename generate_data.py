# coding=utf-8
import sys
import itertools

subjects = [{'en_s': 'the senator', 	'en_p': 'the senators', 	'ru_s': 'сенатор', 		'ru_p': 'сенаторы', 	'fr_s': 'le sénateur', 		'fr_p': 'les sénateurs'},
	        {'en_s': 'the author', 		'en_p': 'the authors', 		'ru_s': 'автор', 		'ru_p': 'авторы', 		'fr_s': 'l\'auteur', 		'fr_p': 'les auteurs'}, 
	        {'en_s': 'the pilot', 		'en_p': 'the pilots', 		'ru_s': 'пилот', 		'ru_p': 'пилоты', 		'fr_s': 'le pilote', 		'fr_p': 'les pilotes'}, 
	        {'en_s': 'the surgeon', 	'en_p': 'the surgeons', 	'ru_s': 'хирург', 	    'ru_p': 'хирурги', 		'fr_s': 'le chirugien', 	'fr_p': 'les chirugiens'}, 
	        {'en_s': 'the customer', 	'en_p': 'the customers', 	'ru_s': 'клиент', 		'ru_p': 'клиенты', 		'fr_s': 'le client', 		'fr_p': 'les clients'}, 
	        {'en_s': 'the consultant', 	'en_p': 'the consultants', 	'ru_s': 'консультант', 	'ru_p': 'консультанты', 'fr_s': 'le consultant', 	'fr_p': 'les consultants'}, 
	        {'en_s': 'the manager', 	'en_p': 'the managers', 	'ru_s': 'менеджер',     'ru_p': 'менеджеры', 	'fr_s': 'l\'homme', 		'fr_p': 'les hommes'}, 
	        {'en_s': 'the officer', 	'en_p': 'the officers', 	'ru_s': 'офицер', 		'ru_p': 'офицеры', 		'fr_s': 'l\'officier', 		'fr_p': 'les officiers'},
	        {'en_s': 'the farmer', 		'en_p': 'the farmers', 		'ru_s': 'фермер', 	    'ru_p': 'фермеры', 		'fr_s': 'l\'agriculteur', 	'fr_p': 'les agriculteurs'}, 
	        {'en_s': 'the teacher',	 	'en_p': 'the teachers', 	'ru_s': 'профессор', 	'ru_p': 'профессорa', 	'fr_s': 'l\'enseignant', 	'fr_p': 'les enseignants'}]

preps = [{'en': 'near', 	  'fr': 'près de', 		'ru': 'рядом с'}, 
		 {'en': 'around',     'fr': 'autour de',   	'ru': 'около'},
		 {'en': 'across from','fr': 'en face de',  	'ru': 'напротив'},
	     {'en': 'in front of','fr': 'devant', 		'ru': 'перед'},
	     {'en': 'behind', 	  'fr': 'derrière', 	'ru': 'за'},
  		 {'en': 'among', 	  'fr': 'parmi', 		'ru': 'посреди'}]

attractors = [{'en_s': 'the guard', 		'en_p': 'the guards', 		'ru_s': 'охранник', 	'ru_p': 'охранник',   'fr_s': 'le garde', 	  'fr_p': 'les gardes'},
         	  {'en_s': 'the chef', 			'en_p': 'the chefs', 		'ru_s': 'повар', 		'ru_p': 'повар', 	  'fr_s': 'le chef', 	  'fr_p': 'les chefs'}, 
         	  {'en_s': 'the skater', 		'en_p': 'the skaters', 		'ru_s': 'фигуристка', 	'ru_p': 'фигуристка', 'fr_s': 'le patineur',  'fr_p': 'les patineurs'}, 
              {'en_s': 'the taxi driver', 	'en_p': 'the taxi drivers', 'ru_s': 'таксист', 		'ru_p': 'таксист', 	  'fr_s': 'le chauffeur', 'fr_p': 'les chauffeurs'}, 
              {'en_s': 'the theif', 		'en_p': 'the theives', 		'ru_s': 'вор', 	     	'ru_p': 'вор', 		  'fr_s': 'le voleur', 	  'fr_p': 'les voleurs'}, 
              {'en_s': 'the child', 		'en_p': 'the children', 	'ru_s': 'ребёнок', 		'ru_p': 'ребёнок',    'fr_s': 'l\'enfant', 	  'fr_p': 'les enfants'}]

verbs = [{'en_s': 'has flowers', 'en_p': 'have flowers', 'fr_s': 'a des fleurs', 'fr_p': 'ont des fleurs',	'ru_s': 'похотел цветы', 'ru_p': 'похотели цветы'}, 
         {'en_s': 'talks',       'en_p': 'talk', 		 'fr_s': 'va parler', 	 'fr_p': 'vont parler',   	'ru_s': 'говорит', 		 'ru_p': 'говорят'}, 
         {'en_s': 'is waiting',  'en_p': 'are waiting',  'fr_s': 'attends',      'fr_p': 'attendent', 	  	'ru_s': 'будет ждать',	 'ru_p': 'будут ждать'}, 
         {'en_s': 'exists',      'en_p': 'exist', 		 'fr_s': 'existe', 		 'fr_p': 'existent', 	  	'ru_s': 'существует', 	 'ru_p': 'существуют'}, 
         {'en_s': 'is',          'en_p': 'are', 		 'fr_s': 'est', 		 'fr_p': 'sont', 	      	'ru_s': 'жил',			 'ru_p': 'жили'}, 
         {'en_s': 'carries',     'en_p': 'carry', 		 'fr_s': 'porte', 		 'fr_p': 'portent', 	  	'ru_s': 'носил',			'ru_p': 'носили'}, 
         {'en_s': 'wants to eat','en_p': 'want to eat',  'fr_s': 'a voulu manger', 'fr_p': 'ont voulu manger', 'ru_s': 'хочет кушать',	'ru_p': 'хотят кушать'},
         {'en_s': 'goes', 		 'en_p': 'go', 		 	 'fr_s': 'va', 			 'fr_p': 'vont',		  	'ru_s': 'ездит',			'ru_p': 'ездят'}]

russian_cases = {'рядом с': 'inst', 'около': 'gen', 'напротив': 'gen', 'перед': 'inst', 'за': 'inst', 'посреди': 'gen'}
declined = {'gen': {'охранник':   ['охранника', 'охранников'],
					'повар': 	  ['повара', 'поваров'],
					'фигуристка': ['фигуристки', 'фигуристок'],
					'таксист':    ['таксиста', 'таксистов'],
					'вор':		  ['вора', 'воров'],
					'ребёнок':    ['ребёнка', 'детей']}, 
			'inst': {'охранник':  ['охранником', 'охранниками'],
				     'повар': 	  ['поваром', 'поварами'],
				     'фигуристка':['фигуристкой', 'фигуристками'],
				     'таксист':   ['таксистом', 'таксистами'],
				     'вор':		  ['вором', 'ворами'],
				     'ребёнок':	  ['ребёнком', 'детьми'],}}


def make_all():
	test_type = "prep_anim"

	lcodes = {0: 'en', 1: 'fr', 2: 'ru'}
	gcodes = {0: '_s', 1: '_p'}
	gcombinations = list(itertools.product([0, 1], repeat=2))
	lcombinations = list(itertools.product([0, 1, 2], repeat=3))

	for subj in subjects:
		for prep in preps:
			for attractor in attractors:
				for verb in verbs:
					# 0-index = Subject, 1-index = Prepositional phrase, 2-index = Verb
					for lcombo in lcombinations:
						l0, l1, l2 = lcodes[lcombo[0]], lcodes[lcombo[1]], lcodes[lcombo[2]]

						for gcombo in gcombinations:
							g0, g1 = gcodes[gcombo[0]], gcodes[gcombo[1]]
							c0, c1 = l0 + g0, l1 + g1

							# grammatical verb agrees in number with subject
							gv, ugv = g0, gcodes[(1+gcombo[0])%2]

							tag = c0+"--"+c1+"--"+l2

							this_subj = subj[c0]
							good_this_verb, bad_this_verb = verb[l2+gv], verb[l2+ugv]

							# Build PP
							this_pp = ""
							this_prep = prep[l1]
							# Russian has issues 
							if l1 == 'ru':
								case = russian_cases[this_prep]
								declined_attractor = declined[case][attractor[c1]][gcombo[1]]
								
								this_pp = this_prep + " " + declined_attractor 
							# French has issues
							elif this_prep[-2:] == "de":
								# Ex: prep = "en face de", attractor = "le chef" -> en face du chef
								# Ex: prep = "en face de", attractor = "l'homme" -> en face de l'homme
								# Ex: prep = "en face de", attractor = "les hommes" -> en face des hommes
								
								this_pp = this_prep[:-3] # "en face"
								this_attractor = attractor[c1].split()
								
								if this_attractor[0][:2] == "l\'":
									this_pp += " de " + this_attractor[0]
								elif this_attractor[0] == "la":
									this_pp += " de la " + this_attractor[1]
								elif this_attractor[0] == "le":
									this_pp += " du " + this_attractor[1]
								elif this_attractor[0] == "les":
									this_pp += " des " + this_attractor[1]
								else:
									print("EEK ERROR?!?!", attractor, this_attractor, file=sys.stderr)
							else:
								this_pp = this_prep + " " + attractor[c1] 


							good_sent = this_subj + " " + this_pp + " " + good_this_verb
							bad_sent = this_subj + " " + this_pp + " " + bad_this_verb

							print("\t".join([test_type, tag, good_sent, bad_sent]))


def make_russianfrench():


	lcodes = {0: 'fr', 1: 'ru'}
	gcodes = {0: '_s', 1: '_p'}
	combinations = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 1), (1, 0, 0), (1, 1, 1), (1, 1, 0)]
	output = []
	for subj in subjects:
		for prep in preps:
			for attractor in attractors:
				for verb in verbs:
					# 0-index = Subject, 1-index = Prepositional phrase, 2-index = Verb
					for lcombo in combinations:
						l0, l1, l2 = lcodes[lcombo[0]], lcodes[lcombo[1]], lcodes[lcombo[2]]

						for gcombo in combinations:
							g0, g1, g2 = gcodes[gcombo[0]], gcodes[gcombo[1]], gcodes[gcombo[2]]
							c0, c1, c2 = l0 + g0, l1 + g1, l2 + g2

							# is grammatical if subject (0-index) and verb (2-index) agree
							#     This is true if 0,0 or 1,1 and not if 0,1 or 1,0
							is_grammatical = str((gcombo[0] + gcombo[2]) % 2 == 0)
							
							tag = c0+"--"+c1+"--"+l2

							this_subj = subj[c0]
							this_verb = verb[c2]

							# Build PP
							this_pp = ""
							this_prep = prep[l1]
							# Russian has issues 
							if l1 == 'ru':
								case = russian_cases[this_prep]
								declined_attractor = declined[case][attractor[c1]][gcombo[1]]
								
								this_pp = this_prep + " " + declined_attractor 
							elif this_prep[-2:] == "de":
								# Ex: prep = "en face de", attractor = "le chef" -> en face du chef
								# Ex: prep = "en face de", attractor = "l'homme" -> en face de l'homme
								# Ex: prep = "en face de", attractor = "les hommes" -> en face des hommes
								
								this_pp = this_prep[:-3] # "en face"
								this_attractor = attractor[c1].split()
								
								if this_attractor[0][:2] == "l\'":
									this_pp += " de " + this_attractor[0]
								elif this_attractor[0] == "la":
									this_pp += " de la " + this_attractor[1]
								elif this_attractor[0] == "le":
									this_pp += " du " + this_attractor[1]
								elif this_attractor[0] == "les":
									this_pp += " des " + this_attractor[1]
								else:
									print("EEK ERROR?!?!", attractor, this_attractor, file=sys.stderr)
							else:
								this_pp = this_prep + " " + attractor[c1] 


							sent = this_subj + " " + this_pp + " " + this_verb
							print("\t".join([is_grammatical, tag, sent]))

def make_russian():
	russian_cases = {'рядом с': 'inst', 'около': 'gen', 'напротив': 'gen', 'перед': 'inst', 'за': 'inst', 'посреди': 'gen'}
	declined = {'gen': {'охранник':   ['охранника', 'охранников'],
						'повар': 	  ['повара', 'поваров'],
						'фигуристка': ['фигуристки', 'фигуристок'],
						'таксист':    ['таксиста', 'таксистов'],
						'вор':		  ['вора', 'воров'],
						'ребёнок':    ['ребёнка', 'детей']}, 
				'inst': {'охранник':  ['охранником', 'охранниками'],
					     'повар': 	  ['поваром', 'поварами'],
					     'фигуристка':['фигуристкой', 'фигуристками'],
					     'таксист':   ['таксистом', 'таксистами'],
					     'вор':		  ['вором', 'ворами'],
					     'ребёнок':	  ['ребёнком', 'детьми'],}}

	lcodes = {0: 'en', 1: 'ru'}
	gcodes = {0: '_s', 1: '_p'}
	combinations = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 1), (1, 0, 0), (1, 1, 1), (1, 1, 0)]
	output = []
	for subj in subjects:
		for prep in preps:
			for attractor in attractors:
				for verb in verbs:
					# 0-index = Subject, 1-index = Prepositional phrase, 2-index = Verb
					for lcombo in combinations:
						l0, l1, l2 = lcodes[lcombo[0]], lcodes[lcombo[1]], lcodes[lcombo[2]]

						for gcombo in combinations:
							g0, g1, g2 = gcodes[gcombo[0]], gcodes[gcombo[1]], gcodes[gcombo[2]]
							c0, c1, c2 = l0 + g0, l1 + g1, l2 + g2

							# is grammatical if subject (0-index) and verb (2-index) agree
							#     This is true if 0,0 or 1,1 and not if 0,1 or 1,0
							is_grammatical = str((gcombo[0] + gcombo[2]) % 2 == 0)
							
							tag = c0+"--"+c1+"--"+l2

							this_subj = subj[c0]
							this_verb = verb[c2]

							# Build PP
							this_pp = ""
							this_prep = prep[l1]
							# Russian has issues 
							if l1 == 'ru':
								case = russian_cases[this_prep]
								declined_attractor = declined[case][attractor[c1]][gcombo[1]]
								
								this_pp = this_prep + " " + declined_attractor 
							else:
								this_pp = this_prep + " " + attractor[c1] 


							sent = this_subj + " " + this_pp + " " + this_verb
							print("\t".join([is_grammatical, tag, sent]))


def make_french():

	lcodes = {0: 'en', 1: 'fr'}
	gcodes = {0: '_s', 1: '_p'}
	combinations = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 1), (1, 0, 0), (1, 1, 1), (1, 1, 0)]
	output = []
	for subj in subjects:
		for prep in preps:
			for attractor in attractors:
				for verb in verbs:
					# 0-index = Subject, 1-index = Prepositional phrase, 2-index = Verb
					for lcombo in combinations:
						l0, l1, l2 = lcodes[lcombo[0]], lcodes[lcombo[1]], lcodes[lcombo[2]]

						for gcombo in combinations:
							g0, g1, g2 = gcodes[gcombo[0]], gcodes[gcombo[1]], gcodes[gcombo[2]]
							c0, c1, c2 = l0 + g0, l1 + g1, l2 + g2

							# is grammatical if subject (0-index) and verb (2-index) agree
							#     This is true if 0,0 or 1,1 and not if 0,1 or 1,0
							is_grammatical = str((gcombo[0] + gcombo[2]) % 2 == 0)
							
							tag = c0+"--"+c1+"--"+l2

							this_subj = subj[c0]
							this_verb = verb[c2]

							# Build PP
							this_pp = ""
							this_prep = prep[l1]
							# French has issues 
							if this_prep[-2:] == "de":
								# Ex: prep = "en face de", attractor = "le chef" -> en face du chef
								# Ex: prep = "en face de", attractor = "l'homme" -> en face de l'homme
								# Ex: prep = "en face de", attractor = "les hommes" -> en face des hommes
								
								this_pp = this_prep[:-3] # "en face"
								this_attractor = attractor[c1].split()
								
								if this_attractor[0][:2] == "l\'":
									this_pp += " de " + this_attractor[0]
								elif this_attractor[0] == "la":
									this_pp += " de la " + this_attractor[1]
								elif this_attractor[0] == "le":
									this_pp += " du " + this_attractor[1]
								elif this_attractor[0] == "les":
									this_pp += " des " + this_attractor[1]
								else:
									print("EEK ERROR?!?!", attractor, this_attractor, file=sys.stderr)
							else:
								this_pp = this_prep + " " + attractor[c1] 


							sent = this_subj + " " + this_pp + " " + this_verb
							print("\t".join([is_grammatical, tag, sent]))


def verify_verb_tokens_equal():
	print("Verifying verbs are BERT friendly")
	from pytorch_pretrained_bert import tokenization

	model_name = 'bert-base-multilingual-cased'
	tokenizer=tokenization.BertTokenizer.from_pretrained(model_name, do_lower_case=False)
	print("tokenization model loaded:",file=sys.stderr)
	
	langs = ['en', 'fr', 'ru']
	conjs = ['_s', '_p']
	for verb in verbs:
		for lang in langs:
			t1 = tokenizer.tokenize(verb[lang+conjs[0]])
			t2 = tokenizer.tokenize(verb[lang+conjs[1]])
			print(t1, t2)

			if len(t1) != len(t2):
				print("AAH!! Token Mismatch")
				print(t1, t2)
	print("all verbs okay!",file=sys.stderr)

		
        
# make_french()
# make_russian()
# make_russianfrench()

# verify_verb_tokens_equal()

make_all()


