# -*- coding: utf-8 -*-

# Liste des commandes et des descriptions associés
commands = {}
descriptions = {}


# Décorateurs pour les fonctions
def register_as_command(command_name, description="", group="Global", keywords=[]):
    """
    Décorateurs des fonction

    Parameters:
      :param command_name: Nom de la commande.
      :param description: Description de la fonction (utilisé dans l’aide). Si pas de texte alors n’aparait pas.
      :param group: Groupement à l’affichage de l’aide.
      :param keywords: Tableau d’alias à la commande.
    """

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
