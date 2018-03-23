# -*- coding: utf-8 -*-
from .context import mark_for_awaiting_response
from .decorators import register_as_command
from tools.libs import get_username

@register_as_command("meeting", "Enregistre une nouvelle entrée", "Meeting")
def cmd_metting(msg):
    mark_for_awaiting_response(get_username(msg), "meeting")
    return "Hey! T'as fait quoi hier ?"