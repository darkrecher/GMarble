# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common import pyRect

# ------------------------- Common au display---------------------------------

# Hauteur et largeur (en caractère de mode texte) d'une tile du jeu.
# C'est plus large que haut, pour vaguement essayer d'avoir des tiles carrés 
# dans un mode texte classique.
TILE_WIDTH = 4
TILE_HEIGHT = 3

def posScreenFromPosArenaTile(posArena):
    """
    Position à l'écran du coin haut-gauche d'une tile. 
    Entrée : position (X, Y) de la tile dans l'arène.
    Sortie : position (X, Y) à l'écran, en caractère, du coin haut-gauche de la tile.
    """
    # Décalage de (1, 1) à cause de la bordure de l'arène.
    # Re-décalage de (1, 0) à cause de la colonne de caractère espace à gauche de l'arène.
    # (Voir explication dans ArenaDisplayer pour savoir d'où vient cette colonne d'espace).
    return pyRect(posArena.x * TILE_WIDTH + 2,
                  posArena.y * TILE_HEIGHT + 1)


def posScreenFromPosArenaMarble(posArena):
    """
    Position à l'écran d'une marble dans une tile, lorsqu'elle n'est pas en train
    de se déplacer d'une tile à une autre. (C'est à dire qu'elle est au milieu de la tile). 
    Entrée : position (X, Y) de la tile dans l'arène.
    Sortie : position (X, Y) à l'écran, en caractère, de la marble.
    """
    # Même décalage que pour posScreenFromPosArenaTile
    # Re-re-décalage de (1, 1) pour placer la marble à peu près au milieu du Component.
    return pyRect(posArena.x * TILE_WIDTH + 3,
                  posArena.y * TILE_HEIGHT + 2)
