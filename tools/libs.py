from settings import DEBUG_USER, DEBUG_USER_ID

def is_debug(username):
    return username in DEBUG_USER

def is_telegram(msg):
    return "telegram" in msg

def is_private_channel(update):
    return update.message.chat.type is "private"

def get_username(msg):
    return msg["user_name"][0]

def get_debug_user_id(msg):
    if msg.id and msg.username in DEBUG_USER_ID:
        DEBUG_USER_ID[msg.username] = msg.id

def send_message_debug_user(bot, message=""):
    for user in DEBUG_USER_ID:
        bot.sendMessage(chat_id=DEBUG_USER_ID[user], text=message)

def username_or_channel(attrs):
    if attrs["channel"]:
        pseudo = "channel_{0}".format(attrs["channel"])
    else:
        pseudo = get_username(attrs)

    return pseudo

def get_probable_command(text, bot_name=None):
    commande = text.lower().split(' ')
    commande = commande[0]

    if commande.startswith("/"):
        commande = commande[1:]

    # Suppression du nom du bot exemple /gif@laurence_le_bot
    if bot_name and bot_name in commande:
        commande = commande.replace(bot_name, "").replace(" ", "")

    return commande.lower()

def make_attrs(username, text, args, channel=None, telegram=None):
    attrs = {"user_name": [username], "text": [text], "channel": channel, "query": " ".join(args)}
    if telegram:
        attrs["telegram"] = telegram

    return attrs
