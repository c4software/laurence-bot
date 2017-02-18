# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command
from settings import HUE_BRIDGE

from libs import get_username, save_new_user

from database import db_session
from models.models import User

import logging

try:
    from qhue import Bridge, create_new_username
    @register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
    def cmd_hue(msg):
        return "Prochainement"
except:
    logging.debug ("qhue is required to use the hue module")

def cmd_communicate_hue_server(msg, ressource, bri):
    pseudo = get_username(msg)
    b = Bridge(HUE_BRIDGE, "TODO")
    pass

def cmd_init_hue(msg):
    # Récupération du « username » depuis le BRIDGE HUE
    hue_username = create_new_username(HUE_BRIDGE)

    # Récupération du pseudo de la personne qui parle
    pseudo = get_username(msg)

    # Sauvegarde de l’association entre l’username hue et la personne qui parle
    current_user = save_new_user(pseudo, msg["telegram"]["update"].message.chat.id)
    current_user.settings.hue_username = hue_username
    db_session.merge(current_user)
    db_session.commit()

def cmd_set_level(msg, ressource, bri):
    cmd_communicate_hue_server(msg, ressource, bri)
    pass

def cmd_change_room_state(msg, ressource, state=True):
    if state:
        cmd_communicate_hue_server(msg, ressource, 128)
    else:
        cmd_communicate_hue_server(msg, ressource, 0)
