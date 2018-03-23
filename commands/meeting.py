# -*- coding: utf-8 -*-
from .decorators import register_as_command

@register_as_command("meeting", "Stand", "Images")
def cmd_metting(msg):
    return "Hey! T'as fait quoi hier ?"