from rest import callrest


def launch_stop():
    try:
        data = callrest(domain="vbr.dev", port=8000, ssl=False, path="/stop", params={})[2]
        return "ok"
    except Exception as e:
        print (e)
        return "Erreur"


def launch_play(params):
    try:
        data = callrest(domain="vbr.dev", port=8000, ssl=False, path="/play", params=params)[2]
        return "ok"
    except Exception as e:
        print (e)
        return "Erreur"


def cmd_stop(msg):
    return launch_stop()


def cmd_play(msg):
    params = {"file": msg.split(' ')[1]}
    return launch_play(params)
