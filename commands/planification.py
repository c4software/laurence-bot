# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_last_message
from commands.context import mark_for_awaiting_response
from tools.libs import get_probable_command, username_or_channel
from commands.decorators import commands


def extract_hours_minutes(query):
    '''
    Éxtraction des heures du message saisie par l’utilisateur
    '''
    if query:
        query = query.replace("h", ":")
        query = query.split(":")
        return query[0], query[1]
    else:
        return None, None

@register_as_command("planifier", "Planifier la réccurrence de la précédente commande", keywords=[])
def cmd_planifier(msg):
    '''
    Commande pour la planification d’un message récuurrent.
    Utilise le context pour la réponse. Ex :

    - Vous: /planifier
    - Lui : À qu’elle heure ?
    - Vous : 10h
    - Lui : Trés bien … planification de « commande » à 10h

    ou :

    - Vous /planifier 10h
    - Lui : Trés bien … planification de « commande » à 10h
    '''
    previous_text = get_last_message(msg)
    previous_text = get_probable_command(previous_text)
    if previous_text and previous_text != "planifier":
        heure, minute = extract_hours_minutes(msg["query"])
        if heure:
            # TODO Planification
            return "[TODO] Planification effective, vous allez recevoir automatiquement « {0} » tous les jours à {1}h{2}".format(previous_text, heure, minute)
        else:
            mark_for_awaiting_response(username_or_channel(msg), "planifier")
            return "À qu’elle heure voulez vous planifier l’envoi automatique de « {0} » ?".format(previous_text)
    else:
        return "Désolé, je ne peu pas planifier autre chose qu’une commande."
