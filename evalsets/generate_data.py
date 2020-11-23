# coding=utf-8
import sys


subjects = [{'en_s': 'the senator', 	'en_p': 'the senators', 	'fr_s': 'le sénateur', 		'fr_p': 'les sénateurs'},
         	{'en_s': 'the author', 		'en_p': 'the authors', 		'fr_s': 'l\'auteur', 		'fr_p': 'les auteurs'}, 
         	{'en_s': 'the pilot', 		'en_p': 'the pilots', 		'fr_s': 'le pilote', 		'fr_p': 'les pilotes'}, 
         	{'en_s': 'the surgeon', 	'en_p': 'the surgeons', 	'fr_s': 'le chirugien', 	'fr_p': 'les chirugiens'}, 
         	{'en_s': 'the customer', 	'en_p': 'the customers', 	'fr_s': 'le client', 		'fr_p': 'les clients'}, 
         	{'en_s': 'the consultant', 	'en_p': 'the consultants', 	'fr_s': 'le consultant', 	'fr_p': 'les consultants'}, 
        	{'en_s': 'the manager', 	'en_p': 'the managers', 	'fr_s': 'l\'homme', 		'fr_p': 'les hommes'}, 
         	{'en_s': 'the officer', 	'en_p': 'the officers', 	'fr_s': 'l\'officier', 		'fr_p': 'les officiers'},
         	{'en_s': 'the farmer', 		'en_p': 'the farmers', 		'fr_s': 'l\'agriculteur', 	'fr_p': 'les agriculteurs'}, 
         	{'en_s': 'the teacher',	 	'en_p': 'the teachers', 	'fr_s': 'l\'enseignant', 	'fr_p': 'les enseignants'}]

preps = [{'en': 'next to', 		'fr': 'à côté de'}, 
		 {'en': 'near',    	    'fr': 'près de'},
		 {'en': 'across from',  'fr': 'en face de'},
	     { 'en': 'in front of', 'fr': 'devant'},
  		 { 'en': 'with', 		'fr': 'avec'}]

attractors = [{'en_s': 'the guard', 		'en_p': 'the guards', 		'fr_s': 'le garde', 	'fr_p': 'les gardes'},
         	  {'en_s': 'the chef', 			'en_p': 'the chefs', 		'fr_s': 'le chef', 		'fr_p': 'les chefs'}, 
         	  {'en_s': 'the skater', 		'en_p': 'the skaters', 		'fr_s': 'le patineur', 	'fr_p': 'les patineurs'}, 
              {'en_s': 'the taxi driver', 	'en_p': 'the taxi drivers', 'fr_s': 'le chauffeur', 'fr_p': 'les chauffeurs'}, 
              {'en_s': 'the theif', 		'en_p': 'the theives', 		'fr_s': 'le voleur', 	'fr_p': 'les voleurs'}, 
              {'en_s': 'the child', 		'en_p': 'the children', 	'fr_s': 'l\'enfant', 	'fr_p': 'les enfants'}]

verbs = [{'en_s': 'has flowers', 'en_p': 'have flowers', 'fr_s': 'a des fleurs', 'fr_p': 'ont des fleurs'}, 
         {'en_s': 'talks',       'en_p': 'talk', 		 'fr_s': 'parle', 		 'fr_p': 'parlent'}, 
         {'en_s': 'waits',       'en_p': 'wait', 		 'fr_s': 'attends',      'fr_p': 'attendent'}, 
         {'en_s': 'exists',      'en_p': 'exist', 		 'fr_s': 'existe', 		 'fr_p': 'existent'}, 
         {'en_s': 'is',          'en_p': 'are', 		 'fr_s': 'est', 		 'fr_p': 'sont'}, 
         {'en_s': 'carries',     'en_p': 'carry', 		 'fr_s': 'porte', 		 'fr_p': 'portent'}, 
         {'en_s': 'was',         'en_p': 'were', 		 'fr_s': 'était', 		 'fr_p': 'étaient'},
         {'en_s': 'goes', 		 'en_p': 'go', 		 	 'fr_s': 'va', 			 'fr_p': 'vont'}]

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

