# -*- coding: utf-8 -*-
from .decorators import register_as_command

@register_as_command("aide")
def cmd_aide(msg):
    from .decorators import commands
    return "Mot clés disponibles : \r\n- {0}".format("\r\n- ".join(commands.keys()))

@register_as_command("bonjour")
def cmd_bonjour(msg):
    return 'Bonjour {0}'.format(msg['user_name'][0])
