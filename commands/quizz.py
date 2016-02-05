# -*- coding: utf-8 -*-
from .decorators import register_as_command
import random
import codecs
import operator
import difflib

class quizz():
	quizz_question = ""
	quizz_reponse = ""
	quizz_tabscore = {}

def get_question():
	f = codecs.open("data/quizz_general.txt", 'r',"iso-8859-1")
	questions = f.read().splitlines()
	choice =random.choice(questions).split("\\")
	quizz.quizz_question     = choice[0]
	quizz.quizz_reponse      = choice[1].lstrip().rstrip()
	return "> "+quizz.quizz_question

def sayindice():
		if quizz.quizz_question:
			try:
				indice = ""
				letter = random.choice(quizz.quizz_reponse)
				for x in quizz.quizz_reponse:
					if x == letter:
						indice = indice+str(x)
					else:
						if x == " ":
							indice = indice+"  "
						else:
							indice = indice+" _"

				return "Un petit indice: {0}".format(indice)
			except:
				return "Pas d'indice..."
		else:
			return "Aucun quizz en cours"

@register_as_command("question", "C'est parti ! (Pour répondre ! r ma réponse")
def cmd_quizzstart(msg):
	return get_question()

@register_as_command("indice", "Quizz un indice")
def cmd_indice(msg):
	return sayindice()	

@register_as_command("r", "! r votre réponse")
def cmd_quizzreponse(msg):
	username = msg['user_name'][0]

	reponse  = str(msg['text'][0])
	reponse = reponse.replace("{0} r ".format(msg['trigger_word'][0]), "")

	if reponse.strip().lower() == quizz.quizz_reponse.strip().lower():
		try:
			score = quizz.quizz_tabscore[username]
			quizz.quizz_tabscore[username] = score+1
		except:
			quizz.quizz_tabscore[username] = 1

		return 'Bravo! Bonne reponse {0} \r\nQuestion suivante : \r\n {1}'.format(username, get_question())
	else:
		# Test si la reponse s'approche
		if difflib.SequenceMatcher(None, quizz.quizz_reponse.strip().lower(), reponse.strip().lower()).ratio() > 0.7:
			return 'ha {0} pas loin!'.format(username)
		else:
			# Si ce n'est pas la bonne reponse et que la reponse est eloigne
			if random.randint(0,20) == 10:
				# tous les quelques messages on diffuse soit un indice, soit la question
				if random.choice(['indice', 'question']) == "indice":
					return sayindice()
				else:
					return quizz.quizz_question

@register_as_command("score", "Affiche le score")
def cmd_quizzscore(msg):
	string_score = "Score : "
	for user in quizz.quizz_tabscore:
		string_score = string_score + " \r\n " + str(user) + " : " + str(quizz.quizz_tabscore[user])

	return string_score