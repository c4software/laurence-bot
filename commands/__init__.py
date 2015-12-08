# -*- coding: utf-8 -*-

from .reddit import *
from .lapin import *
from .general import *
from .jenkins import *

commands = {
    "bonjour": cmd_bonjour,
    "random": cmd_random,
    "nsfw": cmd_nsfw,
    "image": cmd_image,
    "gif": cmd_gif,
    "cute": cmd_cute,
    "top10": cmd_top10,
    "aide": cmd_aide,
    "play": cmd_play,
    "stop": cmd_stop,
    "jstatus": cmd_building
}
