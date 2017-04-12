# -*- coding: utf-8 -*-
import json
import signal
import sys
import atexit

from tools.extended_BaseHTTPServer import serve,route, redirect, override
from tools.rest import callrest

from commands import *
from commands.decorators import commands
from settings import *

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def chat(kwargs):
    try:
        commande = kwargs['text'][0].split(' ')
        if len (commande) > 1:
            commande = commande[1]
        else:
            commande = commande[0]

        commande = commande.lower()

        kwargs["query"] = "".join(kwargs["text"][0].split(' ')[2:])

        # Sauvegarde de l’historique
        add_history(pseudo=kwargs["user_name"][0], command="{0} {1}".format(commande, kwargs["query"]))

        if commande in commands:
            retour = commands[commande](kwargs)
            if retour != "" and retour is not None:
                if type(retour) is str:
                    return build_response(kwargs, retour)
                else:
                    # Impossible de retourner un message enrichie alors, on passe par l'API
                    callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params={"payload": json.dumps(retour)})
        else:
            pass

    except Exception as e:
        logging.error(e)
        pass

def build_response(kwargs, retour):
    ret = {"text": retour, "username": PSEUDO}
    if kwargs['slash_command']:
        ret["response_type"] = "in_channel"
    return json.dumps(ret)

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
    if kwargs['channel_name'][0] in DISABLE_CHANNEL:
        pass

    return chat(kwargs)

if __name__ == '__main__':
    print("Serving Laurenc on {0} port {1} ...".format(IP, PORT))
    serve(ip=IP, port=PORT)
