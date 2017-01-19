# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_last_message
from commands.context import mark_for_awaiting_response
from tools.libs import get_probable_command, get_username, make_attrs, is_private_channel
from commands.decorators import commands

@register_as_command("planifier", "Planifier la réccurence de la précédente commande", keywords=[])
def cmd_planifier(msg):
    previous_text = get_last_message(msg)
    if previous_text != "planning":
        mark_for_awaiting_response(msg)
        return "À qu’elle heure voulez vous planifier l’envoi automatique de « {0} » ?".format(previous_text)
    else:
        return "Je ne peux pas planifier la planification"
