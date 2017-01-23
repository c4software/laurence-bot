# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import random

def get_commitstrip(latest=False):
    """
    Récupération d’un CommitStrip.
    Utilisation du flux RSS pour récupérer la liste des CommitStrip.
    :param latest: Retourne uniquement le Cs le plus récent
    """
    try:
        # Récupération du flux CommitStrip
        data = callrest(domain="www.commitstrip.com", port="80", path="/fr/feed/", user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        if not latest:
            # Pas de flag latest on en prend un en aléatoire
            lien = random.choice(soup.select("item")).link.text
        else:
            # Uniquement le dernier
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
    if "random" in msg["query"]:
        return get_commitstrip()
    else:
        return get_commitstrip(latest=True)
