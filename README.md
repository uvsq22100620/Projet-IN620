##### Projet IN620 - LE CORRE Camille et LEFEVRE Laura - LDD BI


Le fichier ProjetIN620.py contient les différentes fonctions que nous avons codées afin de répondre aux différentes questions de l'énoncé. Il est découpé en trois parties : la simulation de l'exécution d'une machine RAM, la simulation d'un automate à pile avec une machine RAM, et l'optimisation de la machine RAM.

Chaque partie est elle-même divisée en plusieurs sous-parties, afin de retrouver facilement quelle fonction permet de répondre à quelle question.
A la fin de chaque question, vous retrouverez le code qui doit être exécuté pour répondre à cette question. Par défaut, si vous exécutez le code tel quel, toutes les fonctions s'exécutent. Cela est permis par l'appel de la fonction execute_projet(). Vous pouvez aussi exécuter les fonctions une par une, grâce aux lignes de code mises en commentaire à la fin de chaque question.
Vous pouvez évidemment modifier les paramètres des fonctions, comme en testant différents codes de machine RAM, présents dans les fichiers testX.txt.

### PARTIE 1 : Simulation de l'exécution d'une machine RAM

Dire comment on représente une machine RAM

Nous avons représenté une configuration d'une machine RAM comme... Quand les instructions du code RAM sont exécutées sur l'entrée donnée, les différentes configurations sont stockées dans une liste, affichée sur le terminal.

Nous avons aussi fait un affichage sur le terminal pour visualiser l'état des registres après chaque instruction.

Expliquer les codes RAM de la question 5 et pour a puissance b : proposer amélirorations
Pour la partie 2, nous avons décidé d'ajouter l'instruction JNE...
