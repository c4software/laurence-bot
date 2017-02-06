# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import FML_URL, FML_PATH


def get_fuckmylife():
    try:
        data = callrest(domain=FML_URL, port="80", path=FML_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        texte = soup.select("div.post.article")[0].p.text

        return texte
    except Exception as e:
        return None
        
@register_as_command("fml", "Affiche un fuck my life", "Web")
def cmd_viedemerde(msg):
    return get_fuckmylife()
