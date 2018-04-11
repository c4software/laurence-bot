# -*- coding: utf-8 -*-
import os
from commands.libs.context import mark_for_awaiting_response
from commands.libs.decorators import register_as_command
from tools.libs import get_username
import threading
import time
import schedule

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK")
SLACK_REPORT_CHANNEL = os.environ.get("SLACK_REPORT_CHANNEL", "")

TODAY_MEETING = {}

MAP_TRADUCTION = {"today": "Tu prévois quoi aujourd'hui ?", "yesterday": "T'as fait quoi hier ?"}

@register_as_command("meeting_report", "Affiche le rapport global", "Meeting")
def cmd_report(msg):
    message = ""
    report = TODAY_MEETING
    for username in report:
        message = "{}: \r\n".format(username)
        for event in report[username]:
            message += "*{0}:* \r\n".format(MAP_TRADUCTION[event])
            message += "> {0}\r\n\r\n".format('>'.join(report[username][event].splitlines(True)))

    if message:
        if SLACK_REPORT_CHANNEL != "" and SLACK_TOKEN != "":
            send_slack_message_channel(message)
            return "Message envoyé dans @{0}".format(SLACK_REPORT_CHANNEL)
        else:
            return message
    else:
        return "Personne n'a fait de report pour l'instant"

def send_slack_message_channel(content):
    from slackclient import SlackClient
    client = SlackClient(SLACK_TOKEN)
    client.api_call("chat.postMessage",link_names=1, channel=SLACK_REPORT_CHANNEL, text=content)

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
        schedule.every().day.at("10:00").do(cmd_report, msg={})
        while schedule.run_pending:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=report_planed, args=()).start()
