# -*- coding: utf-8 -*-

from .decorators import register_as_command

from .context import mark_for_awaiting_response
from tools.libs import username_or_channel

try:
    from google import search
except: # pragma: no cover
    pass

@register_as_command("google", "Effectue une recherche Google", "Web", ["hey", "ordinateur", "laurence"])
def cmd_do_googlesearch(msg):
    try:
        if msg["query"]:
            for url in search(msg["query"], tld='fr', lang='fr',num=1, stop=1):
                return "Voici le premier résultat \n {0}".format(url)
        else:
            mark_for_awaiting_response(username_or_channel(msg), "google")
            return "Oui ? Que recherchez vous ?"
    except: # pragma: no cover
        return "Recherche impossible."
