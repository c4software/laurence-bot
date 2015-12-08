# -*- coding: utf-8 -*-
from .decorators import register_as_command
from libs import make_message
from settings import PSEUDO

@register_as_command("aide")
def cmd_aide(msg):
    from .decorators import commands
    command_list = "\r\n- {0}".format("\r\n- ".join(commands.keys()))
    return make_message(username=PSEUDO, icon_url="", fallback=command_list, pretext="", title="Liste des commandes :", title_link="", text=command_list, color="#7CD197")

@register_as_command("bonjour")
def cmd_bonjour(msg):
    return 'Bonjour {0}'.format(msg['user_name'][0])
