# -*- coding: utf-8 -*-

def cmd_aide(msg):
    from commands import commands
    return "Mot clés disponibles : \r\n- {0}".format("\r\n- ".join(commands.keys()))

def cmd_bonjour(msg):
    return 'Bonjour {0}'.format(msg['user_name'][0])
