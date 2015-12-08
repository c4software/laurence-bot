# -*- coding: utf-8 -*-

from rest import callrest
from settings import SMALLNABS_DOMAIN, SMALLNABS_PORT

def launch_stop():
    try:
        data = callrest(domain=SMALLNABS_DOMAIN, port=SMALLNABS_PORT, path="/stop", params={})[2]
        return ""
    except Exception as e:
        print (e)
        return "Erreur"


def launch_play(params):
    try:
        data = callrest(domain=SMALLNABS_DOMAIN, port=SMALLNABS_PORT, path="/play", params=params)[2]
        return ""
    except Exception as e:
        print (e)
        return "Erreur"


def cmd_stop(msg):
    return launch_stop()


def cmd_play(msg):
    params = {"file": msg["text"][0].split(' ')[2]}
    return launch_play(params)
