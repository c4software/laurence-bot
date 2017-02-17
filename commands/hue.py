# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command
from settings import HUE_BRIDGE
import logging

try:
    from qhue import Bridge, create_new_username
    @register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
    def cmd_hue(msg):
        return "Prochainement"
except:
    logging.debug ("qhue is required to use the hue module")

def cmd_communicate_hue_server(ressource, bri):
    username = "TODO"
    b = Bridge(HUE_BRIDGE, username)
    pass

def cmd_init_hue():
    username = create_new_username(HUE_BRIDGE)
    # TODO Save username

def cmd_set_level(ressource, bri):
    cmd_communicate_hue_server(ressource, bri)
    pass

def cmd_change_room_state(ressource, state=True):
    if state:
        cmd_communicate_hue_server(ressource, 128)
    else:
        cmd_communicate_hue_server(ressource, 0)
