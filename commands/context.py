# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_last_message
from tools.libs import get_probable_command, get_username, make_attrs, is_private_channel
from commands.decorators import commands

@register_as_command("plus", None, keywords=["encore"])
def cmd_more(msg):
    previous_text = get_last_message(msg)

    # Réécriture des args avec la nouvelle commande
    msg["args"]     = previous_text.split(' ')[1:]
    msg["query"]    = " ".join(msg["args"])

    if previous_text:
        commande = get_probable_command(previous_text)
        if commande in commands:
            return commands[commande](msg)
        else:
            return None
    else:
        return None
