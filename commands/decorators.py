# -*- coding: utf-8 -*-

commands = {}
descriptions = {}

def register_as_command(command_name, description="", group="Global", keywords=[]):
    def wrap(f):
        commands[command_name] = f
        if group not in descriptions:
            descriptions[group] = {}
        descriptions[group][command_name] = description

        # On register les keywords comme des commandes, mais sans associer
        # d’aide car se sont des alias.
        for keyword in keywords:
             commands[keyword] = f

        def wrapped_f(*args):
            f(*args)
        return wrapped_f
    return wrap
