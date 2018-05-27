import os
import datetime
import threading
import time
from commands.libs.decorators import register_as_command
import schedule

from models.models import Link

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK", None)


def get_slack_client():
    """
        Retourne le client slack en fonction du token courant.
    """
    from slackclient import SlackClient
    return SlackClient(SLACK_TOKEN)


def send_direct_message(channel_id, content, as_user=True):
    """
        Envoi d'un message direct dans un channel.
    """
    client = get_slack_client()
    client.api_call("chat.postMessage", link_names=1, channel=channel_id, text=content, as_user=as_user)


def links_report_for_channel(channel):
    """
    Generation du rapport pour le salon
    :param channel:
    :return:
    """
    current_time = datetime.datetime.utcnow()
    seven_days_ago = current_time - datetime.timedelta(days=7)
    link_shared = Link.query.filter_by(channel=channel).filter(Link.date > seven_days_ago).all()

    if link_shared:
        return "Weekly Report : \r\n- {0}".format("\r\n- ".join(link_shared))
    else:
        return None


if SLACK_TOKEN:
    @register_as_command("rapport_lien", "Liste des liens partagés les 7 derniers jours", "Historique des liens")
    def cmd_link_report(attrs):
        """
        Liste des derniers liens partagés dans le salon.
        :param msg:
        :return:
        """
        links_report_for_channel(channel=attrs["channel"])


    @register_as_command("rapport_liens", "Envoi sur l'ensemble des salons les liens partagés sur les 7 derniers jours",
                         "Historique des liens")
    def generate_all_report(attrs):
        """
        Génere la liste des liens pour chaque salons
        :param attrs:
        :return:
        """
        current_time = datetime.datetime.utcnow()
        seven_days_ago = current_time - datetime.timedelta(days=7)
        channels = Link.query.filter(Link.date > seven_days_ago).group_by(Link.channel).all()
        for channel in channels:
            send_direct_message(channel, links_report_for_channel(channel))

        return "OK"
