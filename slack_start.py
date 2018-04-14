from slackclient import SlackClient

from commands import *
from commands.libs.decorators import commands, descriptions
from commands.libs.history import add_history
from commands.general import cmd_start
from settings import *

from tools.text import analyze_text_slack
from tools.libs import *

from shared import save_data, clean_data
from emoji import emojize, demojize

import logging, os, sys, atexit, threading, time, re

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
SLACK_TOKEN = os.environ.get("LAURENCE_TOKEN_SLACK")

if not SLACK_TOKEN:
    logging.critical('Token absent (LAURENCE_TOKEN_SLACK="YOUR_TOKEN"')
    sys.exit()

SLACKCLIENT = SlackClient(SLACK_TOKEN)
SLACKBOT_ID = None
USERLIST = {}

def parse_bot_messages(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            return event["text"], event["channel"], event
    return None, None, None

def extract_command_query(commande):
    commande = parse_direct_mention(commande)
    commande = commande.lower().split(' ')
    if commande[0].startswith("/"):
        commande[0] = commande[0][1:]
       
    return commande

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return matches.group(2).strip() if matches else message_text

def handle_command(text, channel, event):
    commande = extract_command_query(text)
    pseudo = get_slack_username(event["user"])
    attrs = analyze_text_slack(make_attrs(pseudo, text, commande[1:], event["channel"], None, {}))

    # Extract data depuis la données analysée.
    commande = extract_command_query(attrs["text"][0])

    if commande[0] in commands:
        retour = commands[commande[0]](attrs)
        if retour != "" and retour is not None:
            if not isinstance(retour, str):
                retour = " ".join(retour)
            post_message(retour, channel)
        else:
            post_message("Désolé, je ne comprend pas encore votre demande…", channel)

def post_message(retour, channel):
    SLACKCLIENT.api_call("chat.postMessage", link_names=1, channel=channel, text=retour)

def get_users_list_slack():
    return {u["id"]:u["name"] for u in SLACKCLIENT.api_call("users.list")["members"]}

def get_slack_username(user_id):
    global USERLIST
    if id in USERLIST:
        return "@{}".format(USERLIST[user_id])
    else:
        USERLIST = get_users_list_slack()
        return get_slack_username(user_id)

if __name__ == "__main__":
    if SLACKCLIENT.rtm_connect(with_team_state=False):
        print("Laurence is ready !")
        SLACKBOT_ID = SLACKCLIENT.api_call("auth.test")["user_id"]
        USERLIST = get_users_list_slack()
        while True:
            MESSAGE, CHANNEL, EVENT = parse_bot_messages(SLACKCLIENT.rtm_read())
            if MESSAGE:
                handle_command(MESSAGE, CHANNEL, EVENT)
            time.sleep(0.5)
