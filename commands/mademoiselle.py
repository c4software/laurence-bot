# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import MADEMOISELLE_URL, MADEMOISELLE_PATH


def get_mademoiselle():
    try:
        data = callrest(domain=MADEMOISELLE_URL, port="80", path=MADEMOISELLE_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        image = soup.find_all("div", class_="photo")[0].find("img")['src']
        return return_md(image)
    except Exception as e:
        print (e)
        return ("Oups", "Rien... ")


def return_md(image):
    return "![image]({0})".format(image)


@register_as_command("mlle", "Affiche un bonjour mademoiselle aléatoire")
def cmd_mademoiselle(msg):
    if msg.get("channel_name", [''])[0] == "nsfw":
        return get_mademoiselle()
    else:
        return "## Mauvais channel"