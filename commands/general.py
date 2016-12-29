# -*- coding: utf-8 -*-
from .decorators import register_as_command
from libs import make_message
from settings import PSEUDO

@register_as_command("aide", "Affiche L'aide")
def cmd_aide(msg):
    return get_command_list()
    #return make_message(username=PSEUDO, icon_url="", fallback=command_list, pretext="", title="Liste des commandes :", title_link="", text=command_list, color="#7CD197")

@register_as_command("bonjour", "Heu… Bonjour?")
def cmd_bonjour(msg):
    return 'Bonjour {0}'.format(msg['user_name'][0])

def get_command_list():
    from .decorators import commands, descriptions
    command_list = "\r\n"
    for group in descriptions:
        command_list = command_list+"\r\n"
        command_list = command_list+"{0} :".format(group)
        for command in descriptions[group]:
            command_list = command_list+"\r\n- {0} ({1})".format(command, descriptions[group][command])
        command_list = command_list+"\r\n"

    return command_list
