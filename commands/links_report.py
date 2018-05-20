import os
import datetime
import threading
import time
from commands.libs.decorators import register_as_command
import schedule

from models.models import Link

SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK", None)

if SLACK_TOKEN:
    @register_as_command("rapport_lien", "Liste des liens partagés les 7 derniers jours", "Historique des liens")
    def cmd_link_report(attrs):
        """
        Liste des derniers liens partagés dans le salon.
        :param msg:
        :return:
        """
        current_time = datetime.datetime.utcnow()
        seven_days_ago = current_time - datetime.timedelta(days=7)
        link_shared = Link.query.filter_by(channel=attrs["channel"]).filter(Link.date > seven_days_ago).all()

        if link_shared:
            return "Weekly Report : \r\n- {0}".format("\r\n- ".join(link_shared))
