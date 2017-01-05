# -*- coding: utf-8 -*-

from rest import callrest
from .decorators import register_as_command
import json
import wikipedia
# https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=valentin

@register_as_command("def", "Recherche la définition sur Wikipedia", "Web")
def cmd_aide(msg):
    try:
        wikipedia.set_lang("fr")
        query = wikipedia.search(msg["query"], results=1).pop(0).replace(" ", "_")

        # En français la lib wikipedia ne fonctionne pas vraiment bien (exemple valentin est impossible à charger…)
        if query:
            params = {"format": "json", "action":"query", "prop": "extracts", "exintro":"", "explaintext":"", "titles": query}
            domain = "fr.wikipedia.org"
            retour = callrest(domain=domain, port="443", ssl=True, params=params, path="/w/api.php", user_headers={"Accept-Charset": "utf-8"})
            retour = json.loads(retour[2])
            page_id = list(retour["query"]["pages"]).pop(0)
            if page_id != "-1":
                page = retour["query"]["pages"][page_id]
                return "{0} \n\nEn savoir plus : https://{1}/wiki/{2}".format(page.get("extract", ""), domain, page.get("title", ""))
            else:
                raise Exception("")
    except:
        if msg["query"]:
            return "Aucun résultat pour {0}".format(query)
