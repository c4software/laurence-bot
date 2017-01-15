from settings import DEBUG_USER

def is_debug(username):
    return username in DEBUG_USER

def is_telegram(msg):
    return "telegram" in msg

def get_username(msg):
    return msg["user_name"][0]
