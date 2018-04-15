# -*- coding: utf-8 -*-
import os
import datetime
import threading
import time
import copy
import schedule
from commands.libs.context import mark_for_awaiting_response
from commands.libs.decorators import register_as_command
from tools.libs import get_username

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK")
SLACK_REPORT_CHANNEL = os.environ.get("SLACK_REPORT_CHANNEL", "")
SLACK_REPORT_MEMBERS = os.environ.get("SLACK_REPORT_MEMBERS", "").split(",")

TODAY_MEETING = {}

MAP_TRADUCTION = {"today": "Tu prévois quoi aujourd'hui ?", "yesterday": "T'as fait quoi hier ?"}

@register_as_command("meeting_report", "Affiche le rapport global", "Meeting")
def cmd_report(msg = {}):
    """
        Genere le rapport pour la journée en cours,
        et le supprime une fois envoyé dans le salon de reporting.
    """
    message = ""
    report = copy.deepcopy(TODAY_MEETING)
    for username in report:
        del TODAY_MEETING[username]
        # Seulement si l'utilisateur à fait un report
        if "today" in report[username]:
            message += "\r\n{0}: \r\n".format(username)
            for event in report[username]:
                message += "*{0}:* \r\n".format(MAP_TRADUCTION[event])
                message += "> {0}\r\n\r\n".format('>'.join(report[username][event].splitlines(True)))
                message += "\r\n"

    if message:
        if SLACK_REPORT_CHANNEL != "" and SLACK_TOKEN != "":
            send_direct_message(SLACK_REPORT_CHANNEL, message, as_user=False)
            return "Message envoyé dans @{0}".format(SLACK_REPORT_CHANNEL)
        else:
            return message
    else:
        return "Aucun reporting pour l'instant"

@register_as_command("meeting", "Enregistre une nouvelle entrée", "Meeting")
def cmd_metting(msg):
    """
        Enregistrement d'un nouveau rapport
    """
    username = get_username(msg)
    task = msg["query"]

    init_report_for_username(username)

    if task:
        if "yesterday" not in TODAY_MEETING[username]:
            TODAY_MEETING[username]["yesterday"] = task
        elif "today" not in TODAY_MEETING[username]:
            TODAY_MEETING[username]["today"] = task

    return text_for_report(username)

def get_slack_client():
    """
        Retourne le client slack en fonction du token courant.
    """
    from slackclient import SlackClient
    return SlackClient(SLACK_TOKEN)

def send_direct_message(user_id, content, as_user=True):
    """
        Envoi d'un message direct dans un channel.
    """
    client = get_slack_client()
    client.api_call("chat.postMessage", link_names=1, channel=user_id, text=content, as_user=as_user)

def init_report_for_username(username):
    """
        Initialise la structure pour le « rapport » de l'utilisateur.
    """
    if username not in TODAY_MEETING:
        TODAY_MEETING[username] = {}

def text_for_report(username):
    """
        Retourne le texet pour l'interaction en mode meeting
    """
    if "yesterday" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return "Hey! T'as fait quoi hier ?"
    elif "today" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return "Et aujourd'hui tu prévois quoi ?"
    else:
        return "Merci !"

def is_weekend():
    """
        Détermine si le jour courant est un weekend.
    """
    return datetime.datetime.today().weekday() >= 5

def ask_for_report():
    """
        Fonction lancée automatiquement lors des messages automatiques, permet de demander
        aux différents utilisateurs leur rapport journalier.
    """
    if is_weekend():
        return

    for user_id in SLACK_REPORT_MEMBERS:
        init_report_for_username(user_id)
        # Envoi le message uniquement au gens n'ayant pas fait leur report
        # (today et yesterday non présent dans TODAY_MEETING[username])
        if MAP_TRADUCTION.keys() >= TODAY_MEETING[user_id].keys():
            send_direct_message(user_id, text_for_report(user_id))
            mark_for_awaiting_response(user_id, "meeting")

if SLACK_REPORT_CHANNEL:
    def report_planed():
        """
            Méthode utilisé pour le thread des messages automatiques.
            Déclenché uniquement en mode slack.
        """
        print("Register report scheduling at « 10:00 » every week day")
        print("Register ask_for_report scheduling at « 09:30 » every week day")
        schedule.every().day.at("10:00").do(cmd_report)
        schedule.every().day.at("09:30").do(ask_for_report)
        while schedule.run_pending:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=report_planed, args=()).start()
