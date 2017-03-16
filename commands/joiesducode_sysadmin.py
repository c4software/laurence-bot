# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import JOIESDUCODE_URL, JOIESDUCODE_PATH, LESJOIESDUSYSADMIN_URL, LESJOIESDUSYSADMIN_PATH


def get_joieducode(n=1):
    try:
        data = callrest(domain=JOIESDUCODE_URL, port="80", path=JOIESDUCODE_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        titre = soup.find_all("h1")[0]
        image = soup.find_all("div", class_="blog-post-content")[0].find("img")['src']

        return "{0} : ![image]({1})".format(titre.strip(), image)
    except: # pragma: no cover
        if n > 2:
            return "Désolé récupération impossible"
        else:
            return get_joieducode(n=n+1)

def get_lesjoiesdusysadmin(n=1):
    try:
        data = callrest(domain=LESJOIESDUSYSADMIN_URL, port="80", path=LESJOIESDUSYSADMIN_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        titre = soup.select("div.content")[0].h3.span.text
        image = soup.find_all("div", class_="text")[0].find("img")['src']

        return "{0} : ![image]({1})".format(titre.strip(), image)
    except: # pragma: no cover
        if n > 2:
            return "Désolé récupération impossible"
        else:
            return get_lesjoiesdusysadmin(n=n+1)

@register_as_command("code", "Affiche un joieducode aléatoire", "Web")
def cmd_joieducode(msg):
    return get_joieducode()

@register_as_command("sysadmin", "Affiche un joiedusysadmin aléatoire", "Web")
def cmd_lesjoiesdusysadmin(msg):
    return get_lesjoiesdusysadmin()
