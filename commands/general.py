# -*- coding: utf-8 -*-
from .decorators import register_as_command
from libs import make_message
from settings import PSEUDO
import random

@register_as_command("aide", "Affiche L'aide")
def cmd_aide(msg):
    return get_command_list()
    #return make_message(username=PSEUDO, icon_url="", fallback=command_list, pretext="", title="Liste des commandes :", title_link="", text=command_list, color="#7CD197")

@register_as_command("bonjour", "Heu… Bonjour?", keywords=["salut", "hey", "coucou"])
def cmd_bonjour(msg):
    return '{0} {1}, besoin d’/aide ?'.format(random.choice(["Salut", "Coucou", "Bonjour", "Hello", "Hoy"]),msg['user_name'][0])

def get_command_list():
    from .decorators import commands, descriptions
    command_list = "\n"
    for group in descriptions:
        sub_command_list = ""
        for command in descriptions[group]:
            if descriptions[group][command]:
                sub_command_list = sub_command_list+"\n- {0} ({1})".format(command, descriptions[group][command])

        if sub_command_list:
            command_list = command_list+"\n{0} : {1}".format(group, sub_command_list)

        command_list = command_list+"\n"

    return command_list
