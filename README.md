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
#### Mais comment fonctionne-t-il ?



