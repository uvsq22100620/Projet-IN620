##### Projet IN620 - LE CORRE Camille et LEFEVRE Laura - LDD BI


Le fichier ProjetIN620.py contient les différentes fonctions que nous avons codées afin de répondre aux différentes questions de l'énoncé. Il est découpé en trois parties : la simulation de l'exécution d'une machine RAM, la simulation d'un automate à pile avec une machine RAM, et l'optimisation de la machine RAM.

Chaque partie est elle-même divisée en plusieurs sous-parties, afin de retrouver facilement quelle fonction permet de répondre à quelle question.
A la fin de chaque question, vous retrouverez le code qui doit être exécuté pour répondre à cette question. Par défaut, si vous exécutez le code tel quel, toutes les fonctions s'exécutent. Cela est permis par l'appel de la fonction execute_projet(). Vous pouvez aussi exécuter les fonctions une par une, grâce aux lignes de code mises en commentaire à la fin de chaque question.
Vous pouvez évidemment modifier les paramètres des fonctions, comme en testant différents codes de machine RAM, présents dans les fichiers testX.txt.

### PARTIE 1 : Simulation de l'exécution d'une machine RAM

Nous représentons le code d'une machine RAM comme une liste de ses instructions. Une configuration est donnée par un dictionnaire comprenant l'état des registres i, r et o, ainsi que la liste des instructions. Quand les instructions du code RAM sont exécutées sur l'entrée donnée, les différentes configurations (dictionnaires) sont stockées dans une liste.

Nous avons aussi fait un affichage sur le terminal pour visualiser l'état des registres après chaque instruction.

Le code RAM de la machine calculant a^b est dans le fichier ApuissanceB.txt.
Celui pour trier un tableau à l'aide du tri à bulle est dans le fichier triAbulle.txt.

### PARTIE 2 : Simulation d'un automate à pile par une machine RAM

Pour faire la simulation d'un automate à pile par une machine RAM, il faut générer dans un fichier txt, le code de la machine RAM permettant cette simulation. On a besoin de plusieurs variables et compteurs qui sont stockés dans les registres r en plus de la pile. 

L'idée pour faire cette simulation est la suivante : 
- on fait l'initialisation des registres r
-  on regarde s'il y a une transition pour chaque lettre du mot en regardant si l'état de départ, la lettre et le sommet de pile sont identiques entre la transition à tester et les paramètres dans lesquels on se trouve
- Arrivée à la fin, si on est dans un état final, alors le mot est reconnu, sinon on va regarder s'il n'y a pas une epsilon transition qui nous amène dans un état final. Si c'est le cas, le mot est reconnu, sinon il ne l'est pas.

Pour cette partie, nous avons décidé d'ajouter l'instruction JNE(x, y, z) (JUMP NOT EQUAL) aux types d'instructions possibles. Cette instruction permet de sauter de z lignes si x est différent de y et elle est gérée par la fonction analyse_instructions() de la partie 1.

### PARTIE 3 : Optimisation d'une machine RAM

La première étape constite en la représentation du code d'une machine RAM sous forme de graphe, où les instructions sont représentées par des sommets et il y a une arête d'un sommet u vers un sommet v si et seulement si on peut passer de l'instruction u à l'instruction v en un seul pas de calcul.
Notre graphe est stocké dans un dictionnaire où chaque clé est un sommet et la valeur associée est une liste de ses successeurs. Par exemple : {sommet1 : [successeur1, successeur2], sommet2 : [successeur3]}
Il a fallu également ajouter un sommet D (début) possédant un seul successeur (la première instruction) et aucun prédécesseur. 
Cela nous permet d'optimiser la machine RAM de deux façons différentes :
- élimination du code mort (instructions qui ne seront jamais exécutées)
- regrouper plusieurs instructions en une seule (quand cela est possible)
Cela permet donc de diminuer le nombre d'instructions.