# -*- coding: utf-8 -*-

from .decorators import register_as_command

from .context import mark_for_awaiting_response
from tools.libs import get_username

try:
    from google import search
except:
    pass

@register_as_command("google", "Effectue une recherche Google", "Web")
def cmd_do_googlesearch(msg):
    try:
        if msg["query"]:
            for url in search(msg["query"], tld='fr', lang='fr',num=1, stop=1):
                return "Voilà ce que j’ai trouvé … \n {0}".format(url)
        else:
            mark_for_awaiting_response(get_username(msg), "google")
            return "Bien, que recherchez vous ?"
    except:
        return "Recherche impossible."
