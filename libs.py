# -*- coding: utf-8 -*-

def make_message(username, icon_url, fallback, pretext, title, title_link, text, color="#7CD197"):
    return {"username": username, "icon_url":icon_url, "attachments": [{"fallback": fallback, "pretext": pretext, "title": title, "title_link": title_link, "text": text, "color": color}]}
