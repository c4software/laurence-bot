# -*- coding: utf-8 -*-

from tools.rest import callrest
from commands.libs.decorators import register_as_command
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
        data = callrest(domain="www.commitstrip.com", port="80", path="/fr/feed/")[2]
        soup = BeautifulSoup(data, "html.parser")
        liens = soup.select("item")
        if not latest:
            # Pas de flag latest on en prend un en aléatoire
            data = random.choice(liens).find("content:encoded").text
        else:
            # Uniquement le dernier
            data = liens[0].find("content:encoded").text

        # Get the image
        soup = BeautifulSoup(data, "html.parser")
        return soup.select("p > img")[0].attrs.get("src")
    except Exception as e:  # pragma: no cover
        return "Impossible de récupérer les CommitStrip. {}".format(e)


@register_as_command("commitstrip", "Affiche le dernier CommitStrip", "Commitstrip", keywords=["cs"])
def cmd_commitstrip(msg):
    if "random" in msg["query"]:
        return get_commitstrip()
    else:
        return get_commitstrip(latest=True)
