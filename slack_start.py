from slackclient import SlackClient

from commands import *
from commands.libs.decorators import commands, descriptions
from commands.libs.history import add_history
from commands.general import cmd_start
from settings import *

from tools.text import analyze_text
from tools.libs import *

from shared import save_data, clean_data

import random, logging, os, sys, atexit, threading, time, re

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
slack_token = os.environ.get("LAURENCE_TOKEN_SLACK")

sc = SlackClient(slack_token)
starterbot_id = None

def parse_bot_messages(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            return event["text"], event["channel"]
    return None, None

def handle_command(command, channel):
    response = "Pong"
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

if __name__ == "__main__":
    if sc.rtm_connect(with_team_state=False):
        print("Laurence is ready !")
        starterbot_id = sc.api_call("auth.test")["user_id"]
        while True:
            message, channel = parse_bot_messages(sc.rtm_read())
            if message:
                handle_command(message, channel)
            time.sleep(1)