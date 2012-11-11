# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from compgen import ComponentGeneric, COMP_NOTHING


class ComponentNothing(ComponentGeneric):
    """ 
    Component avec rien dedans. 
    Il n'autorise le passage d'aucune bille (y'a pas de tuyau). Il n'envoie aucune commande.
    Il ne fait jamais rien lorsqu'il reçoit une commande, quelle qu'elle soye. C'est un boulet.
    """
    pass
