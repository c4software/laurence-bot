# -*- coding: utf-8 -*-
import json

from extended_BaseHTTPServer import serve,route, redirect, override
from rest import callrest
from commands.decorators import commands
from settings import *

def chat(kwargs):
    try:
        commande = kwargs['text'][0].split(' ')[1]
        if commande in commands:
            retour = commands[commande](kwargs)
            if retour != "" and retour is not None:
                if type(retour) is str:
                    ret = {"text": retour, "username": PSEUDO}
                    return json.dumps(ret)
                else:
                    # Impossible de retourner un message enrichie alors, on passe par l'API
                    callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(retour)})

    except Exception as e:
        print (e)
        pass

def welcome():
    params = {"username": PSEUDO, "attachments": [{"color": "#3c901a", "title": PSEUDO, "text":"System Ready !".format(PSEUDO)}]}
    data = callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(params)})

@route("/",["POST"])
def form(**kwargs):
    kwargs['preview'] = False
    return chat(kwargs)

if __name__ == '__main__':
    print("Serving BOT on {0} port {1} ...".format(IP, PORT))
    #welcome()
    serve(ip=IP, port=PORT)
