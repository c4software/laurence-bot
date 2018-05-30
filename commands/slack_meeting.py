# -*- coding: utf-8 -*-
import copy
import datetime
import os
import threading
import time
from collections import OrderedDict

import holidays
import schedule

from commands.libs.context import mark_for_awaiting_response, get_awaiting_response
from commands.libs.decorators import register_as_command
from settings import SLACK_REPORT_CHANNEL, SLACK_REPORT_MEMBERS, MAP_TRADUCTION
from tools.libs import get_username

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK", None)
TODAY_MEETING = {}
TEST_TOKEN = "SAMPLE_TOKEN"


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
        TODAY_MEETING[username] = OrderedDict()


def text_for_report(username):
    """
        Retourne le texet pour l'interaction en mode meeting
    """
    if "yesterday" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return MAP_TRADUCTION["yesterday"]
    elif "today" not in TODAY_MEETING[username]:
        mark_for_awaiting_response(username, "meeting")
        return MAP_TRADUCTION["today"]
    else:
        return None


def is_weekend():
    """
        Détermine si le jour courant est un weekend.
    """
    return datetime.datetime.today().weekday() >= 5


def is_holidays():
    """
        Détermine si lejour courant est un jour ferié
    :return:
    """
    return datetime.datetime.today() in holidays.FRA()


def ask_for_report():
    """
        Fonction lancée automatiquement lors des messages automatiques, permet de demander
        aux différents utilisateurs leur rapport journalier.
    """
    if is_weekend() or is_holidays():
        return

    for user_id in SLACK_REPORT_MEMBERS:
        init_report_for_username(user_id)
        # Envoi le message uniquement au gens n'ayant pas fait leur report
        # (today et yesterday non présent dans TODAY_MEETING[username])
        if MAP_TRADUCTION.keys() >= TODAY_MEETING[user_id].keys():
            text_to_send = text_for_report(user_id)
            if text_to_send:
                send_direct_message(user_id, text_to_send)
                mark_for_awaiting_response(user_id, "meeting")
            else:
                pass


def remove_awaitings():
    """
    Supprime le mode « attente » de réponse.
    :return:
    """
    for user_id in SLACK_REPORT_MEMBERS:
        get_awaiting_response(user_id)


if SLACK_TOKEN:
    @register_as_command("meeting_report", "Affiche le rapport global", "Meeting")
    def cmd_report(msg={}):
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
                    formated_user_reports = '>'.join(report[username][event].splitlines(True))
                    message += "*{0}:* \r\n".format(MAP_TRADUCTION[event])
                    message += "> {0}\r\n\r\n".format(formated_user_reports)
                    message += "\r\n"

        if message:
            remove_awaitings()
            if SLACK_REPORT_CHANNEL != "" and SLACK_TOKEN != "" and SLACK_TOKEN != TEST_TOKEN:
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

        text_to_send = text_for_report(username)

        if text_to_send:
            return text_to_send
        else:
            return "Merci !"

if SLACK_TOKEN and SLACK_TOKEN != TEST_TOKEN and SLACK_REPORT_CHANNEL:
    def report_planed():
        """
            Méthode utilisé pour le thread des messages automatiques.
            Déclenché uniquement en mode slack.
        """
        print("Register report scheduling at « 10:00 » every week day")
        schedule.every().day.at("10:00").do(cmd_report)

        for time_schedule in ["09:00", "09:30", "09:45", "09:50"]:
            print("Register ask_for_report scheduling at « {0} » every week day".format(time_schedule))
            schedule.every().day.at(time_schedule).do(ask_for_report)

        while schedule.run_pending:
            schedule.run_pending()
            time.sleep(1)


    threading.Thread(target=report_planed, args=()).start()
