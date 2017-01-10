# -*- coding: utf-8 -*-

from .decorators import register_as_command
from commands.history import get_history, get_last_tags
from settings import DEBUG_USER
from emoji import emojize

@register_as_command("learn", "", "Interne")
def cmd_do_learn(msg):
    username = msg["user_name"][0]
    if "telegram" in msg and username in DEBUG_USER:
        print (get_history(username)[-2])
        print (get_last_tags(username))
        return emojize("Correspondance ajoutée :thumbs_up_sign:")
    else:
        return emojize("Désolé le learn n’est pas disponible :unamused_face:")
