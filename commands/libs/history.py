# -*- coding: utf-8 -*-

import json

from .decorators import register_as_command
from tools.libs import get_username, username_or_channel

from database import db_session
from models.models import Historique

last_text = {}

def add_history(pseudo, command):
    '''
    Ajout un historique
    :param pseudo: Pseudo de l’utilisateur en question.
    :param command: Commande à ajouter à l’historique.
    '''
    historique = Historique(pseudo, command.rstrip())
    db_session.add(historique)
    db_session.commit()

def remove_last_history(pseudo):
    historique = Historique.query.filter_by(username=pseudo).order_by(Historique.datetime.desc()).limit(1).one()
    if historique:
        db_session.delete(historique)
        db_session.commit()

def get_history(pseudo):
    historique = Historique.query.filter_by(username=pseudo).all()
    return [h.text for h in historique]

def get_last_message(msg):
    # Récupération du dernier message dans l’historique. (Utilisé pour le context)
    try:
        pseudo = username_or_channel(msg)
        remove_last_history(pseudo)
        return Historique.query.filter_by(username=pseudo).order_by(Historique.datetime.desc()).limit(1).one().text
    except: # pragma: no cover
        return ""

def get_last_tags(pseudo):
    # Gestion des tags pour l’apprentissage
    return last_text.get(pseudo, [])

def save_last_tags(pseudo, tags):
    # Gestion des tags pour l’apprentissage
    last_text[pseudo] = tags