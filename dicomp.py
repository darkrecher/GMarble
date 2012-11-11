# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common   import UP, RIGHT, DOWN, LEFT
from compgen  import COMP_NOTHING, COMP_SIMPLE_PIPE

"""
Bibliothèque contenant tout le code pour déterminer les images des Components, qu'on peut
afficher à l'écran. Dans ce mode d'affichage (tout pourri, en mode texte), une image
de Component est constituée d'un rectangle de 4 caractères de large sur 3 de haut.
Les caractères, c'est ce qu'on veut. Mais vaut mieux rester dans de l'ascii, quand même.
Sinon ça risque de poser problème sur des consoles tordues (genre Mac).

Donc une image de Component est constituée d'une liste de 3 éléments (un élément = une ligne 
de caractères), chacun de ces élément est une string ascii de 4 caractères.

J'ai choisi 4 par 3, car les caractères sont plus haut que large. Ce qui permet de compenser un
peu et d'afficher des Components presque carrés.
Lorsqu'on veut afficher une marble sur un composant, on la place sur la 2ème ligne (centrée
verticalement), et la 2ème colonne (pas centrée horizontalement, mais on peut pas faire mieux).

Donc pour toutes les images de Components, les chemins verticaux doivent tous être dessinés 
sur la 2ème colonne de caractères. sinon ça sera moche-bizarre.
"""

# Image du ComponentNothing
IMG_NOTHING = ("    ", ) * 3

# --- Images des Components de type Simple Pipe ---
# On a les tuyaux droits, et toutes les possibilités de tuyaux coudés (CORN = cornered).
# Trip : on a gagné monsieur Cornard !

IMG_VERTIC = (" |  ",
              " |  ",
              " |  ")

IMG_HORIZ = ("    ",
             "----",
             "    ")

IMG_CORN_1 = (" |  ",
              " \--",
              "    ")

IMG_CORN_2 = ("    ",
              " /--",
              " |  ")

IMG_CORN_3 = ("    ",
              "-\  ",
              " |  ")

IMG_CORN_4 = (" |  ",
              "-/  ",
              "    ")

# Dictionnaire de correspondance pour les images de Component de type Simple Pipe.
# clé : tuple de 2 éléments : les directions des 2 extrémités du Simple Pipe.
#       Comme dit plus haut, elles sont indiqués dans le sens des aiguilles d'une montre,
#       en commençant par le UP. J'aurais pu ajouter les autres possibilités dans le dico,
#       mais pas envie, et de toutes façons pas besoin. Faut juste pas se vautrer quand on 
#       crée un objet Simple Pipe.
# valeur : image (liste de string). L'image du Simple Pipe, quoi.
DICT_IMG_FROM_SIMPLE_PIPE_DIR = {
   (UP, RIGHT)   : IMG_CORN_1,
   (UP, DOWN)    : IMG_VERTIC,
   (UP, LEFT)    : IMG_CORN_4,
   (RIGHT, DOWN) : IMG_CORN_2,
   (RIGHT, LEFT) : IMG_HORIZ,
   (DOWN, LEFT)  : IMG_CORN_3,
}


class ComponentDisplayer():
    """
    Classe renvoyant l'image d'un Component à afficher dans l'arène. (ou ailleurs, d'ailleurs).
    Type MVC : Vue (haut niveau)
    TRODO : Euh... en fait ça vaut pas le coup de faire une classe pour ça. Y'a juste besoin
    d'une fonction. Et éventuellement de sous-fonction. On verra si on change.
    """
    def imgFromComponent(self, component):
        """
        Renvoie l'image d'un Component.
        Entrées : component : objet de type Component, ou d'une classé dérivée.
        Sorties : image (liste de caractères) A priori, de 3 lignes et 4 colonnes,
                  mais en théorie, osef. Donc on vérifie pas la taille.
        """
        if component.compType == COMP_SIMPLE_PIPE:
            # Le Component est un Simple Pipe. On peut déterminer l'image correspondante,
            # à partir de la direction des 2 extrémités du Simple Pipe.
            keyPipe = (component.dirOne, component.dirTwo)
            return DICT_IMG_FROM_SIMPLE_PIPE_DIR[keyPipe]
        else:
            # Pour les ComponentNothing, et les Component pas encore géré,
            # on renvoie une image vide (avec que des caractères espaces dedans)
            return IMG_NOTHING
