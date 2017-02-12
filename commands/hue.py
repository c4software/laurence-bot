# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

@register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
def cmd_hue(msg):
    return "Prochainement"

def cmd_communicate_hue_server():
    pass

def cmd_init_hue():
    pass

def cmd_set_level():
    pass

def cmd_change_room_state():
    pass
