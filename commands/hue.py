# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command
from settings import HUE_BRIDGE

from libs import get_username, save_new_user, reply_to_user

from database import db_session
from models.models import User

import logging

try:
    from qhue import Bridge, create_new_username

    @register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
    def cmd_hue(msg):
        if "init" in msg["text"]:
            cmd_init_hue(msg)
except:
    logging.debug ("qhue is required to use the hue module")

def cmd_communicate_hue_server(msg, ressource, bri):
    pseudo      =   get_username(msg)
    utilisateur =   User.query.filter_by(username=pseudo).one()
    if "hue_username" in current_user.settings:
        b = Bridge(HUE_BRIDGE, current_user.settings.hue_username)
    else:
        reply_to_user(msg, "Pour utiliser les commandes HUE, vous devez faire « hue init »")

def cmd_init_hue(msg):
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

def cmd_set_level(msg, ressource, bri):
    cmd_communicate_hue_server(msg, ressource, bri)
    pass

def cmd_change_room_state(msg, ressource, state=True):
    if state:
        cmd_communicate_hue_server(msg, ressource, 128)
    else:
        cmd_communicate_hue_server(msg, ressource, 0)
