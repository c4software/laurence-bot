# -*- coding: utf-8 -*-

from rest import callrest
from settings import SMALLNABZ_DOMAIN, SMALLNABZ_PORT
from .decorators import register_as_command

def launch_stop():
    try:
        data = callrest(domain=SMALLNABZ_DOMAIN, port=SMALLNABZ_PORT, path="/stop", params={})[2]
        return ""
    except Exception as e:
        print (e)
        return "Erreur"


def launch_play(params):
    try:
        data = callrest(domain=SMALLNABZ_DOMAIN, port=SMALLNABZ_PORT, path="/play", params=params)[2]
        return ""
    except Exception as e:
        print (e)
        return "Erreur"

@register_as_command("stop", "Arrête la diffusion")
def cmd_stop(msg):
    return launch_stop()

@register_as_command("play", "Lance la diffusion d'un son (Ex: play http://www.youtube.com/?v=SIREST)", "SmallNabz")
def cmd_play(msg):
    params = {"file": msg["text"][0].split(' ')[2]}
    return launch_play(params)
