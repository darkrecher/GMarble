# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common   import (pyRect, NO_MOVE, UP, RIGHT, DOWN, LEFT, 
                      DICT_OFFSET_FROM_DIR)
from disptext import posScreenFromPosArenaMarble
from dicomp   import ComponentDisplayer

"""
Construction de l'image représentant une Arena, et animation des trucs animés dans l'arena.
Cette classe contient une grande liste de grande string, contenant l'image de l'Arena.
Taille de la liste = hauteur de l'image.
Taille d'une string de la liste = largeur de l'image. Toutes les strings ont la même taille.

La classe est chargée de mettre à jour cette image, en fonction de ce qu'elle trouve dans la
classe-Modèle Arena.
Le code extérieur est chargé de faire l'affichage effectif de l'image (sur la sortie standard,
dans un fichier, en rafraîchissement dans la console, ...).

L'image se présente sous cette gueule. Pour une arena de largeur 3, hauteur 2 : 
BBBBBBBBBBBBBBB 
B Co11Co12Co13B
B Co11Co12Co13B
B Co11Co12Co13B
B Co21Co22Co23B
B Co21Co22Co23B
B Co21Co22Co23B
BBBBBBBBBBBBBBB

B = les caractères de bordures, pour délimiter l'arène. (J'ai choisi le caractère ")
Co11 : image du Component en haut à gauche. Co12 : image du Component d'à côté, etc...
Il y a un espace entre la bordure de gauche et les images des Components. C'est pour compenser 
le fait que les tuyaux verticaux des Components sont un peu décalés vers la gauche.
Comme ça, on a l'impression que les tuyaux verticaux sont bien centrés. Ha ha !

Cette classe gère donc les trucs suivants : 
 - Récupération des images des Components, et "blit" de ces images dans celle de l'arène
 - Détermination de la position des marbles dans l'image de l'arène, affichage de ces marbles
 - Pour les marbles en mouvement : détermination des positions intermédiaires de ces marbles
   (pour passer d'un Component à l'autre).
 - détermination de la position et de l'image des explosions de marble, et affichage.
 - Globalement : gestion des cycles d'animation. Détermination de l'image globale de l'arène
   à chacun de ces cycles. Indication si quelque chose a changé dans l'image par rapport
   au cycle précédent.
 
TRODO : séparer cette classe en 2. SurfaceText (bas niveau, avec les blits), et ArenaDisplayer.
ArenaDiplsayer contiendra une SurfaceText
"""

# TRODO : enlever ce truc qu'a rien à faire ici.
import pygame
from disptext import TILE_WIDTH, TILE_HEIGHT, posScreenFromPosArenaTile
from dimarbxp import MarbleExplosionDisplayer

# Caractère pour afficher les bords de l'arène
CHAR_BORDER = "\""
# Caractère d'initialisation de toute l'arène. (Avant d'afficher les Component et tout le reste).
CHAR_VOID = " "
# Image d'une marble. Là, c'est une image de taille 1*1.
IMG_MARBLE = ["O", ]
# Nombre de cycle d'animation pour décrire ce qu'il se passe dans un cycle de jeu.
# Les cycles d'anim seront numérotés de 0 à (NB_ANIM_CYCLE_PER_GAME_CYCLE-1)
NB_ANIM_CYCLE_PER_GAME_CYCLE = 25

# Période de déplacement des marbles (caractère par caractère). 
# Quand une marble bouge horizontalement, elle doit se déplacer de 4 caractères (largeur d'un
# Component). Donc (période=6) * (distance=4) = 24 = numéro du dernier cycle d'anim
# Quand une marble bouge verticalement, elle doit se déplacer de 3 caractères (hauteur d'un
# Component). Donc (période=8) * (distance=3) = 24 = numéro du dernier cycle d'anim aussi.
DICT_ANIM_PERIOD_FROM_DIR = {
 UP       : 8,
 RIGHT    : 6,
 DOWN     : 8,
 LEFT     : 6,
}


class ArenaDisplayer():
    """
    Classe affichant l'état actuel d'une arène. Et les différentes étapes intermédiaires 
    ( = cycles d'animation) pour passer d'un état à un autre.
    Type MVC : Vue. (Haut et Bas niveau en même temps). D'ailleurs si on peu séparer...
    """

    def __init__(self, arena):
        """ Constructeur
        Entrée : arena : objet de type Arena. C'est l'arène à afficher.
        """
        self.arena = arena
        self.componentDisplayer = ComponentDisplayer()

        # Création des strings composant les lignes de l'image de l'arène. 
        # Puis création de l'image elle-même.
        lineMiddle = "".join((CHAR_BORDER,
                              CHAR_VOID * (self.arena.width * TILE_WIDTH + 1),
                              CHAR_BORDER))

        lineTopBottom = CHAR_BORDER * len(lineMiddle)
        
        screenMiddle = [lineMiddle, ] * (self.arena.height * TILE_HEIGHT)
        self.screen = [lineTopBottom, ] + screenMiddle + [lineTopBottom, ]
        # Récupération de la taille de l'image (en caractère), maintenant que l'image est faite.
        self.screenWidth = len(self.screen[0])
        self.screenHeight = len(self.screen)

        # Liste des informations décrivant chaque mouvement de marble. 
        # C'est une liste de tuple de 4 éléments : 
        # - Référence vers l'objet marble qui est en mouvement
        # - Rect. Position actuelle, à l'écran de la marble. Donc les coord sont en caractères.
        # - Tuple(X, Y), en caractère. Offset à appliquer à la position de la marble,
        #   à chaque fois qu'elle doit bouger. C'est (0, 1), (0, -1), (1, 0) ou (-1, 0)
        # - Int. Période de déplacement de la marble.
        self.listMovMarbleInfo = []
        # liste de Rect. Positions (dans l'arène, pas en caractères) des Components à
        # réafficher durant les cycles d'animations du cycle de jeu en cours. 
        # Lorsqu'une marble se déplace, (en explosant ou pas), on doit réafficher le Component
        # de départ et celui d'arrivée. Ah que sinon ça fait des "traces".
        # TRODO : d'autres réaffichages à prévoir, par exemple quand y'aura les commandes.
        self.listPosTileToRefresh = []
        # Liste d'objet Marble. Elles doivent toute être mentionnées dans au moins un élément
        # de self.listMovMarbleInfo (sinon ça sert à rien).
        # Ce sont les marbles qu'il ne faut PAS afficher (pour une raison ou pour une autre). 
        # En général, la raison c'est que la marble vient d'exploser. 
        # Donc on doit afficher les images de son explosion, mais plus la marble elle-même. 
        self.listMarbleHidden = []
        # Liste d'objet de type SimpleSprite. Il faut les afficher et faire avancer leur animation
        # à chaque cycle d'anim. Contient les SimpleSprite des explosions (et peut-être d'autres
        # trucs plus tard).
        self.listSimpleSprite = []
        # Liste d'objet de type marbleExplosionDisplayer. C'est les explosions à afficher pour
        # les cycles d'animations du cycle de jeu en cours.
        self.listMarbleExplosionDisplayer = []
        # Compteur indiquant l'index du cycle d'animation en cours. 
        # Varie de 0 à (NB_ANIM_CYCLE_PER_GAME_CYCLE-1)        
        self.animationCounter = 0


    def blitSlice(self, posScreen, strSlice):
        """
        blitte un morceau de ligne de caractère, sur la grande image principale de l'arène.
        Entrées : posScreen : Rect. Position sur l'image d'arrivée, en caractère, 
                              du morceau à blitter.
                  strSlice : string. Ligne à blitter. Elle peut avoir n'importe quelle longueur.
                             Pas de verif ni de tronquage si la longueur est trop grande.
                             Donc si on fait pas gaffe, on peut se retrouver avec 
                             une image d'arène mal foutue, comportant des string dont la 
                             longueur dépasse self.screenWidth
        """
        strSrc = self.screen[posScreen.y]

        # On peut pas réécrire les caractères un par un. Donc on compose 
        # la nouvelle ligne de l'image. Avec : le début de la ligne initiale (qui ne change pas),
        # le nouveau morceau de ligne et la fin de la ligne initiale (qui ne change pas non plus).
        strDest = "".join((strSrc[:posScreen.x],
                           strSlice,
                           strSrc[posScreen.x+len(strSlice):]))

        self.screen[posScreen.y] = strDest


    def blitImg(self, posScreen, img):
        """
        blitte une image sur la grande image principale de l'arène.
        Entrées : posScreen : Rect. Position sur l'image d'arrivée, en caractère, 
                              du coin haut-gauche de l'image à blitter.
                  img : image à blitter. (liste de string). Les strings composant cette image
                        peuvent avoir des tailles différentes, osef. (Même si ça serait zarbi).
                        Pas de verif ni de tronquage si la longueur d'une des string 
                        est trop grande. (voir description de bitSlice)
        """
        # clonage du Rect contenant les coordonnées de destination du blittage. Car on va
        # le modifier au fur et à mesure qu'on blitte.
        posScreenLocal = pyRect(posScreen.left, posScreen.top)
        # Blittage des lignes de caractère composant l'image, les unes après les autres.
        # A chaque blittage de ligne, on descend d'un caractère pour la ligne suivante.
        for strSlice in img:
            self.blitSlice(posScreenLocal, strSlice)
            posScreenLocal.move_ip((0, +1))


    def refreshAllScreen(self):
        """
        Réactualise tout le contenu de la grande image de l'arène.
        Attention ! Cette fonction ne doit pas être appelée pendant qu'on est en train
        de dérouler des cycles d'animation. Car ça n'afficherait pas tout comme il faut.
        On ne doit l'appeler que pendant la résolution d'un cycle de jeu.
        La fonction réaffiche tous les Components, et toutes les marbles.
        """
        # On parcourt tous les Component de l'arène
        # TRODO : need a crawler, pour parcourir plus classieusement ?
        for y in xrange(self.arena.height):
            for x in xrange(self.arena.width):
                posArena = pyRect(x, y)
                posScreen = posScreenFromPosArenaTile(posArena)
                component = self.arena.getComponent(posArena)
                # Détermination de l'image correspondant au Component en cours à afficher.
                # not TRODO : on pourrait garder ces images en mémoire, quelque part. Pour
                # ne pas avoir à redéterminer l'image à chaque fois. On va pas le faire, car ça
                # ralentit pas trop (on est en mode texte !). De plus, certaines images de
                # Components pourront changer au cours du jeu. (ex : switch, reset, ...)
                img = self.componentDisplayer.imgFromComponent(component)
                # Blit de l'image du Component sur l'image principale de l'arène.
                self.blitImg(posScreen, img)

        # On parcourt toutes les marbles de l'arène, et on les affiche.
        # On tient pas compte des marble hidden, ni des marble en mouvement. Il est pas
        # censé y avoir ce genre de trucs lorsqu'on n'est pas en train de dérouler une anim.
        for marble in self.arena.listMarble:
            posScreen = posScreenFromPosArenaMarble(marble.pos)
            self.blitImg(posScreen, IMG_MARBLE)

        # On parcourt tous les SimpleSprite, et on les affiche.
        # En fait ça sert à rien mais pour l'instant. Car pas de SimpleSprite si pas pendant
        # une anim. Mais peut-être pour plus tard.
        for simpleSprite in self.listSimpleSprite:
            self.blitImg(simpleSprite.posScreen, simpleSprite.getCurrentImg())
            

    def initAnimation(self):
        """
        Initialise un début d'animation, qui décrira le passage d'un état de jeu à un autre
        (c'est à dire un cycle de jeu).
        Cette fonction consulte les infos qu'il y a dans self.arena, et en déduit les mouvements
        de bille, les explosions, etc. qu'il faut afficher et animer.
        """
        # Réinitialisation d'un tas de trucs
        self.listMovMarbleInfo = []
        self.listPosTileToRefresh = []
        self.listMarbleHidden = []
        self.listSimpleSprite = []
        self.animationCounter = 0

        #On parcourt toutes les marbles de l'arena, on s'intéresse à celles qui sont en mouvement.
        for marble in self.arena.listMarble:
            if marble.moveDir != NO_MOVE:
                
                # On déduit les informations décrivant le mouvement de la marble
                posScreen = posScreenFromPosArenaMarble(marble.pos)

                movMarbleInfo = (marble,
                                 posScreen,
                                 DICT_OFFSET_FROM_DIR[marble.moveDir],
                                 DICT_ANIM_PERIOD_FROM_DIR[marble.moveDir])

                # Et on ajoute ces infos déduites dans self.listMovMarbleInfo.
                self.listMovMarbleInfo.append(movMarbleInfo)
                # Au passage, on complète la liste des Components qui devront être réaffichés
                # lors de l'animation du mouvement de la marble. (Y'a le component de départ
                # de la marble, et le component d'arrivée).
                # TRODO : si plusieurs marbles proches, on risque d'ajouter plusieurs fois 
                # les mêmes positions de Component. C'est crétin. A optimiser.
                self.listPosTileToRefresh.append(marble.pos)
                self.listPosTileToRefresh.append(marble.posFuture)

        # Détermination des marbleExplosionDisplayer, à partir de la liste des marbleExplosion
        # actuellement présentes dans l'arène.
        self.listMarbleExplosionDisplayer = [
            # Les objets marbleExplosionDisplayer ainsi créés contiennent un simpleSprite,
            # représentant l'animation de l'explosion. Mais ce simpleSprite n'est pas affiché
            # ni animé tout de suite. Il ne le sera pas tant qu'il ne sera pas placé dans la
            # liste self.listSimpleSprite. Cette action est faite plus tard 
            # (voir advanceAnimationCounter)
            MarbleExplosionDisplayer(marbleExplosion)
            for marbleExplosion in self.arena.listMarbleExplosion ]


    def advanceAnimationCounter(self):
        """
        Fait avancer d'un cycle d'animation.
        Remet à jour les diverses infos et bazar d'affichage rapport à cet avancement.
        Sortie : Boolean. False : Il n'y a eu aucune modification dans l'image principale
                                  de l'arène, suite à cet avancement d'un cycle d'anim.
                          True : Il y a eu des modifs
        """
        self.animationCounter += 1
        somethingChanged = False

        # On parcourt les simpleSprite en cours, et on les fait avancer d'un cycle d'anim,
        # eux aussi.
        for simpleSprite in self.listSimpleSprite:
            # Si l'image du simpleSprite a changée, la fonction advanceTimer renverra True.
            # Dans ce cas, on doit propager cette notification de changement à l'image de l'arène.
            if simpleSprite.advanceTimer():
                somethingChanged = True

        # On parcourt tous les éléments décrivant les mouvements de marble.
        for movMarbleInfo in self.listMovMarbleInfo:
            # Récupération des infos décrivant un mouvement de une marble.
            marble, posScreen, offsetMove, periodMove = movMarbleInfo
            # On vérifie si la marble ne doit pas être cachée, et si on a atteint
            # la période (en cycle d'anim) de réalisation d'un déplacement.
            if (marble not in self.listMarbleHidden
                and self.animationCounter % periodMove == 0):
                # On déplace un petit peu la marble à l'écran. (de un caractère, à priori)
                posScreen.move_ip(offsetMove)
                # Vu que y'a eu mouvement, l'image principale a changée.
                somethingChanged = True

        # On parcourt tous les marbleExplosionDisplayer en cours. Pour chacun d'eux on vérifie
        # si le temps d'attente (en cycle d'anim) avant l'apparition de l'explosion a été
        # atteint ou pas.
        for marbExpDisp in self.listMarbleExplosionDisplayer:
            if self.animationCounter == marbExpDisp.waitLimit:
                # Le temps a été atteint. On ne doit plus afficher la/les marbles
                # liés à cette explosion de marble.
                for marble in marbExpDisp.marbleExplosion.listMarbleExploded:
                    self.listMarbleHidden.append(marble)
                # Mais on doit afficher l'explosion en elle-même. On ajoute le simpleSprite
                # représentant cette explosion dans la liste des simpleSprite à afficher et
                # à faire avancer à chaque cycle d'anim. Le ArenaDisplayer va s'occuper
                # tout seul, et automatiquement, de ces simpleSprites. (D'ailleurs, c'est
                # le code situé au début de cette fonction qui le gère)
                self.listSimpleSprite.append(marbExpDisp.simpleSprExplosion)
                # Vu que cachage de bille et affichage d'explosion, l'image principale a changée.
                somethingChanged = True

        return somethingChanged


    def refreshAnimation(self):
        """
        Met à jour l'image principale de l'arène, lorsque l'avancement d'un (ou plusieurs)
        cycle d'animation a fait que l'image doit être changée.
        La fonction ne rafraîchit pas toute l'arène. Mais elle rafraîchit toutes les zones
        comportant des éléments animés, qu'elles ait changée ou pas.
        Ex : supposons une arène avec 2 marbles, l'une qui bouge horizontalement, l'autre
        verticalement. On avance d'un cycle d'anim, ça fait déplacer la marble bougeant
        horizontalement. Mais pas l'autre.
        Eh bien cette fonction va rafraîchir les deux zones à rafraîchir, concernant ces
        deux marbles.
        not TRODO : On pourrait optimiser en ne rafraîchissant vraiment que le strict
        nécessaire. Mais pas envie, et pas trop besoin. C'est pas ça qui va niquer les 
        performances. (Nous sommes en fucking mode texte, je rappelle).
        """
        # Rafraîchissement de toutes les images des Components dont les positions sont
        # mentionnés dans self.listPosTileToRefresh.
        for posArena in self.listPosTileToRefresh:
            posScreen = posScreenFromPosArenaTile(posArena)
            component = self.arena.getComponent(posArena)
            img = self.componentDisplayer.imgFromComponent(component)
            self.blitImg(posScreen, img)

        # Rafraîchissement de toutes les marbles en mouvement, et qui ne font pas partie
        # de la liste des marbles à cacher.
        # On parcourt tous les éléments décrivant les mouvements de marble.
        for movMarbleInfo in self.listMovMarbleInfo:
            # Je récupère pas d'un coup toutes les infos décrivant un mouvement de marble.
            # Car je n'ai pas besoin de tout. (L'offset de déplacement et la période : osef).
            marble = movMarbleInfo[0]
            if marble not in self.listMarbleHidden:
                posScreen = movMarbleInfo[1]
                self.blitImg(posScreen, IMG_MARBLE)

        # Rafraîchissement de tous les simpleSprite en cours d'affichage.
        for simpleSprite in self.listSimpleSprite:
            self.blitImg(simpleSprite.posScreen, simpleSprite.getCurrentImg())
