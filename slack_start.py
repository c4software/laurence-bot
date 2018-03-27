from slackclient import SlackClient

from commands import *
from commands.libs.decorators import commands, descriptions
from commands.libs.history import add_history
from commands.general import cmd_start
from settings import *

from tools.text import analyze_text
from tools.libs import *

from shared import save_data, clean_data

import random, logging, os, sys, atexit, threading

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


slack_token = os.environ["LAURENCE_TOKEN_SLACK"]
sc = SlackClient(slack_token)