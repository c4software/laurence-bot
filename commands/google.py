# -*- coding: utf-8 -*-

from .decorators import register_as_command
try:
    from google import search
except:
    pass

@register_as_command("google", "Effectue une recherche Google", "Web")
def cmd_do_googlesearch(msg):
    try:
        for url in search(msg["query"], tld='fr', lang='fr',num=1, stop=1):
            return "Voilà ce que j’ai trouvé … \n {0}".format(url)
    except:
        print ("Pour utiliser la recherche vous devez : pip install https://github.com/MarioVilas/google/archive/master.zip")
