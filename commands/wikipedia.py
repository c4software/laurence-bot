# -*- coding: utf-8 -*-

from tools.rest import callrest
from .decorators import register_as_command
import json
import wikipedia

from .context import mark_for_awaiting_response
from tools.libs import username_or_channel

@register_as_command("def", "Recherche la définition sur Wikipedia", "Web", keywords=["wikipedia", "wiki"])
def cmd_aide(msg):
    """
    Cherche la définition demandé par l’utilisateur
    :param msg: Objet qui correspond à la demande de l’utilisateur.
    """

    if not msg["query"]:
        mark_for_awaiting_response(username_or_channel(msg), "def")
        return "Bien, sur quel sujet ?"

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
                return "{0} \n\nEn savoir plus : https://{1}/?curid={2}".format(page.get("extract", ""), domain, page_id)
            else:
                raise Exception("KO")
    except:
        if msg["query"]:
            return "Aucun résultat pour {0}".format(query)
