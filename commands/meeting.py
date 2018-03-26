# -*- coding: utf-8 -*-
from commands.libs.context import mark_for_awaiting_response
from commands.libs.decorators import register_as_command
from tools.libs import get_username

today_metting = []

@register_as_command("meeting_repport", "Affiche le rapport global", "Meeting")
def cmd_report(msg):
    message = ""
    for username in today_metting:
        message = "@{0}: \r\n"
        for event in today_metting[username]:
            message += "\t{0} : \r\n\t\t {1}".format(event, today_metting[username][event])

    today_metting = []

    return message

@register_as_command("meeting", "Enregistre une nouvelle entrée", "Meeting")
def cmd_metting(msg):
    username = get_username(msg)
    task =  msg["query"]

    if username not in today_metting:
        today_metting[username] = {}

    if "yesterday" not in today_metting[username]:
        today_metting[username]["yesterday"] = task
    elif "today" not in today_metting[username]:
        today_metting[username]["today"] = task


    if "yesterday" not in today_metting[username]:
        mark_for_awaiting_response(username, "meeting")
        return "Hey! T'as fait quoi hier ?" 
    elif "today" not in today_metting[username]:
        mark_for_awaiting_response(username, "meeting")        
        return "Et aujourd'hui tu prévois quoi ?"       
    else:
        return "Merci !"