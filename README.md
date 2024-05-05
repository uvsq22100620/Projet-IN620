##### Projet IN620 - LE CORRE Camille et LEFEVRE Laura - LDD BI


Le fichier ProjetIN620.py contient les différentes fonctions que nous avons codées afin de répondre aux différentes questions de l'énoncé. Il est découpé en trois parties : la simulation de l'exécution d'une machine RAM, la simulation d'un automate à pile avec une machine RAM, et l'optimisation de la machine RAM.

Chaque partie est elle-même divisée en plusieurs sous-parties, afin de retrouver facilement quelle fonction permet de répondre à quelle question.
A la fin de chaque question, vous retrouverez le code qui doit être exécuté pour répondre à cette question. Par défaut, si vous exécutez le code tel quel, toutes les fonctions s'exécutent. Cela est permis par l'appel de la fonction execute_projet(). Vous pouvez aussi exécuter les fonctions une par une, grâce aux lignes de code mises en commentaire à la fin de chaque question.
Vous pouvez évidemment modifier les paramètres des fonctions, comme en testant différents codes de machine RAM, présents dans les fichiers testX.txt.

### PARTIE 1 : Simulation de l'exécution d'une machine RAM

Dire comment on représente une machine RAM

Nous avons représenté une configuration d'une machine RAM comme... Quand les instructions du code RAM sont exécutées sur l'entrée donnée, les différentes configurations sont stockées dans une liste, affichée sur le terminal.

Nous avons aussi fait un affichage sur le terminal pour visualiser l'état des registres après chaque instruction.

Le code RAM de la machine calculant a^b est dans le fichier ApuissanceB.txt.
Celui pour trier un tableau à l'aide du tri à bulle est dans le fichier triAbulle.txt.

### PARTIE 2 : Simulation d'un automate à pile par une machine RAM

Nous avons décidé d'ajouter l'instruction JNE(x, y, z) (JUMP NOT EQUAL) aux types d'instructions possibles. Cette instruction permet de sauter de z lignes si x est différent de y et elle est gérée par la fonction analyse_instructions() de la partie 1.

### PARTIE 3 : Optimisation d'une machine RAM

La première étape constite en la représentation du code d'une machine RAM sous forme de graphe, où les instructions sont représentées par des sommets et il y a une arête d'un sommet u vers un sommet v si et seulement si on peut passer de l'instruction u à l'instruction v en un seul pas de calcul.
Notre graphe est stocké dans un dictionnaire où chaque clé est un sommet et la valeur associée est une liste de ses successeurs. Par exemple : {sommet1 : [successeur1, successeur2], sommet2 : [successeur3]}
Il a fallu également ajouter un sommet D (début) possédant un seul successeur (la première instruction) et aucun prédécesseur. 
