# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from arena   import Arena
from diarena import ArenaDisplayer, NB_ANIM_CYCLE_PER_GAME_CYCLE

class ArenaController():
    """
    classe qui gère tout le bazar pour une Arena : 
    Déroulement des cycles d'animation et de jeu, affichage de l'Arena entière, des anims, ...
    L'affichage est effectué sur la sortie standard, paf, direct.
    Type MVC : Contrôleur
    """
    
    def __init__(self):
        """ Constructeur """
        # Arena de largeur 5 et de hauteur 2. L'initialisation du contenu de l'Arena
        # (ses Components) est directement effectuée dans l'init de la classe Arena.
        # TRODO : d'ailleurs c'est mal. Mais provisoire.
        self.arena = Arena((5, 2))
        self.arenaDisplayer = ArenaDisplayer(self.arena)
        
        
    def printSeparator(self):
        """ écrit une superbe ligne de séparation sur la sortie standard """
        print "#" * 79
        
        
    def refreshAndDisplayAll(self):
        """
        Rafraîchit en entier l'image de l'arenaDisplayer, représentant toute l'Arena.
        Et balance cette image sur la sortie standard, suivi d'une superbe ligne de séparation.
        """
        self.arenaDisplayer.refreshAllScreen()
        for line in self.arenaDisplayer.screen:
            print line
        self.printSeparator()

    
    def ProcessAndAnimOneGameCycle(self):
        """
        Exécute, anime, et affiche un cycle de jeu, sur la sortie standard.
        On peut recommencer un autre cycle de jeu immédiatement après celui-là.
        """
        # Préparation du cycle de jeu en cours
        self.arena.handleNextMarbleMove()
        self.arenaDisplayer.initAnimation()
    
        # Exécution des cycles d'animation de ce cycle de jeu en cours.
        for animCounter in xrange(NB_ANIM_CYCLE_PER_GAME_CYCLE):
            if self.arenaDisplayer.advanceAnimationCounter():
                # Le cycle d'animation qu'on vient d'exécuter a provoqué un changement dans
                # la grande image représentant l'arène.
                # On indique quelle est le numéro du cycle d'anim en cours. Pour pouvoir se
                # repérer un minimum dans le temps. (Parce qu'en vrai, on peut pas trop
                # gérer le temps, puisqu'on balance tout derec sur la sortie standard).
                print "animCounter :", animCounter
                # Rafraîchissement des zones de l'image de l'Arena qui sont susceptibles 
                # de changer. Et affichage, sur la sortie standard, de toute l'image
                self.arenaDisplayer.refreshAnimation()
                for line in self.arenaDisplayer.screen:
                    print line
                self.printSeparator()
            # Si le cycle d'anim qu'on vient d'exécuter n'a pas provoqué de changement dans
            # l'image, on ne la réaffiche pas sur la sortie standard. Ca servirait à rien.
    
        print "animation ended"
        # Terminaison du cycle de jeu en cours. Modification des coordonnées des marbles
        # dans l'Arena, selon le mouvement qu'on avait prévus lors de la préparation de ce
        # cycle de jeu.
        self.arena.doMarbleMove()
        self.printSeparator()
        