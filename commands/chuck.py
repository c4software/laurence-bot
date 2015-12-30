# -*- coding: utf-8 -*-

import json
import html
from rest import callrest
from settings import CHUCK_DOMAIN, CHUCK_PATH
from .decorators import register_as_command


def launch_chuck(params):
    try:
        data = callrest(domain=CHUCK_DOMAIN, path=CHUCK_PATH)[2]
        return html.unescape(json.loads(data)[0].get("fact"))
    except Exception as e:
        print (e)
        return "Erreur"


@register_as_command("chuck")
def cmd_chuck(msg):
    return launch_chuck(msg)
