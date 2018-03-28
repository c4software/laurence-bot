# -*- coding: utf-8 -*-
from commands.libs.decorators import register_as_command
from commands.libs.history import get_history
from commands.libs.context import get_last_message, get_probable_command
from tools.libs import make_message, get_username, save_new_user, username_or_channel, reply_to_user
from settings import PSEUDO
from commands.libs.decorators import commands
import random

def cmd_start(msg):
    if "telegram" in msg: # pragma: no cover
        save_new_user(username_or_channel(msg), msg["telegram"]["update"].message.chat.id)
        reply_to_user(msg, "Bonjour, Je suis Laurence. Pour avoir la liste des commandes tapez /aide")
        return True
    else:
        return False

@register_as_command("test", None, keywords=["debug", "ping", "pong"])
def cmd_test(msg):
    # Commande qui permet de tester que le bot est là (réponse aléatoire)
    reponse = ["Hum! 1, 2, 1, 2.", "C’est OK ! :thumbs_up_sign:", "Pong", "Debug OK.\nTag : 120391000092.\nHum c’est OK !", "I’m sorry Dave, I’m afraid I can't do that"]
    return random.choice(reponse)

@register_as_command("aide", "Affiche L'aide")
def cmd_aide(msg):
    # Retourne l’aide (généré dynamiquement)
    return get_command_list()

@register_as_command("bisous", None, keywords=["kiss", "bise"])
def cmd_bisous(msg):
    # Commande d’ambiance pour les salons et les chats
    return ":kiss:"

@register_as_command("echo", None, keywords=[])
def cmd_echo(msg):
    # Commande d’echo
    return msg["query"]

@register_as_command("bonjour", "Heu… Bonjour?", keywords=["salut", "hey", "coucou"])
def cmd_bonjour(msg):
    # Commande d’ambiance
    return '{0} {1}, besoin d’aide ?'.format(random.choice(["Salut", "Coucou", "Bonjour", "Hello", "Hoy"]), get_username(msg))

def get_command_list():
    '''
        Génération de l’aide.
        Parcours des commandes et des descriptions chargé au lancement du bot.
        Les commandes sans descriptions ne sont pas retourné.
    '''
    from commands.libs.decorators import descriptions
    command_list = "\n"
    for group in descriptions:
        sub_command_list = ""
        for command in descriptions[group]:
            if descriptions[group][command]:
                sub_command_list = sub_command_list+"\n- {0} ({1})".format(command, descriptions[group][command])

        if sub_command_list:
            command_list = command_list+"\n{0} : {1}".format(group, sub_command_list)

        command_list = command_list+"\n"

    return command_list


@register_as_command("historique", "Affiche votre historique de message", "Global")
def cmd_show_history(msg):
    historique = get_history(get_username(msg))
    if historique:
        return "- "+"\n- ".join(historique)
    else: # pragma: no cover
        return "Aucun historique"

# Commande pour rejouer la dernière commande
@register_as_command("plus", None, keywords=["encore"])
def cmd_more(msg):
    previous_text = get_last_message(msg)

    # Réécriture des args avec la nouvelle commande
    msg["args"]     = previous_text.split(' ')[1:]
    msg["query"]    = " ".join(msg["args"])

    if previous_text:
        commande = get_probable_command(previous_text)
        if commande in commands:
            return commands[commande](msg)
        else:
            return ""
    else:
        return ""
