# Laurence-bot

[![Build Status](https://travis-ci.org/c4software/laurence-bot.svg?branch=master)](https://travis-ci.org/c4software/laurence-bot)

![Couverture](https://raw.githubusercontent.com/c4software/laurence-bot/master/test/coverage/coverage.svg)

Un bot simple et sans prétention, pour animer notre salon mattermost / Telegram interne…

## Requiert   
- Python3

## Dépendances
- sqlalchemy
- https://github.com/mailgun/expiringdict/archive/master.zip
- beautifulsoup4
- python-telegram-bot
- https://github.com/MarioVilas/google/archive/master.zip
- emoji
- textblob textblob_fr
- wikipedia
- qhue (https://github.com/quentinsf/qhue)

## Parametrage
L'ensemble des paramétrage est dans settings.py

## Utilisation Mattermost
```bash
$ python mattermost_start.py
Serving Laurence on 0.0.0.0 port 5001 ...
```

## Utilisation Telegram
```bash
$ export LAURENCE_TOKEN="YOUR_TOKEN"
$ python telegram_start.py
Laurence is ready
```


## Test Curl Mattermost
```
curl -s -X POST -d "text=test aaa&channel_name=test" http://localhost:5001/ | json_pp
```
