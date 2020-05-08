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

![image-uct-formula](https://user-images.githubusercontent.com/60757246/81433802-6f1b3580-9165-11ea-8235-d8a1fbfce5a8.png)

- X représente la division du nombre de victoire sur le nombre d'exploration du noeud
- Cp étant un coefficient d'exploration
- N le nombre d'exploration
- Nj le nombre d'exploration du noeud

On descend ainsi jusqu'à un noeud qui n'a aucun fils

#### L'expansion

Si un noeud ne posséde aucun fils et qu'il a été déjà exploré, on va alors 'l'expand' donc lui rajouter autant de fils qu'il y a de possibilité de jeu.

Par exemple,

![TicTacToe](https://user-images.githubusercontent.com/60757246/81435139-a12d9700-9167-11ea-844f-e33533caf105.png)

Dans ce cas-ci, les croix ont encore 5 possibilités de jeux donc ce noeud aura 5 fils.

#### La Simulation

Si dans la descente, il trouve un noeud ne possédant aucun fils **et n'a pas été encore exploré.**
Il va à partir de la valeur du noeud donc d'un **move** dans l'exemple d'un jeu, effectué des simulations avec des déplacements aléatoires
jusqu'a ce que il arrive à un état de victoire pour un des deux camps.
Exemple du TicTacToe, jusqu'a ce que il y ai une ligne de 3 croix ou  3 cercles indiquant une victoire ou alors s'arrête lors d'une égalité.

#### Backpropagation

À la suite de la simulation, on se retouve avec un résultat vainqueur, perdant ou égalité. Le programme va alors faire remonter cette info jusque au noeud de départ et lui ajouter le résultat dans ses paramètres ainsi que lui rajouter +1 dans son paramètre d'exploration
```python
self.__exploration+=1
self.__win+=resultat
```

