# -*- coding: utf-8 -*-

from .decorators import register_as_command
from commands.history import get_history, get_last_tags
from settings import DEBUG_USER
from emoji import emojize
from tools.text import save_alias
from tools.libs import is_telegram, is_debug, get_username

@register_as_command("learn", "", "Interne")
def cmd_do_learn(msg):
    username = get_username(msg)
    save_alias(get_history(username)[-2], get_last_tags(username))

    if is_telegram(msg) and is_debug(username):
        print (get_history(username)[-2])
        print (get_last_tags(username))
        return emojize("Correspondance ajoutée :thumbs_up_sign:")
    else:
        return emojize("Désolé le learn n’est pas disponible :unamused_face:")
