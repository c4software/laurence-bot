# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command
import json


from settings import GIPHY_URL, GIPHY_PATH, GIPHY_API_KEY, MASHAPE_KEY


def get_gyphy(keyword):
    try:
        params = {}
        params['api_key'] = GIPHY_API_KEY
        params['tag'] = keyword
        data = callrest(domain=GIPHY_URL, ssl=True, path=GIPHY_PATH, params=params, user_headers={"X-Mashape-Key": MASHAPE_KEY})[2]
        retour = json.loads(data)
        if len(retour['data']) == 0:
            return get_gyphy("")
        return return_md(retour['data']['image_original_url'])
    except Exception as e:
        print("Erreur ! {0}".format(e))
        return ("Oups", "Rien... ")


def return_md(image):
    return "![image]({0})".format(image)

@register_as_command("giphy", "Recherche une image sur giphy (prend un thème en paramètre)", "Gif")
def cmd_gyphy(msg):
    return get_gyphy(msg["query"])
