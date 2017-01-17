# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

def get_commitstrip():
    try:
        # Récupération du dernier CommitStrip
        data = callrest(domain="www.commitstrip.com", port="80", path="/fr/feed/", user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        lien = soup.select("item")[0].link.text

        # Récupération de l’image.
        o = urlparse(lien)
        data = callrest(domain=o.netloc, port="80", path=o.path, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        return soup.select("p > img")[0].attrs.get("src")
    except Exception as e:
        return "Désolé pas de CommitStrip disponible."

@register_as_command("commitstrip", "Affiche le dernier CommitStrip", "Commitstrip", keywords=["cs"])
def cmd_commitstrip(msg):
    return get_commitstrip()
