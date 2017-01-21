# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_last_message
from commands.context import mark_for_awaiting_response
from tools.libs import get_probable_command, username_or_channel
from commands.decorators import commands

def extract_hours_minutes(query):
    pass

@register_as_command("planifier", "Planifier la réccurence de la précédente commande", keywords=[])
def cmd_planifier(msg):
    previous_text = get_last_message(msg)
    if previous_text != "planning":
        date = extract_hours_minutes(msg["query"])
        if date:
            # TODO Planification
            return "Planification effective, vous allez recevoir automatiquement « {0} » tous les jours à {1}".format(previous_text, date)
        else:
            mark_for_awaiting_response(username_or_channel(msg), "planning")
            return "À qu’elle heure voulez vous planifier l’envoi automatique de « {0} » ?".format(previous_text)
    else:
        return "Je ne peux pas planifier la planification"
