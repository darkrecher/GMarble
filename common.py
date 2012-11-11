# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

import pygame
# Pas d'init de pygame, pas de mode graphique, rien. On n'utilise que les Rect.
# TRODO : faudra d'ailleurs essayer de s'en passer totalement.

# ------------------------- Common -------------------------------------------

# Les directions
# (Peut-être que l'ordre sera important. On sait pas.)
# TODO : utiliser un genre d'enum.
(NO_MOVE,
 UP,
 RIGHT,
 DOWN,
 LEFT,
) = range(5)

# Offset de déplacement en fonction des directions.
# Strange, car on utilise ce même dico d'offset pour l'arena et pour le screen. Mais ça se tient.
DICT_OFFSET_FROM_DIR = {
 NO_MOVE : ( 0,  0),
 UP      : ( 0, -1),
 RIGHT   : (+1,  0),
 DOWN    : ( 0, +1),
 LEFT    : (-1,  0),
}

# Directions opposée en fonction des directions pas-opposée
DICT_OPPOSITE_DIR = {
 NO_MOVE : NO_MOVE,
 UP      : DOWN,
 RIGHT   : LEFT,
 DOWN    : UP,
 LEFT    : RIGHT,
}


def pyRect(left=0, top=0, width=0, height=0):
    """
    permet de générer un pygame.Rect, sans forcément donner la hauteur et la largeur.
    pourquoi ils ont pas mis eux-même des valeurs par défaut bordel !!
    (ou alors c'est moi qui suis à la masse et j'ai loupé une astuce.)
    """
    return pygame.Rect(left, top, width, height)
