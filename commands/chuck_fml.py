# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import FML_URL, FML_PATH, CHUCK_DOMAIN, CHUCK_PATH

@register_as_command("fml", "Affiche un fuck my life", "Web")
def cmd_fml(msg):
    try:
        data = callrest(domain=FML_URL, port="80", path=FML_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        texte = soup.select("div.post.article")[0].p.text

        return texte
    except Exception as e:
        return None

@register_as_command("chuck", "Chuck Norris a déjà compté jusqu'à l'infini. Deux fois.", "Web")
def cmd_chuck(msg):
    try:
        data = callrest(domain=CHUCK_DOMAIN, path=CHUCK_PATH)[2]
        return html.unescape(json.loads(data)[0].get("fact"))
    except Exception as e:
        return None
