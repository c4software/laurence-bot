import os
import datetime
import threading
import time
from commands.libs.decorators import register_as_command
import schedule

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK", None)

if SLACK_TOKEN:
    @register_as_command("rapport_lien", "Liste des liens partagés les 7 derniers jours", "Historique des liens")
    def cmd_link_report(msg):
        """
        Liste des derniers liens partagés dans le salon.
        :param msg:
        :return:
        """