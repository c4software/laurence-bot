# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup

from settings import MADEMOISELLE_URL, MADEMOISELLE_PATH, MADAME_URL, MADAME_PATH

@register_as_command("mlle", "Affiche un bonjour mademoiselle aléatoire", "Images")
def cmd_mademoiselle(msg):
    try:
        data = callrest(domain=MADEMOISELLE_URL, port="80", path=MADEMOISELLE_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        image = soup.find_all("div", class_="photo")[0].find("img")['src']
        return "![image]({0})".format(image)
    except Exception as e:
        return None

@register_as_command("madame", "Affiche un bonjour madame aléatoire", "Images")
def cmd_madame(msg):
    try:
        data = callrest(domain=MADAME_URL, port="80", path=MADAME_PATH, user_headers={"Accept-Charset": "utf-8"})[2]
        soup = BeautifulSoup(data, "html.parser")
        image = soup.find_all("div", class_="photo")[0].find("img")['src']
        return "![image]({0})".format(image)
    except Exception as e:
        return None
