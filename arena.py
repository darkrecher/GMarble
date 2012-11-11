# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

from common   import pyRect, UP, RIGHT, DOWN, LEFT
from compnoth import ComponentNothing
from comppipe import ComponentSimplePipe
from marblexp import MarbleExplosion, EXPLOS_MARBLE_ON_BORDER


class Arena():
    """
    Gestion de l'aire de jeu. L'arène est composée d'un tableau à 2 dimension de Components,
    ainsi que de zero, une ou plusieurs marbles. L'arène s'occupe des trucs suivants : 
     - Déplacement des marbles d'une case à l'autre. 
     - Exécution des contrôles pour chaque déplacement (détection des collisions)
     - Exécution des fonctions handleMarble des Components, pour déterminer les déplacements.
     - Envoi des commandes d'un component à un autre.
     - Et surement plein d'autres trucs cools.
    Type MVC : Modèle
    """
    def __init__(self, size):
        """ Constructeur
        Entrée : size : tuple de 2 int. Largeur et hauteur de l'arène, en nombre de Component.
        """
        # init des différentes variables contenant la taille de l'arène.
        # TRODO : virer les variables qui servent à rin.
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.rectSize = pyRect(0, 0, self.width, self.height)
        # Init diverses
        self.listMarble = []
        self.listMarbleToRemove = []
        self.listMarbleExplosion = []

        # Init du tableau à 2 dimensions contenant les Components. 
        # C'est une liste de "height" éléments.
        # Chacun de ces éléments est une sous-liste, contenant "width" Component.
        self.matrixComponent = []        
        # Pour l'init, on crée les listes et sous-listes avec que des ComponentNothing.
        for _ in xrange(self.height):
            lineComponent = [ ComponentNothing(pyRect(0, 0))
                              for _ in xrange(self.width) ]
            self.matrixComponent.append(lineComponent)

        # Provisoire. Placement des Component pas Nothing, à la main.
        self.matrixComponent[1][2] = ComponentSimplePipe("osef", UP, RIGHT)
        self.matrixComponent[1][3] = ComponentSimplePipe("osef", UP, LEFT)
        self.matrixComponent[0][3] = ComponentSimplePipe("osef", RIGHT, DOWN)


    # Fonctions Get-Set à la con. (Je fais partie de la Jet-Set !)
    def getComponent(self, pos):
        return self.matrixComponent[pos.y][pos.x]

    def getComponentXY(self, posX, posY): # TRODO : useless ?
        return self.matrixComponent[posY][posX]

    def setComponent(self, pos, component): # TRODO : useless ?
        self.matrixComponent[pos.y][pos.x] = component

    def addMarble(self, marble):
        """ ajoute une marble dans l'arène.
        Entrées : marble : Objet de type Marble.
                           Il est de bon ton d'avoir préalablement initialisé les coordonnées
                           et la direction initiale de cet objet marble.
                           (L'arène pourrait déterminer la direction initiale à partir de 
                           la position. Mais pas toujours. Donc on le fixe avant).
        """
        self.listMarble.append(marble)


    def handleNextMarbleMove(self):
        """
        Détermine le prochain mouvement, et donc les positions futures, de toutes les marbles
        présentes dans l'arène.
        Au passage, on détermine les collisions, et les explosions de Marble qui en résultent.
        TRODO : il faudra aussi déterminer les commandes qui s'envoient entre Components.
        """
        for marble in self.listMarble:
        
            # Exécution des actions que doivent effectuer les Components sur lesquels se
            # trouve actuellement une marble. Au passage, détermination de la nouvelle direction
            # de mouvement de chaque marble. Déduction de la future position, dans l'arène,
            # de chaque marble.
            compOfMarble = self.getComponent(marble.pos)
            compOfMarble.handlePresentMarble(marble)
            marble.determinePosFuture()

            # TRODO : verif que la position future de la marble est dans l'arène. 
            # (coordonnées comprise dans la size de l'arène. Sinon faut exploser la marble.

            # Exécution des actions que doivent effectuer les Components qui vont accueillir
            # une marble au prochain cycle de jeu.
            compOfMarbleFuture = self.getComponent(marble.posFuture)
            if not compOfMarbleFuture.handleIncomingMarble(marble):
                # Le Component ne peut pas accueillir la marble qui va lui arriver dessus
                # (pour une raison ou pour une autre, c'est son problème).
                # Il faut faire exploser la marble contre le bord du Component non-accueillant.
                self.listMarbleToRemove.append(marble)
                # L'arène va comporter une explosion, de type "explosion contre un bord",
                # et concernant une seule marble. 
                explos = MarbleExplosion((marble, ), EXPLOS_MARBLE_ON_BORDER)
                self.listMarbleExplosion.append(explos)

        # TRODO : gestion des collisions (2 marbles qui se rentrent dedans entre 2 tile)

        # TRODO 2 : gestion des collisions (2 marbles qui se rentrent dedans au milieu d'une tile)


    def doMarbleMove(self):
        """
        Réalisation effective du mouvement de toutes les marbles de l'arène.
        Chaque marble ne se déplace que d'une seule case. (Même si en théorie, on pourrait faire
        ce qu'on veut, car on peut mettre n'importe quelles coordonnées dans la position future.)
        """
        # Supression des marble à suppressionner. Soit elle a explosée, TRODO : soit elle est
        # sortie de l'arène.
        for marbleToRemove in self.listMarbleToRemove:
            self.listMarble.remove(marbleToRemove)

        # Réinitialisation des listes de marble à virer, et des explosions.
        # Les explosions, quelles qu'elles soye, ne durent toujours qu'un seul cycle de jeu.
        # TRODO : ou pas. Mais pour l'instant, si.
        self.listMarbleToRemove = []
        self.listMarbleExplosion = []

        # Réalisation des mouvements pour les marbles qui restent.
        for marble in self.listMarble:
            marble.doMovement()
