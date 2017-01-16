# -*- coding: utf-8 -*-
from .decorators import register_as_command
from libs import make_message
from settings import PSEUDO
import random

@register_as_command("test", None, keywords=["debug", "ping", "pong"])
def cmd_test(msg):
    reponse = ["Hum! 1, 2, 1, 2.", "C’est OK ! :thumbs_up_sign:", "Pong", "Debug OK.\nTag : 120391000092.\nHum c’est OK !", "I’m sorry Dave, I’m afraid I can't do that"]
    return random.choice(reponse)

@register_as_command("aide", "Affiche L'aide")
def cmd_aide(msg):
    return get_command_list()

@register_as_command("bisous", None, keywords=["kiss", "bise"])
def cmd_aide(msg):
    return ":kiss:"

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
