# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command
import json


from settings import GIPHY_URL, GIPHY_PATH, GIPHY_API_KEY, MASHAPE_KEY


def get_gyphy(keyword, md=True):
    '''
    Éfféctue une recherche d’un gif via GIPHY
    :param keyword: Mot clef recheché
    :param md: Indique si le retour doit-être du type Markdown
    '''
    try:
        params = {}
        params['api_key'] = GIPHY_API_KEY
        params['tag'] = keyword
        data = callrest(domain=GIPHY_URL, ssl=True, path=GIPHY_PATH, params=params, user_headers={"X-Mashape-Key": MASHAPE_KEY})[2]
        retour = json.loads(data)
        if len(retour['data']) == 0:
            return get_gyphy("")
        if md:
            return return_md(retour['data']['image_original_url'])
        else:
            return retour['data']['image_original_url']
    except Exception as e:
        return None


def return_md(image):
    return "![image]({0})".format(image)

@register_as_command("giphy", "Recherche une image sur giphy (prend un thème en paramètre)", "Gif", keywords=["gif"])
def cmd_gyphy(msg):
    return get_gyphy(msg["query"], md="telegram" not in msg)

@register_as_command("fail", "LA catégorie !", "Gif")
def cmd_gyphy(msg):
    return get_gyphy("fail", md="telegram" not in msg)
