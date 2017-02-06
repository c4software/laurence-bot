# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import MADAME_URL, MADAME_PATH


def get_madame():
    try:
        data = callrest(domain=MADAME_URL, port="80", path=MADAME_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        image = soup.find_all("div", class_="photo")[0].find("img")['src']
        return "![image]({0})".format(image)
    except Exception as e:
        return None

@register_as_command("madame", "Affiche un bonjour madame aléatoire", "Images")
def cmd_madame(msg):
    return get_madame()
