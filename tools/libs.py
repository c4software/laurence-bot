from settings import DEBUG_USER, DEBUG_USER_ID

def is_debug(username):
    return username in DEBUG_USER

def is_telegram(msg):
    return "telegram" in msg

def get_username(msg):
    return msg["user_name"][0]

def get_debug_user_id(msg):
    DEBUG_USER_ID[msg.username] = msg.id

def send_message_debug_user(bot, message=""):
    for user in DEBUG_USER_ID:
        bot.sendMessage(chat_id=DEBUG_USER_ID[user], text=message)
