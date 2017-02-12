# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

@register_as_command("hue", "Gestion des ampoules hue.", "Domotique")
def cmd_hue(msg):
    return "Prochainement"
