# Avalam_IA

Projet réalisé par Matthias Reveillard (18122) et Mateo Yerles (18714) dans le cadre du cours 'Projet Informatique' à L'ECAM Brussels Engineering School.

# Présentation du Projet

Dans le cadre du projet, il nous a été demandé de programmer une intelligence artificielle avec un algorithme au choix sur base d'un jeu de société appelé "Avalam".

Pour la petite histoire, Avalam fut crée par Philipe Deweys en 1995.
Son créateur est d'ailleurs Waterlootois et de nombreux prix ont été attribués à son jeu autour du globe. Ce qui en fait le jeu belge le plus primé à ce jour.
L'objectif étant de s'affronter entre élèves sur le serveur créé par le professeur Mr Lurkin.

# Le Programme
Afin de démarrer le serveur principal qui recueillera les matchs, vous aurez besoin des fichiers du serveur sur le profil suivant:
https://github.com/ECAM-Brussels/AIGameRunner

Pour lancer le serveur effectuez cette commande:
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
AlphaZero utilise comme algorithme principal le Monte Carlo Tree Search (MCTS) et en complément un réseau de neurones.
Dans le cadre du projet nous nous sommes arretés au MCTS qui est déjà puissant pour la tâche demandée.

### Mais comment fonctionne-t-il ?
![MCTS](https://user-images.githubusercontent.com/60757246/81428082-07142180-915c-11ea-8349-7aaea1bd9a57.png)

Comme le décrit le graphe au-dessus il possède plusieurs étapes importantes.
C'est un algorithme qui fonctionne sur base d'un Arbre de possibilité, les noeuds de cette arbre stock les informations comme le coup lié à ce noeud mais aussi le nombre d'exploration et de victoire lié (j'explique en bas ce que ça signifie).

#### La Selection

Le programme descend de la racine à ses fils, et de ses fils à ses "petit-fils", dans un sens bien précis.
En effet, le prochain fils à être visité est choisi parmi les autres suivant une équation, le noeud possédant la valeur la plus élevée est sélectionné.

![image-uct-formula](https://user-images.githubusercontent.com/60757246/81433802-6f1b3580-9165-11ea-8235-d8a1fbfce5a8.png)

- X représente la division du nombre de victoire sur le nombre d'exploration du noeud
- Cp étant un coefficient d'exploration
- N le nombre d'exploration
- Nj le nombre d'exploration du noeud

On descend ainsi jusqu'à un noeud qui n'a aucun fils

#### L'expansion

Si un noeud ne possède aucun fils et qu'il a déjà été exploré, on va alors 'l'expand' donc lui rajouter autant de fils qu'il y a de possibilités de jeu.

Par exemple,

![TicTacToe](https://user-images.githubusercontent.com/60757246/81435139-a12d9700-9167-11ea-844f-e33533caf105.png)

Dans ce cas-ci, les croix ont encore 5 possibilités de jeux donc ce noeud aura 5 fils.

#### La Simulation

Si dans la descente, il trouve un noeud ne possédant aucun fils **et n'a pas été encore exploré.**
Il va, à partir de la valeur du noeud donc d'un **move** dans l'exemple d'un jeu, effectuer des simulations avec des déplacements aléatoires
jusqu'a ce que il arrive à un état de victoire pour un des deux camps.
Exemple du TicTacToe, jusqu'à ce que il y ait une ligne de 3 croix ou 3 cercles indiquant une victoire ou alors s'arrête lors d'une égalité.

#### Backpropagation

À la suite de la simulation, on se retouve avec un résultat vainqueur, perdant ou égalité. Le programme va alors faire remonter cette info jusqu'au noeud de départ et lui ajouter le résultat dans ses paramètres ainsi que lui rajouter +1 dans son paramètre d'exploration et ce, aussi pour le noeud racine.
```python
self.__exploration+=1
self.__win+=resultat
```
### C'est bien mais on fait quoi après ?

En fonction du nombre de simulations voulues ou bien dans notre cas d'une contrainte de temps, l'algorithme va renvoyer le meilleur fils de la racine en fonction de l'équation mentionnée plus haut.

Ce fils est censé représenter le meilleur coup possible, en effet le MCTS se base sur des statistiques.
Donc, plus il y aura de simulations plus l'algorithme représentera une réalité dépassant la notion de 'random'.

# Bibliothèque utiliser
- copy
- random
- math
- sys
- cherrypy
- json
- socket
- webbroser

### liens intéressants pour la compréhension

- https://www.youtube.com/watch?v=UXW2yZndl7U
- https://www.youtube.com/watch?v=Fbs4lnGLS8M&t=638s
- https://web.stanford.edu/~surag/posts/alphazero.html

### Si tu veux continuer sur mes pas, jeune padawan :godmode:

Le plus intéressant serait de lui rajouter un soutien avec un réseau de neurones, pour l'algorithme en tant que tel une optimisation serait la bienvenue.

Et bien sûr, même si l'algorithme est puissant, il a une nette faiblesse en début de partie due aux nombres conséquents de coups possibles.
Donc lui obliger en début de partie à répondre sur base d'une tactique choisie à l'avance serait bien vu:

- Cacher les pions adverses avec ses propres pions
- Neutraliser les tours possédants plus de 4 pions
- Essayer de jouer les pions au milieu du board, pour raccourcir rapidement le nombre de possibilitsé de jeu et ainsi recourir plus vite au MCTS

Le moment le plus efficace pour switcher sur du MCTS serait un nombre de 40 possibilités.
