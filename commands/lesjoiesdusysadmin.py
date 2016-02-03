# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import LESJOIESDUSYSADMIN_URL, LESJOIESDUSYSADMIN_PATH


def get_lesjoiesdusysadmin():
    try:
        data = callrest(domain=LESJOIESDUSYSADMIN_URL, port="80", path=LESJOIESDUSYSADMIN_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        titre = soup.select("div.content")[0].h3.span.text
        image = soup.find_all("div", class_="text")[0].find("img")['src']

        return return_md(titre.strip(), image)
    except Exception as e:
        print(e)
        return ("Oups", "Rien... ")


def return_md(titre, image):
    return "{0} : ![image]({1})".format(titre, image)


@register_as_command("sysadmin", "Affiche un joiedusysadmin aléatoire")
def cmd_lesjoiesdusysadmin(msg):
    return get_lesjoiesdusysadmin()