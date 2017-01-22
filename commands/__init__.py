# -*- coding: utf-8 -*-
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")

"""
    Initialisation de toutes les commandes lors de l’import du module
"""

__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
