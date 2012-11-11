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
from marble   import Marble
from ctrlaren import ArenaController


if __name__ == "__main__":
    # Init, et coucoutage
    print "coucou"
    arenaController = ArenaController()
    arenaController.refreshAndDisplayAll()
    # Ajout d'une marble dans l'arène du jeu.
    # TRODO : C'est un peu fait à l'arrache, et ça n'a pas grand chose à faire ici.
    # C'est provisoire. On fera plus formel plus tard. 
    newMarble = Marble(pyRect(2, 1), RIGHT)
    arenaController.arena.addMarble(newMarble)
    # Affichage total de l'Arena dans son état initial. Avec la marble dedans.
    arenaController.refreshAndDisplayAll()
    print "starts the game"
    # Exécution et animation de 4 cycles de jeu. Dans le dernier cycle, il ne se passe rien,
    # car l'unique marble a explosé au cycle précédent. Mais je le fait, pour bien montrer
    # que ça marche dans ce cas là aussi.
    for _ in xrange(4):
        arenaController.ProcessAndAnimOneGameCycle()
    # Affichage total de l'Arena dans son état final. 
    # Avec pas de marble dedans, vu qu'on l'a explosée.
    print "final state"
    arenaController.refreshAndDisplayAll()

