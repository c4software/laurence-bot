from slackclient import SlackClient

from commands import *
from commands.libs.decorators import commands, descriptions
from commands.libs.history import add_history
from commands.general import cmd_start
from models.models import Link
from settings import *

from tools.text import analyze_text_slack
from tools.libs import *

import logging, os, sys, time, re

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
URL_REGEX = "https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK")

if not SLACK_TOKEN:
    logging.critical('Token absent (LAURENCE_TOKEN_SLACK="YOUR_TOKEN"')
    sys.exit()

SLACKCLIENT = SlackClient(SLACK_TOKEN)
SLACKBOT_ID = None
USERLIST = {}


def parse_bot_messages(slack_events):
    for event in slack_events:
        message_type = 'C'
        if "channel" in event and isinstance(event["channel"], str):
            if event["channel"].startswith("C"):
                message_type = 'C'
            elif event["channel"].startswith("D"):
                message_type = "D"
            elif event["channel"].startswith("G"):
                message_type = "G"

        if event["type"] == "message" and not "subtype" in event:
            return event["text"], event["channel"], event, message_type
        elif event["type"] == "message_changed" and "previous_message" in event:
            # FIXME Gestion de l'edition de message (Pour l'instant je retrigger l'event)
            return event["text"], event["channel"], event, message_type

    return None, None, None, None


def extract_command_query(commande, message_type):
    commande = parse_direct_mention(commande, message_type)
    if commande:
        commande = commande.lower().split(' ')
        if commande[0].startswith("/"):
            commande[0] = commande[0][1:]

        return commande
    else:
        return None


def parse_direct_mention(message_text, message_type):
    matches = re.search(MENTION_REGEX, message_text)

    # Si dans un salon et les groupes et pas de pseudo alors on ignore
    if message_type in ["C", "G"] and not matches:
        return ""

    # Sinon on parse et on retire le pseudo du bot.
    return matches.group(2).strip() if matches else message_text


def handle_command(text, channel, event, message_type):
    commande = extract_command_query(text, message_type)

    # On ignore si pas de commande dans le retour
    if commande:
        pseudo = get_slack_username(event["user"])

        # Si c'est autre chose qu'un DM alors on ignore le mode context.
        ignore_context = message_type is not "D"

        # Extract data depuis la données analysée.
        attrs = analyze_text_slack(make_attrs(pseudo, text, commande[1:], event["channel"], None, {}), ignore_context)
        commande = extract_command_query(attrs["text"][0], message_type)
        try:
            if commande[0] in commands:
                retour = commands[commande[0]](attrs)
                if retour != "" and retour is not None:
                    if not isinstance(retour, str):
                        retour = " ".join(retour)
                    post_message(retour, channel)
        except Exception as e:
            print(e)
            pass
    else:
        # C'est pas une commande, alors on cherche a extraire les liens du messages
        links = re.findall(URL_REGEX, text)
        for found_link in links:
            link = Link(found_link, channel)
            db_session.add(link)

        if links:
            print("Found {} link(s) => Saved in DB".format(len(links)))
            react_message(event["ts"], channel, "thumbsup")
            db_session.commit()


def post_message(retour, channel):
    SLACKCLIENT.api_call("chat.postMessage", link_names=1, channel=channel, text=retour)


def react_message(timestamp, channel, name):
    SLACKCLIENT.api_call("reactions.add", channel=channel, name=name, timestamp=timestamp)


def get_users_list_slack():
    client_list = SLACKCLIENT.api_call("users.list")
    if "members" in client_list:
        return {u["id"]: u["name"] for u in client_list["members"]}
    else:
        return {}


def get_slack_username(user_id):
    global USERLIST
    if user_id in USERLIST:
        return "@{}".format(USERLIST[user_id])
    else:
        USERLIST = get_users_list_slack()
        return get_slack_username(user_id)


if __name__ == "__main__":
    if SLACKCLIENT.rtm_connect(with_team_state=False, auto_reconnect=True):
        print("Laurence is ready !")
        SLACKBOT_ID = SLACKCLIENT.api_call("auth.test")["user_id"]
        USERLIST = get_users_list_slack()
        while True:
            MESSAGE, CHANNEL, EVENT, MESSAGE_TYPE = parse_bot_messages(SLACKCLIENT.rtm_read())
            if MESSAGE:
                try:
                    handle_command(MESSAGE, CHANNEL, EVENT, MESSAGE_TYPE)
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
                    pass
