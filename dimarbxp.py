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
from marblexp import EXPLOS_MARBLE_ON_BORDER
from disptext import posScreenFromPosArenaMarble
from simpspri import SimpleSprite

# Définitions d'une suite d'image, pour des sprites. Liste de tuple de 2 éléments :
#  - int : Temps, en nombre de cycle d'animation, durant lequel on affiche cette image du sprite.
#  - liste de string : Image à afficher. 
#                      On affiche les strings ligne par ligne, à partir d'une position X, Y donnée.
# Pour la dernière image, c'est obligé de mettre un temps de -1, et c'est cette image qui restera,
# tant que le sprite est affiché. Si on met pas -1, ça plante.
# Pour que le sprite n'affiche rien, on peut mettre une liste de string vide (avec 0 elem)
# dans une image. On peut faire ça y compris pour la dernière image.

# Explosion verticale (d'une bille contre le bord de quelque chose)
EXPLOS_VERTIC = (( 3, (" ",
                       "*",
                       " ")),
                 ( 3, ("*",
                       "*",
                       "*")),
                 ( 3, ("*",
                       " ",
                       "*")),
                 (-1, ()),
                )

# Explosion horizontale (d'une bille contre le bord de quelque chose)
EXPLOS_HORIZ = (( 3, (" * ", )),
                ( 3, ("***", )),
                ( 3, ("* *", )),
                (-1, ()),
               )

# Dictionnaire donnant les infos d'affichage d'une explosion de type EXPLOS_MARBLE_ON_BORDER.
# Pour afficher l'explosion d'une bille contre un bord de tile ou un bord d'arène, on commence
# par afficher, pendant quelques cycles d'animation, la bille qui se déplace normalement.
# Puis, à un moment donné, on n'affiche plus la bille, mais on affiche un simpleSprite 
# représentant l'explosion de cette bille. La position de ce simpleSprite se détermine
# selon la position de la bille dans l'arène, et du petit bout de déplacement qu'elle a fait.
# Ensuite, on n'affiche ni la bille, ni l'explosion. Et tout a disparu. Crac !
#
# TRODO : faut s'arranger pour que ce soit pareil pour les autres types d'explosions. 
# Et du coup, le blabla ci-dessus s'appliquera à toutes les explosions. 
# Pas que EXPLOS_MARBLE_ON_BORDER
#
# clé du dictionnaire : direction de déplacement de la bille avant qu'elle n'explose.
# valeur : tuple de 3 élément :
#           - temps, en nb de cycle d'animation, avant de faire apparaître l'explosion
#             et de cacher la/les billes qui explosent. 
#           - offset de déplacement entre la position de la bille à l'écran, lorsqu'elle
#             était au milieu de sa tile de départ, et le coin haut-gauche de l'explosion.
#             cet offset tient compte du petit déplacement de la bille avant explosion, ainsi que
#             de la taille de l'image d'explosion (transition centre -> coin haut-gauche).
#           - liste d'imgInfo représentant les images de l'explosion.
DICT_INFO_FROM_EXPLOS_ON_BORDER_DIR = {
    UP    : (12, ( -1, -1), EXPLOS_HORIZ),
    DOWN  : (12, ( -1, +1), EXPLOS_HORIZ),
    LEFT  : (12, ( -1, -1), EXPLOS_VERTIC),
    RIGHT : (16, ( +2, -1), EXPLOS_VERTIC),
}


class MarbleExplosionDisplayer():
    """
    Class qui gère les infos concernant l'affichage d'une explosion d'une bille.
    Type MVC : Vue (haut niveau)
    """

    def __init__(self, marbleExplosion):
        """ constructeur
        Entrées : marbleExplosion : instance d'une classe MarbleExplosion
        """
        self.marbleExplosion = marbleExplosion
        explosionType = marbleExplosion.explosionType

        if explosionType == EXPLOS_MARBLE_ON_BORDER:

            # Récupération de la direction de déplacement de la bille avant qu'elle n'explose.
            marbleMoveDir = marbleExplosion.listMarbleExploded[0].moveDir
            # Récupération des informations sur l'explosion de la bille.
            explosionInfo = DICT_INFO_FROM_EXPLOS_ON_BORDER_DIR[marbleMoveDir]
            self.waitLimit, self.offsetPos, listImgInfo = explosionInfo
            # Détermination de la position de l'explosion, en fonction de la position de la bille,
            # et des infos sur l'explosion.
            marblePos = marbleExplosion.listMarbleExploded[0].pos
            marblePosScreen = posScreenFromPosArenaMarble(marblePos)
            posScreen = marblePosScreen.move(self.offsetPos)
            # Création du SimpleSprite représentant l'explosion, qu'il faudra afficher
            # dans l'arène le moment venu. (C'est à dire après self.waitLimit cycles d'anim).
            self.simpleSprExplosion = SimpleSprite(posScreen, listImgInfo)

        else:
            print "autres types d'explosion pas encore fait"
            assert False
