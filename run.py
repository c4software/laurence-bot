#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from extended_BaseHTTPServer import serve,route, redirect, override
from rest import callrest
from commands import commands
from settings import *

def chat(kwargs):
    try:
        commande = kwargs['text'][0].split(' ')[1]
        if commande in commands:
            ret = {"text": commands[commande](kwargs), "username": PSEUDO}
            return json.dumps(ret)
    except Exception as e:
        pass

def welcome():
    params = {
        'payload': '{"text": "Bonjour, c\'est à vous !"}'
    }
    data = callrest(domain=MATTERMOST_DOMAIN, type="POST", path=MATTERMOST_PATH, params=params)

@route("/",["POST"])
def form(**kwargs):
    kwargs['preview'] = False
    return chat(kwargs)

@route("/preview",["POST"])
def preview(**kwargs):
    kwargs['preview'] = True
    return chat(kwargs)

@route("/", ["GET"])
def test(**kwargs):
    return commands["boobs"](kwargs)

if __name__ == '__main__':
    print("Serving BOT on {0} port {1} ...".format(IP, PORT))
    welcome()
    serve(ip=IP, port=PORT)
