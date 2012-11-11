# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

class SimpleSprite():
    """
    Sprite tout simple. Il ne bouge pas. Il gère juste une succession d'image.
    Y'a pas de fonctions d'affichage du sprite sur une surface ou un écran. Seulement une fonction
    de renvoi de l'image en cours. L'affichage en lui-même doit être géré par le code extérieur.
    Type MVC : Vue (bas niveau)
    """
    def __init__(self, posScreen, listImgInfo):
        """ Constructeur
        Entrées : posScreen : position (X, Y) du coin haut-gauche du sprite à l'écran.
                  listImgInfo : liste de tuples de 2 élèm définissant une suite d'images.
                                (voir descrip détaillée au début de ce fichier de code)
        """
        self.posScreen = posScreen
        self.listImgInfo = listImgInfo
        # Curseur pointant sur un élément de self.listImgInfo
        self.currentImgCursor = 0
        # timer indiquant le nombre de cycle d'animation avant le prochain changement d'image.
        self.imgTimer = self.listImgInfo[self.currentImgCursor][0]


    def getCurrentImg(self):
        """
        renvoie l'image en cours à afficher.
        Sortie : liste de strings, à écrire sur un écran à la position (X, Y) du sprite.
        """
        return self.listImgInfo[self.currentImgCursor][1]


    def advanceTimer(self):
        """
        Fait avancer le sprite d'un cycle d'animation.
        Sortie : booléen. True : l'avancement de cycle a fait que le sprite a avancé d'une image
                                 Donc y'a un rafraîchissement à faire.
                          False : l'avancement n'a pas fait changer l'image du sprite. Donc osef.
        """
        # Si on est arrivé à la dernière image, le timer vaut -1. Rien à faire.
        if self.imgTimer == -1:
            return False

        self.imgTimer -= 1

        if self.imgTimer == 0:
            # Il faut passer à l'image suivante.
            self.currentImgCursor += 1
            # On remet le timer à jour, pour qu'il décompte le temps de la nouvelle image.
            # (self.imgTimer peut être devenu -1 à ce moment là, et c'est cool)
            self.imgTimer = self.listImgInfo[self.currentImgCursor][0]
            # Y'a eu changement d'image
            return True
        else:
            # Il ne s'est rien passé de spécial. Pas de changement d'image.
            return False
