# -*- coding: utf-8 -*-
import os
from commands.libs.context import mark_for_awaiting_response
from commands.libs.decorators import register_as_command
from tools.libs import get_username, get_users_list_slack
import threading
import time
import copy
import schedule

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK")
SLACK_REPORT_CHANNEL = os.environ.get("SLACK_REPORT_CHANNEL", "")
SLACK_REPORT_MEMBERS = os.environ.get("SLACK_REPORT_MEMBERS", "").split(",")

TODAY_MEETING = {}

MAP_TRADUCTION = {"today": "Tu prévois quoi aujourd'hui ?", "yesterday": "T'as fait quoi hier ?"}

@register_as_command("meeting_report", "Affiche le rapport global", "Meeting")
def cmd_report(msg = {}):
    message = ""
    report = copy.deepcopy(TODAY_MEETING)
    for username in report:
        del TODAY_MEETING[username]
        message += "\r\n{}: \r\n".format(username)
        for event in report[username]:
            message += "*{0}:* \r\n".format(MAP_TRADUCTION[event])
            message += "> {0}\r\n\r\n".format('>'.join(report[username][event].splitlines(True)))
            message += "\r\n"

    if message:
        if SLACK_REPORT_CHANNEL != "" and SLACK_TOKEN != "":
            send_slack_message_channel(message)
            return "Message envoyé dans @{0}".format(SLACK_REPORT_CHANNEL)
        else:
            return message
    else:
        return "Personne n'a fait de report pour l'instant"

def get_slack_client():
    from slackclient import SlackClient
    return SlackClient(SLACK_TOKEN)

def send_slack_message_channel(content):
    client = get_slack_client()
    client.api_call("chat.postMessage", link_names=1, channel=SLACK_REPORT_CHANNEL, text=content)

def send_direct_message(client, user_id, content):
   client.api_call("chat.postMessage", link_names=1, channel=user_id, text=content, as_user=True)

def ask_for_report():
    client = get_slack_client()
    for user_id in SLACK_REPORT_MEMBERS:
        send_direct_message(client, user_id, "Hey, c'est l\'heure du Standup Meeting. Tape « meeting » pour commencer.")

@register_as_command("meeting", "Enregistre une nouvelle entrée", "Meeting")
def cmd_metting(msg):
    username = get_username(msg)
    task = msg["query"]

    if username not in TODAY_MEETING:
        TODAY_MEETING[username] = {}

    if task:
        if "yesterday" not in TODAY_MEETING[username]:
            TODAY_MEETING[username]["yesterday"] = task
        elif "today" not in TODAY_MEETING[username]:
            TODAY_MEETING[username]["today"] = task

    if "yesterday" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return "Hey! T'as fait quoi hier ?"
    elif "today" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return "Et aujourd'hui tu prévois quoi ?"
    else:
        return "Merci !"

if SLACK_REPORT_CHANNEL:
    print("Register report scheduling at « 10:00 » everyday")
    def report_planed():
        schedule.every().day.at("10:00").do(cmd_report)
        schedule.every().day.at("09:30").do(ask_for_report)
        while schedule.run_pending:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=report_planed, args=()).start()
