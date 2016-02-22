# -*- coding: utf-8 -*-
import json
import signal
import sys

from extended_BaseHTTPServer import serve,route, redirect, override
from rest import callrest
from commands.decorators import commands
from settings import *
from commands import giphy
import random

def chat(kwargs):
    try:
        commande = kwargs['text'][0].split(' ')[1]
        if commande in commands:
            retour = commands[commande](kwargs)
            if retour != "" and retour is not None:
                if type(retour) is str:
                    return build_response(kwargs, retour)
                else:
                    # Impossible de retourner un message enrichie alors, on passe par l'API
                    callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(retour)})
        else:
            return build_response(kwargs, giphy.get_gyphy("".join(kwargs["text"][0].split(' ')[1:])))

    except Exception as e:
        print (e)
        pass

def build_response(kwargs, retour):
    ret = {"text": retour, "username": PSEUDO}
    if kwargs['slash_command']:
        ret["response_type"] = "in_channel"
    return json.dumps(ret)

def welcome():
    params = {"username": PSEUDO, "attachments": [{"color": "#3c901a", "title": PSEUDO, "text":"System Ready !".format(PSEUDO)}]}
    data = callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(params)})

def aurevoir():
    params = {"username": PSEUDO, "text": "Au revoir {0}".format("https://www.youtube.com/watch?v=uIMBjES4B4g")}
    data = callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(params)})

@route("/",["POST"])
def form(**kwargs):
    kwargs['preview'] = False

    # Ajout de la gestion des slash commands (pour l'instant transformation en commande normal)
    if "command" in kwargs:
        kwargs['text'][0] = "{0} {1}".format(kwargs['command'][0].replace("/", ""), kwargs['text'][0])
        kwargs['slash_command'] = True
    else:
        kwargs['slash_command'] = False

    # Test si le bot est non actif sur le channel en cours.
    if kwargs['channel_name'][0] in settings.DISABLE_CHANNEL:
        return build_response(kwargs, "Impossible...")

    return chat(kwargs)

def signal_handler(signal, frame):
    aurevoir()
    sys.exit(0)

if __name__ == '__main__':
    print("Serving BOT on {0} port {1} ...".format(IP, PORT))
    #welcome()
    #signal.signal(signal.SIGINT, signal_handler)
    serve(ip=IP, port=PORT)
