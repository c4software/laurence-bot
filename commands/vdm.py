# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import VDM_URL, VDM_PATH


def get_viedemerde():
    try:
        data = callrest(domain=VDM_URL, port="80", path=VDM_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        texte = soup.select("div.post.article")[0].p.text

        return return_md(texte)
    except Exception as e:
        print(e)
        return ("Oups", "Rien... ")


def return_md(titre):
    return "{0}".format(titre)


@register_as_command("vdm", "Affiche un vie de merde")
def cmd_viedemerde(msg):
    return get_viedemerde()
