# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common import pyRect, UP, RIGHT, DOWN, LEFT, DICT_OPPOSITE_DIR
from compgen import ComponentGeneric, COMP_SIMPLE_PIPE

class ComponentSimplePipe(ComponentGeneric):
    """
    Un simple tuyau, avec deux extrémités. Le tuyau peut faire un coude, ou pas.
    Lorsqu'une bille entre par l'une des extrémités, elle ressort par l'autre.
    Chaque extrémité peut donc être une sortie ou une entrée.
    Pas d'envoi ni de réception de commande.
    """

    def __init__(self, pos, dirOne, dirTwo):
        """ Constructeur
        Entrée : pos : osef
                 dirOne, dirTwo : les deux directions des extrémités du tuyau. (UP, DOWN, ...)
                 Il faut obligatoirement les donner dans le sens des aiguilles d'une montre,
                 en commençant par le UP. Sinon la classe qui affiche les components ne va
                 pas s'en sortir. (Je pourrais faire que ça le gère, mais pas envie).
        """
        ComponentGeneric.__init__(self, pos, COMP_SIMPLE_PIPE)
        self.dirOne = dirOne
        self.dirTwo = dirTwo
        self.dirOpposOne = DICT_OPPOSITE_DIR[self.dirOne]
        self.dirOpposTwo = DICT_OPPOSITE_DIR[self.dirTwo]
        # L'endroit d'où vient une bille est la direction opposée de son mouvement.
        # (voir blabla géant de ComponentGeneric). Donc les directions 
        # autorisée pour les billes qui arrivent sont les opposés des extrémités
        # des tuyaus (ou quelque chose comme ça).
        self.authorizedIncomingDir = (self.dirOpposOne, self.dirOpposTwo)

    def handleIncomingMarble(self, marble):
        # Si la bille arrive par l'une des deux extrémités du tuyau, c'est ok.
        # Sinon, elle arrive de nulle part, on devra la fait exploser.
        return marble.moveDir in self.authorizedIncomingDir

    def handlePresentMarble(self, marble):
        # Détermination de la nouvelle direction de la bille.
        if marble.moveDir == self.dirOpposOne:
            # La bille vient de la première extrémité du tuyau. Elle va donc passer dans 
            # la 2ème extrémité. Donc sa direction de mouvement est celle de la 2ème extrémité.
            marble.moveDir = self.dirTwo
        elif marble.moveDir == self.dirOpposTwo:
            # Et vice-et-versaaaaa !!
            marble.moveDir = self.dirOne
