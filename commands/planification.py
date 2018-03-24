# -*- coding: utf-8 -*-
from commands.libs.decorators import register_as_command
from commands.libs.history import get_last_message
from commands.libs.context import mark_for_awaiting_response
from tools.libs import get_probable_command, username_or_channel
from commands.libs.decorators import commands

from database import db_session
from models.models import Task

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

@register_as_command("planning", "Affiche la liste des commandes planifier", keywords=[])
def cmd_planning(msg):
    tasks = Task.query.filter_by(username=username_or_channel(msg)).all()
    if tasks:
        retour = "Voici la liste des commandes planifiés : \n"
        for task in tasks:
            retour = "{0} - « {1} » tous les jours à {2}\n".format(retour, task.commande, task.planned_time)
    else:
        retour = "Aucune commande planifiés."

    return retour

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
    if previous_text and "planifier" not in previous_text:
        heure, minute = extract_hours_minutes(msg["query"])
        if heure:
            task = Task(username_or_channel(msg), "{0}:{1}".format(heure, minute), previous_text)
            db_session.add(task)
            db_session.commit()
            return "Parfait ! Vous allez recevoir automatiquement « {0} » tous les jours à {1}h{2}".format(previous_text, heure, minute)
        else:
            mark_for_awaiting_response(username_or_channel(msg), "planifier")
            return "À qu’elle heure voulez vous planifier l’envoi automatique de « {0} » ?".format(previous_text)
    else:
        return "Désolé, je ne peu pas planifier autre chose qu’une commande."
