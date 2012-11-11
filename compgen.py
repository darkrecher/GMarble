# -*- coding: utf-8 -*-
"""
GMarble

Mon blog : http://recher.wordpress.com/
Mon twitter : http://twitter.com/_Recher_
Repository : https://github.com/darkrecher/GMarble

Ce superbe jeu, son code source, ses euh... images, et son contenu sonore actuellement inexistant
sont disponibles, au choix, sous la licence Art Libre ou la licence CC-BY-SA.
"""

# Type des "Component". Un component = un type d'objet à poser sur une tile du jeu.
(COMP_NOTHING,    # Le component avec rien dedans
 COMP_SIMPLE_PIPE # Tuyau simple, avec 2 extrémités. (qui tourne, ou pas)
) = range(2)


"""
Ordre dans lequel les actions sont censées se passer, durant un cycle de jeu :

 - Pour chaque marble, on détermine sa position future, en fonction de sa position actuelle
   et de sa direction de déplacement.
   
 - On en déduit les components sur lesquels arriveront chaque marbles
 
 - Pour chacun de ces components, on exécute la fonction handleIncomingMarble, 
   qui va faire 2 trucs principaux :
    * Envoi d'une commande vers un autre component (par ex : une commande de switch, de reset ...)
      Dans ce cas, on exécutera la fonction sendCommand, 
      le code extérieur devra se souvenir cette commande. On la prend pas en compte immédiatement.
      (La commande précise le component de destination, et le type de la commande)
    * Renvoi d'un booléen, indiquant si le component accepte l'arrivée de cette bille.
      On déduit le côté d'où arrive la bille par sa direction de déplacement.
      Par exemple, pour un component de type "tuyau horizontal", il ne doit pas accepter
      les billes qui arrive par le haut (direction de mouvement = DOWN) ni les billes qui arrivent
      par le bas (direction de mouvement = UP).
      Lorsque cela survient, le code extérieur devra faire exploser la bille, 
      contre le bord de la tile de ce component "tuyau horizontal".

  - On déterminera d'autres collisions :
    * 2 marbles qui se rentrent dedans entre 2 tiles.
    * 2 marbles ou plus qui se rentrent dedans au milieu d'une tile.
      
  - Pour chaque commande enregistrée, on l'applique sur le component de destination.
    Par exemple : on change la direction d'un switch, on libère la balle d'un component stoqueur.
    On exécutera alors la fonction receiveCommand du component de destination.
  
  - On retire du jeu les marbles qui ont explosée
  
  - Pour chaque marble en mouvement, on effectue le mouvement 
    (modification des coordonnées de la marble, en exécutant doMovement)
    
  - Pour chaque marble, on détermine le component sur lequel elle se trouve actuellement,
    et on exécute la fonction Component.handlePresentMarble. Cette fonction va 
    modifier la direction actuelle du mouvement de la bille. 
    (par exemple, si elle tourne dans un tuyau qui tourne).
    Le component peut également faire exploser la bille. (pas encore géré)
    
  - Détermination des trucs à afficher selon tout ce qu'il s'est passé.
    Exécution de plusieurs cycles d'animation, pour montrer tout cela au joueur.
    
Avec une gestion de ce type, on s'en sort pas trop mal. Par exemple, si 1 bille arrive sur 
la commande d'un switch pendant qu'une autre bille arrive en même temps sur le switch, 
le changement d'état du switch est immédiatement pris en compte, pour la bille qui arrive dessus. 
Et c'est plutôt cool, et assez naturel comme fonctionnement. N'est-ce pas ?
"""
class ComponentGeneric():
    """
    Définit le comportement d'un component, dans l'arène.
    Type MVC : Modèle
    """

    def __init__(self, pos, compType=COMP_NOTHING):
        """ Constructeur
        Entées : pos : position dans l'arène. TRODO : à priori, ça ne servira à rien.
        compType : type du composant. Valeur COMP_*
        """
        self.compType = compType
        self.pos = pos  # useless ?
        self.commandToSend = None

    def handleIncomingMarble(self, marble):
        """
        Prise en compte d'une bille qui va arriver sur le component, 
        lors du prochain cycle de jeu.
        Entrées : marble : objet de type Marble. La bille en question, qui arrive 
                  par un certain côté. On décide, de manière un peu bancale mais pas trop, que
                  le côté d'arrivée de la bille est le côté opposé de sa direction de mouvement.
        Sorties : True : le component accepte cette bille.
                  False : Le component ne l'accepte pas. Il faudra faire exploser la bille 
                  contre le bord de la tile sur laquelle se trouve ce component.
        """
        return False

    def handlePresentMarble(self, marble):
        """
        Prise en compte des actions à effectuer lorsqu'une bille se trouve sur le component.
        Entrées : marble : objet de type Marble. La bille qui est sur le component.
        Ici, on pourra faire plein de trucs, tel que : modifier la direction de la bille, ou
        même modifier sa couleur, si c'est un component qui peint. Enfin bref, c'est la fête.
        """
        pass

    def sendCommand(self, commandType):
        """
        Envoi d'une commande vers un autre component. En fait, on va juste définir la
        variable self.commandToSend, en mettant toutes les infos nécessaires dedans.
        Et c'est le code extérieur qui aura la charge de consulter cette variable, 
        et d'enregistrer éventuellement la commande qui s'y trouve, lors de l'étape suivante
        de ce même cycle de jeu.
        """
        pass

    def receiveCommand(self, commandType):
        """
        Réception d'une commande, envoyé par un autre component. (On n'est pas obligé de savoir
        lequel c'est. Il suffit de connaître le type de la commande).
        Ici on peut faire plein de trucs pour modifier les variables internes du component. Yipi!
        """
        pass
