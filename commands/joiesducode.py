# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import JOIESDUCODE_URL, JOIESDUCODE_PATH


def get_joieducode():
    try:
        data = callrest(domain=JOIESDUCODE_URL, port="80", path=JOIESDUCODE_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        titre = soup.find_all("h1")[0].string.replace("stagiaire", "@stagiaire")
        image = soup.find_all("div", class_="blog-post-content")[0].find("img")['src']

        return return_md(titre.strip(), image)
    except Exception as e:
        return get_joieducode()


def return_md(titre, image):
    return "{0} : ![image]({1})".format(titre, image)


@register_as_command("code", "Affiche un joieducode aléatoire", "Web")
def cmd_joieducode(msg):
    return get_joieducode()
