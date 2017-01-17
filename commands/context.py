# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_history
from tools.libs import get_probable_command, get_username
from commands.decorators import commands

@register_as_command("plus", None, keywords=["encore"])
def cmd_more(msg):
    username = get_username(msg)
    previous_text = get_history(username)[-2]

    commande = get_probable_command(previous_text)
    if commande in commands:
        return commands[commande](msg)
    else:
        return None
