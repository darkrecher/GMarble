# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common import DICT_OFFSET_FROM_DIR

# Couleur des billes.
(MARBLE_COLOR_BLACK,
) = range(1)
    

class Marble():
    """
    Une bille du jeu. Type MVC : Modèle
    """

    def __init__(self, pos, startMoveDir, color=MARBLE_COLOR_BLACK):
        """ constructeur
        Entrée : pos : position (X, Y)
                 startMoveDir : direction initiale du mouvement de la bille. (NO_MOVE, UP, ...)
                 color : couleur de la bille
        """
        self.pos = pos
        self.moveDir = startMoveDir
        self.color = color
        # Position de la bille dans l'arène, après le prochain cycle de jeu. 
        # (Si tout se passe normalement, car elle peut exploser entre temps)
        self.posFuture = None

    def determinePosFuture(self):
        """
        Détermine la future position de la bille, dans l'arène.
        Sortie : position (X, Y) de la bille, après le prochain cycle de jeu.
        """
        # On ajoute l'offset de déplacement de la direction de la bille, à sa position actuelle.
        offsetMovement = DICT_OFFSET_FROM_DIR[self.moveDir]
        self.posFuture = self.pos.move(offsetMovement)

    def doMovement(self):
        """
        Déplace la bille sur sa position future, dans l'arène. (On lui fait faire un cycle de jeu)
        """
        self.pos = self.posFuture
        self.posFuture = None
