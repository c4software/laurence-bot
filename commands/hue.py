# -*- coding: utf-8 -*-

from tools.rest import callrest
from libs.decorators import register_as_command
from settings import HUE_BRIDGE

from tools.libs import get_username, save_new_user, reply_to_user

from database import db_session
from models.models import User

import logging

try:
    from qhue import Bridge, create_new_username

    @register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
    def cmd_hue(msg):
        if "init" in msg["text"]: # pragma: no cover
            cmd_init_hue(msg)
        elif "allume" in msg["text"]: # pragma: no cover
            cmd_change_room_state(msg, "TODO", True)
        elif "eteindre" in msg["text"]: # pragma: no cover
            cmd_change_room_state(msg, "TODO", False)
except: # pragma: no cover
    logging.error ("qhue is required to use the hue module")

def cmd_communicate_hue_server(msg, ressource, bri): # pragma: no cover
    pseudo      =   get_username(msg)
    utilisateur =   User.query.filter_by(username=pseudo).one()
    if "hue_username" in current_user.settings:
        b = Bridge(HUE_BRIDGE, current_user.settings.hue_username)
    else:
        reply_to_user(msg, "Pour utiliser les commandes HUE, vous devez faire « hue init »")

def cmd_init_hue(msg): # pragma: no cover
    reply_to_user(msg, "Association avec votre bridge HUE.")
    reply_to_user(msg, "Pour m’autoriser à dialoguer avec votre bridge HUE, merci d’appuyer sur le bouton présent sur celui-ci.")
    # Récupération du « username » depuis le BRIDGE HUE
    hue_username = create_new_username(HUE_BRIDGE)

    # Récupération du pseudo de la personne qui parle
    pseudo = get_username(msg)

    # Sauvegarde de l’association entre l’username hue et la personne qui parle
    current_user = save_new_user(pseudo, msg["telegram"]["update"].message.chat.id)
    current_user.settings.hue_username = hue_username
    db_session.merge(current_user)
    db_session.commit()

    # Retour pour le client
    reply_to_user(msg, "L’association avec votre brigde est maintenant effectif, vous pouvez utiliser toutes les commandes.")

def cmd_set_level(msg, ressource, bri): # pragma: no cover
    cmd_communicate_hue_server(msg, ressource, bri)

def cmd_change_room_state(msg, ressource, state=True): # pragma: no cover
    if state:
        cmd_communicate_hue_server(msg, ressource, 128)
    else:
        cmd_communicate_hue_server(msg, ressource, 0)
