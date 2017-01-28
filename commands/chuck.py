# -*- coding: utf-8 -*-

import json
import html
from tools.rest import callrest
from settings import CHUCK_DOMAIN, CHUCK_PATH
from .decorators import register_as_command

def launch_chuck():
    """
    Récupération d’un Chuck Norris Fact. (Via API)
    """
    try:
        data = callrest(domain=CHUCK_DOMAIN, path=CHUCK_PATH)[2]
        return html.unescape(json.loads(data)[0].get("fact"))
    except Exception as e:
        return None


@register_as_command("chuck", "Chuck Norris a déjà compté jusqu'à l'infini. Deux fois.", "Web")
def cmd_chuck(msg):
    return launch_chuck()
