# Avalam_IA

Projet réalisé par Matthias Reveillard (18122) et Mateo Yerles (18714) dans le cadre du cours 'Projet Informatique' à L'ECAM Brussels Engineering School.

# Présentation du Projet

Dans le cadre du projet, il nous a été demandé de programmer une intelligence artificiel avec un algorithme au choix sur base d'un jeu de société appellé "Avalam".
Pour la petite histoire, Avalam fut crée par PHilipe Deweys en 1995.
Son créateur est d'ailleurs Waterlootois et son jeu a été primé par de nombreux prix autour du globe ce qui en fait le jeu belge le plus primé à ce jour.
L'objectif étant s'affronter entre éleve sur le serveur créé par le professeur Mr Lurkin.

# Le Programme
Afin de démarré le serveur principal qui recueillera les matches, vous aurez besoin des fichiers du serveur sur le profil suivant:
https://github.com/ECAM-Brussels/AIGameRunner
Pour lancer le serveur effectué cette commande:
```Python
python Server.py Avalam
```
Ensuite pour l'IA il vous suffira d'effectuer cette commande:
```Python
python IA.py PORT
```
Port, représente le port d'écoute sur votre ordinateur.

# Algorithme
Devant l'immense possibilité des algorithmes disponnibles, nous avons décidé de copier les plus grands.
C'est à dire "Alpha(Go)Zero"

## Mont Carlo Tree Search
AlphaZero utilise comme algo principale le Mont Carlo Tree Search (MCTS) et en complément un reseau de neuronnes.
Dans le cadre du projet nous nous sommes arreté au MCTS qui est déja puissant pour la tâche demandée.
### Mais comment fonctionne-t-il ?
![MCTS](https://user-images.githubusercontent.com/60757246/81428082-07142180-915c-11ea-8349-7aaea1bd9a57.png)

Comme le décrit le graphe au-dessus il possède plusieurs étapes importantes.
C'est un algorithme qui fonctionne sur base d'un Arbre de possibilité, les noeuds de cette arbre stock les informations comme le coup lié à ce noeud mais aussi le nombre d'exploration et de victoire lié (j'explique en bas ce que ça signifie).

#### La Selection

Le programme descend de la racine à ses fils, et de ses fils à ses "petit-fils", dans un sens bien précis.
En effet, le prochain fils à être visité est choisie parmis les autres suivants une équation, le noeud possédant la valeur la plus élevé est sélectionné.


