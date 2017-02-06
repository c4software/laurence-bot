# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import VDM_URL, VDM_PATH

def get_viedemerde():
    try:
        data = callrest(domain=VDM_URL, port="80", path=VDM_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        texte = soup.select("div.post.article")[0].p.text

        return texte
    except Exception as e:
        return get_viedemerde()

@register_as_command("vdm", "Affiche une « quote » de vie de merde", "Web")
def cmd_viedemerde(msg):
    return get_viedemerde()
