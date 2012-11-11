# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

# Les types d'explosions d'une bille dans l'arène
(EXPLOS_MARBLE_ON_BORDER, # La bille explose toute seule contre le bord d'une tile du jeu.
 EXPLOS_MARBLE_ON_ARENA_LIMIT, # La bille explose toute seule contre le bord de l'arène.
 EXPLOS_MARBLES_ON_TILE, # Plusieurs billes se rencontrent au milieu d'une tile, et explosent.
 EXPLOS_MARBLES_BETWEEN_TILE, # 2 billes se rencontrent entre 2 tiles, et explosent.
 EXPLOS_MARBLE_IN_TRASH, # La bille arrive dans un component spécial qui la fait exploser.
) = range(5)


class MarbleExplosion():
    """
    définit l'explosion d'une ou plusieurs billes dans l'arène. Type MVC : Modèle
    """

    def __init__(self, listMarbleExploded, explosionType):
        """ constructeur
        Entrées : listMarbleExploded : liste d'objet Marble. 
                  Liste des billes impliquées dans l'explosion. (Y'en a une ou plusieurs)
                  explosionType : type de l'explosion. Valeur EXPLOS_*
        """
        self.listMarbleExploded = listMarbleExploded
        self.explosionType = explosionType
