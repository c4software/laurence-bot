# Mattermost-bot
Un bot simple et sans prétention, pour animer notre salon mattermost interne…

## Requiert   
- Python3
- beautifulsoup4

## Paramétrage
L'ensemble des paramétrage est dans settings.py

## Utilisation
```bash
$ python run.py
Serving BOT on 0.0.0.0 port 5001 ...
```

## Test Curl
```
curl -s -X POST -d "text=test aaa&channel_name=test" http://localhost:5001/ | json_pp
```
