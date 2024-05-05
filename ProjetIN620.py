############ IN620-Projet ##############
### LEFEVRE Laura - LE CORRE Camille ###
########################################

#### IMPORTATION DES MODULES ###########
import re

#### VARIABLES GLOBALES ################
## Regex
#regex_instruction = re.compile(r'(ADD|SUB|DIV|MULT)\((\d+|r\d+|i\d+|o\d+),\s*(\d+|r\d+|i\d+|o\d+),\s*(\d+|r\d+|o\d+)\)')
#regex_instruction = re.compile(r'(ADD|SUB|DIV|MULT)\((\d+|r\d+|i\d+|o\d+|i@r\d+|i@i\d+|r@i\d+|r@r\d+|O@i\d+|O@r\d+),\s*(\d+|r\d+|i\d+|o\d+|i@r\d+|i@i\d+|r@i\d+|r@r\d+|O@i\d+|O@r\d+),\s*(r\d+|O\d+|r@i\d+|r@r\d+|O@i\d+|O@r\d+))')
regex_registre = re.compile(r'([iro])(\d+)')                                                        #regex détail d'un registre en argument
regex_chiffre = re.compile(r'-?\d+')    
regex_indirection = re.compile(r'([iro])@([ir])(\d+)')
regex_instruction = re.compile(r'(ADD|SUB|DIV|MULT)\((\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|o\d+|[ro]@[ir]\d+)\)')
regex_jump = re.compile(r'(JUMP)\((-?\d+)\)')
regex_jumps_spe = re.compile(r'(JE|JL|JNE)\((\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(-?\d+)\)')

## Dico
dico_type_registre = {'i': "registres_i", 'r':"registres_r", 'o':"registres_o"}
dico_elt_RAM = {}       #dico de stockage des différents éléments de la machine RAM à générer



##### PARTIE 1 : Simulation de l'exécution d'une machine RAM

### Question 1:
### Proposer une structure de données qui permet de représenter le programme d’une RAM.
### Ecrire une fonction qui lit un fichier texte contenant le code d’une machine RAM et un mot d’entrée et qui
### initialise la structure de données pour représenter cette machine.

def read_RAM(fic_in):
    '''Fonction permettant la lecture du fichier dans laquelle le code d'une Machine RAM est stockée 
    et retourne l'ensemble du code dans une liste dont chaque elt correspond à une ligne du code'''

    with open(fic_in, 'r') as fic_in:
        codeRAM = []
        for ligne in fic_in:
            codeRAM.append(ligne[:-1])

    return codeRAM  #Renvoie une liste avec l'entrée et les instructions de la machine RAM

def info_code_RAM(codeRAM):
    '''Fonction permettant de récupérer l'entrée de la machine RAM et de créer les différentes listes réprésentant 
    les 3 types de registres (i, r, o)'''
    global dico_elt_RAM

    registres_i = []    #registre input

    entree = codeRAM[0].split(', ')      #la première ligne du code correspond à l'entrée (chaque elt de l'entrée est séparé par une virgule)
    taille = int(entree[0])             #taille de l'entrée
    
    #ajoute dans notre registre input l'entrée obtenue
    for i in range(taille+1) :   
        registres_i.append(entree[i])
    
    #Création des listes correspondant aux registre de type r et o avec une taille correspondant à 2 fois celle de l'entrée (taille arbitraire)
    registres_r = ['#' for i in range(0, taille*2)]
    registres_o = ['#' for i in range(0, taille*2)]

    #ajout des éléments de la machine RAM dans le dico global
    dico_elt_RAM["codeRAM"] = codeRAM[1:]           #liste avec les instructions
    dico_elt_RAM["registres_i"] = registres_i
    dico_elt_RAM["registres_r"] = registres_r
    dico_elt_RAM["registres_o"] = registres_o

    return dico_elt_RAM

# Affichage des résultats de la question 1 :
#print(info_code_RAM(read_RAM('test2.txt')))


### Question 2:
### Proposer une structure de données pour représenter une configuration d’une Machine RAM.
### Donner une fonction qui prend en argument une machine RAM et une configuration et qui donne la
### configuration obtenue après un pas de calcul de la machine.


def desc_registre(registre):
    '''Fonction qui prend en entrée un registre avec le format i|r|o suivit d'un chiffre (par exemple r0)
    et renvoie le type du registre et l'indice du registre'''

    match_registre = re.search(regex_registre, registre)
    #print(match_registre, registre)
    if match_registre :
        type = match_registre.group(1)
        indice = int(match_registre.group(2))
    return (type, indice)

def instruction_ADD(arg1, arg2, arg3):
    '''Fonction permettant l'analyse et le calcul d'une instruction ADD'''

    global dico_elt_RAM

    #Si les éléments à additionner ne sont pas des entiers on va aller chercher les valeurs stockées dans les registre correspondant
    if not re.match(regex_chiffre, arg1):
        desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")

        arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])

    if not re.match(regex_chiffre, arg2):
        desc_arg2 = desc_registre(arg2)

        if desc_arg2[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            
        arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

    #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
    desc_arg3 = desc_registre(arg3)

    if desc_arg3[0] == 'i':
        raise Exception("L'instruction est erronée. Vous ne pouvez pas écrire dans les registres de type Input")

    #Realisation de l'instruction ADD en mettant à jour les registres du dico global
    dico_elt_RAM[dico_type_registre[desc_arg3[0]]][desc_arg3[1]] = int(arg1) + int(arg2)

    return

def instruction_SUB(arg1, arg2, arg3):
    '''Fonction permettant l'analyse et le calcul d'une instruction SUB'''

    global dico_elt_RAM

    #Si les éléments à additionner ne sont pas des entiers on va aller chercher les valeurs stockées dans les registre correspondant
    if not re.match(regex_chiffre, arg1):   
        desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")

        arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
            
    if not re.match(regex_chiffre, arg2):
        desc_arg2 = desc_registre(arg2)

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            
        arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

    #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
    desc_arg3 = desc_registre(arg3)

    if desc_arg3[0] == 'i':
        raise Exception("L'instruction est erronée. Vous ne pouvez pas écrire dans les registres de type Input")

    #Realisation de l'instruction ADD en mettant à jour les registres du dico global
    dico_elt_RAM[dico_type_registre[desc_arg3[0]]][desc_arg3[1]] = int(arg1) - int(arg2)

    return

def instruction_DIV(arg1, arg2, arg3):
    '''Fonction permettant l'analyse et le calcul d'une instruction DIV'''

    global dico_elt_RAM

    #Si les éléments à additionner ne sont pas des entiers on va aller chercher les valeurs stockées dans les registre correspondant
    if not re.match(regex_chiffre, arg1):   
        desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")

        arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
            
    if not re.match(regex_chiffre, arg2):
        desc_arg2 = desc_registre(arg2)

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            
        arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])


    if int(arg2) == 0 :
        raise Exception("Impossible de diviser par 0, l'instruction est erronnée")
            

    #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
    desc_arg3 = desc_registre(arg3)

    if desc_arg3[0] == 'i':
        raise Exception("L'instruction est erronée. Vous ne pouvez pas écrire dans les registres de type Input")
    
    #Realisation de l'instruction ADD en mettant à jour les registres du dico global
    dico_elt_RAM[dico_type_registre[desc_arg3[0]]][desc_arg3[1]] = int(arg1) / int(arg2)

    return

def instruction_MULT(arg1, arg2, arg3):
    '''Fonction permettant l'analyse et le calcul d'une instruction MULT'''

    global dico_elt_RAM

    #Si les éléments à additionner ne sont pas des entiers on va aller chercher les valeurs stockées dans les registre correspondant
    if not re.match(regex_chiffre, arg1):   
        desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")

        arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
            
    if not re.match(regex_chiffre, arg2):
        desc_arg2 = desc_registre(arg2)

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            
        arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

    #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
    desc_arg3 = desc_registre(arg3)

    if desc_arg3[0] == 'i':
        raise Exception("L'instruction est erronée. Vous ne pouvez pas écrire dans les registres de type Input")

    #Realisation de l'instruction ADD en mettant à jour les registres du dico global
    dico_elt_RAM[dico_type_registre[desc_arg3[0]]][desc_arg3[1]] = int(arg1) * int(arg2)

    return  

def gestion_indirection(registre):
    '''Fonction permettant de gérer l'indirection des registres
    ex : i@r1 correspond au registre ik avec k la valeur dans r1'''

    match = re.match(regex_indirection, registre)

    if match :
        registre_type = match.group(1)  # Type de registre (I, R ou O)
        registre_k = match.group(2)  # i ou r
        k = int(match.group(3))  # Chiffre après le r

    else :
        raise Exception("Erreur d'indirection")

    indice = str(dico_elt_RAM[dico_type_registre[registre_k]][k])

    return registre_type + indice


def analyse_instructions(i_instruc):
    '''Fonction permettant l'analyse d'une instruction de la machine RAM à partir d'une configuration. 
    L'indice est renseigné en paramètre et les registres sont récupérés dans le dictionnaire global'''

    global dico_elt_RAM
    print('i : ', i_instruc)
    #récupère la position en cours dans l'execution du code RAM
    instruction = dico_elt_RAM['codeRAM'][i_instruc]
    print(dico_elt_RAM['registres_i'])
    print(dico_elt_RAM['registres_r'])
    print(dico_elt_RAM['registres_o'])
    print('instruction : ', instruction)

    # Analyse des groupes
    match_instruc = re.match(regex_instruction, instruction)
    match_jump = re.match(regex_jump, instruction)
    match_jumps_spe = re.match(regex_jumps_spe, instruction)    

    if match_instruc :
        type_operation = match_instruc.group(1)
        arg1 = match_instruc.group(2)
        arg2 = match_instruc.group(3)
        arg3 = match_instruc.group(4)

    elif match_jump :
        #print(match_jump)
        type_operation = 'JUMP'
        arg1 = int(match_jump.group(2))
        arg2 = '0'
        arg3 = '0'

    elif match_jumps_spe :
        type_operation = match_jumps_spe.group(1)
        arg1 = match_jumps_spe.group(2)
        arg2 = match_jumps_spe.group(3)
        arg3 = match_jumps_spe.group(4)
        
    else :
        print(match_jumps_spe)
        raise Exception("L'instruction n'est pas valide")
    
    # Test pas de #
    if (arg1 == '#') or (arg2 == '#') or (arg3 == '#'):
        raise Exception("Le caractère '#' ne peut pas être accepté")
    
    #traitement des cas avec indirection
    match_arg1 = re.match(regex_indirection, str(arg1))
    match_arg2 = re.match(regex_indirection, str(arg2))
    match_arg3 = re.match(regex_indirection, str(arg3))

    if match_arg1 :
       arg1 = gestion_indirection(arg1)

    if match_arg2 :
       arg2 = gestion_indirection(arg2)

    if match_arg3 :
       arg3 = gestion_indirection(arg3)

    #appel de la fonction correspondant à l'instruction
    if type_operation == 'ADD' :
        nv_i_instr = i_instruc + 1  # à optimiser avec un if
        instruction_ADD(arg1, arg2, arg3)
 
    elif type_operation == 'SUB' :
        nv_i_instr = i_instruc + 1
        instruction_SUB(arg1, arg2, arg3)
           
    elif type_operation == 'DIV' :
        nv_i_instr = i_instruc + 1
        instruction_DIV(arg1, arg2, arg3)

    elif type_operation == 'MULT':
        nv_i_instr = i_instruc + 1
        instruction_MULT(arg1, arg2, arg3)
    
    elif type_operation == 'JUMP':
        nv_i_instr = i_instruc + arg1

    elif type_operation == 'JE':

        if not re.match(regex_chiffre, arg1):
            desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

            if desc_arg1[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
        
        if not re.match(regex_chiffre, arg2):
            desc_arg2 = desc_registre(arg2) #permet de récupérer le type de registre et son indice

            if desc_arg2[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

        if int(arg1) == int(arg2):
            nv_i_instr = int(i_instruc) + int(arg3)
        else:
            nv_i_instr = int(i_instruc) + 1

    ## Nécessaire pour la partie 2
    elif type_operation == 'JNE':
        if not re.match(regex_chiffre, arg1):
            desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

            if desc_arg1[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
        
        if not re.match(regex_chiffre, arg2):
            desc_arg2 = desc_registre(arg2) #permet de récupérer le type de registre et son indice

            if desc_arg2[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])
        
        print('ARGUMENTS', arg1, arg2)
        if int(arg1) != int(arg2):
            nv_i_instr = i_instruc + int(arg3)
        else:
            nv_i_instr = i_instruc + 1

    else:       # JL

        if not re.match(regex_chiffre, arg1):
            desc_arg1 = desc_registre(arg1) #permet de récupérer le type de registre et son indice

            if desc_arg1[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg1 = int(dico_elt_RAM[dico_type_registre[desc_arg1[0]]][desc_arg1[1]])
        
        if not re.match(regex_chiffre, arg2):
            desc_arg2 = desc_registre(arg2) #permet de récupérer le type de registre et son indice

            if desc_arg2[0] == 'o':
                raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

        if int(arg1) > int(arg2):
            nv_i_instr = int(i_instruc) + int(arg3)
        else :
            nv_i_instr = int(i_instruc) + 1      

    return [nv_i_instr, dico_elt_RAM]


# Affichage des résultats de la question 2 :

#print(analyse_instructions(0))
#print(analyse_instructions(1))
#print(analyse_instructions(2))
#print(analyse_instructions(3))

#print(analyse_instructions(0))
#print(analyse_instructions(1))
#print(analyse_instructions(2))
#print(analyse_instructions(3))
#print(analyse_instructions(4))


### Question 3:
### Ecrire une fonction qui prend comme argument un mot et une machine RAM et qui simule
### le calcul de la machine sur le mot jusqu’à atteindre l’état final. 


def analyse_programme(nom_fichier):

    global dico_elt_RAM

    # Initialisation, création du dictionnaire
    info_code_RAM(read_RAM(nom_fichier))

    instructions = dico_elt_RAM["codeRAM"]
    historique_config = []
    i_instr_courant = 0
    fin_fichier = len(dico_elt_RAM["codeRAM"])

    while i_instr_courant < fin_fichier :
        #print(i_instr_courant)
        #print(instructions[i_instr_courant])
        res = analyse_instructions(i_instr_courant)
        #print('reg_o : ', res[1]['registres_o'])
        i_instr_courant = res[0]    # indice de la prochaine ligne à exécuter
        dico_elt_RAM['registres_r'] = res[1]['registres_r'].copy()  # pour régler le problème d'écraser les anciennes listes
        dico_elt_RAM['registres_o'] = res[1]['registres_o'].copy()
        nv_dico = {'codeRAM': dico_elt_RAM['codeRAM'], 'registres_i': dico_elt_RAM['registres_i'], 'registres_r': res[1]['registres_r'].copy(), 'registres_o' : res[1]['registres_o'].copy()}
        historique_config.append(nv_dico)

    return historique_config

# Affichage des résultats de la question 3 :
#print(analyse_programme("test3.txt"))


### Question 4:
#### Modifier la fonction précédente pour que, à chaque pas de simulation, la configuration de la
### machine s’affiche de manière compréhensible (soit graphiquement, soit sur le terminal).


def affichage_resultats_terminal(liste_config):
    for i_config in range(len(liste_config)):
        print('itération '+str(i_config))
        reg_i = liste_config[i_config]['registres_i']
        reg_r = liste_config[i_config]['registres_r']
        reg_o = liste_config[i_config]['registres_o']
        
        for k in range(len(reg_i)):
            print('i'+str(k)+'  ', end='')
        print('     ', end='')
        for k in range(len(reg_r)):
            print('r'+str(k)+'  ', end='')
        print('     ', end='')
        for k in range(len(reg_o)):
            print('o'+str(k)+'  ', end='')

        print()


        for k in range(len(reg_i)):
            print(str(reg_i[k])+(4-len(str(reg_i[k])))*' ', end='')
        print('     ', end='')
        for k in range(len(reg_r)):
            print(str(reg_r[k])+(4-len(str(reg_r[k])))*' ', end='')
        print('     ', end='')
        for k in range(len(reg_o)):
            print(str(reg_o[k])+(4-len(str(reg_o[k])))*' ', end='')
        print()
        print('______________________________________________________________________')

    return 'fin du programme RAM'



# Affichage des résultats de la question 4 :
#print(analyse_programme("question1_ex code recherche max.txt"))
#print(affichage_resultats_terminal(analyse_programme("test2.txt")))
#print(affichage_resultats_fichier(analyse_programme("test2.txt")))


### Question 5:
### Donner le code des machines de RAM suivantes :
### - Avec en entrée deux entiers a et b, calculer a^b => fichier ApuissanceB.txt
#print(analyse_programme("ApuissanceB.txt"))
### - Avec comme entrée un tableau d’entiers, écrire le tableau trié dans la sortie (par un tri à bulle) => fichier triAbull.txt
#print(analyse_programme("triAbulle.txt"))



##### PARTIE 2 : Comment faire rentrer la pile dans la RAM ?

### Question 6 :
### Ecrire une machine RAM qui étant donné un automate à pile A et un mot w en entrée, écrit
### 0 en sortie si w est reconnu par A et 1 sinon.

def registres_entree(mot_w:str, fic_transitions_A:str):
    ''' Créér les registres i de la machine RAM qui prend en entrée un mot w et un automate à pile A'''

    # Ecriture de la taille du mot et du mot
    registres_i = [len(mot_w)]
    for lettre in mot_w:
        registres_i.append(lettre)

    # Récupérer les transitions du fichier
    l_transitions = []
    fic = open(fic_transitions_A, 'r')
    for ligne in fic:
        l_transitions.append(ligne)
    fic.close()

    # Ecriture du nombre de transitions et des transitions
    registres_i.append(len(l_transitions))
    for t in l_transitions:     # pour chaque transition
        t = eval(t)
        registres_i.append(t[0])        # q
        registres_i.append(t[1])        # a
        registres_i.append(t[2])        # A
        registres_i.append(len(str(t[3])))       # taille de w
        for lettre in str(t[3]):
            registres_i.append(int(lettre))      # lettres de w
        registres_i.append(t[4])        # q'

    return registres_i

def initialisation_registre_AP(nameFile):
    '''Fonction permettant la génération des lignes de code RAM l'initialisation des registres pour la simulation d'un automate 
    à pile avec une machine RAM'''

    with open(nameFile, 'a') as fc :
        fc.write('ADD(0, 0, r0)\n')     #r0 est l'état (donc initialise à 0 car état initial)
        fc.write('ADD(8, 0, r1)\n')     #r1 correspond à l'indice du sommet de pile
        fc.write('ADD(2, 0, r2)\n')     #r2 correspond à la tête de lecture du mot (stocké en i2 donc faut faire i@r2 pour avoir la première lettre du mot -> fin du mot en i@i1 -> pas i0 car en i0 on a la taille de l'entrée)
        fc.write('ADD(i1, 3, r3)\n')    #Correspond à l'indice du premier elt de la premiere transition
        fc.write('ADD(0, 0, r4)\n')     #Taille de mot (mot à écrire dans une transition) à 0 pour le moment (va servir de compteur pour écrire le mot dans la pile)
        fc.write('ADD(i1, 0, r5)\n')    #Compteur pour savoir quand est ce qu'on a terminé de lire le mot
        fc.write('ADD(i1, 2, r6)\n')    #Stocke l'indice de la case contenant le nombre de transition
        fc.write('ADD(0, 0, r7)\n')     #Compteur nb transition
        fc.write('ADD(0, 0, r8)\n')     #Fond de pile donc 0

    return

def generation_CodeRAM(nameFile):
    '''Fonction qui génère le code RAM pour simuler un automate à pile'''

    with open(nameFile, 'a') as fc :

        fc.write('ADD(r7, 1, r7)\n')    #Incrémente le compteur de transition vu car on va en traiter une
        #Génération lignes vérification état q
        fc.write('JNE(r0, i@r3, 21)\n')
        fc.write('ADD(r3, 1, r3)\n')

        #Génération lignes vérificaton mot à lire
        fc.write('JNE(i@r3, i@r2, 23)\n')
        fc.write('ADD(r3, 1, r3)\n')

        #Génération lignes vérification sommet de pile
        fc.write('JNE(r@r1, i@r3, 25)\n')
        fc.write('ADD(r3, 1, r3)\n')    #Pointe sur la taille du mot

        #Génération lignes pour l'ajout du mot dans la pile 
        fc.write('ADD(i@r3, 0, r4)\n')    #Ajoute la taille du mot dans r4 qui va servir de compteur dans l'ajout des lettres
        fc.write('ADD(r3, 1, r3)\n')    #Passe à la première lettre du mot

        #Si c'est epsilon on doit dépiler
        fc.write('JNE(i@r3, 2, 4)\n')   
        fc.write('SUB(r1, 1, r1)\n')    #Décrémente de 1 la tête de lecture du sommet de pile
        fc.write('ADD(r3, 1, r3)\n')    #Passe à q'
        fc.write('JUMP(7)\n')
        
        #Si c'est pas epsilon et donc un mot à écrire dans la pile
        fc.write('ADD(r1, 1, r1)\n')        #Décale le sommet de pile pour ajouter une lettre du mot
        fc.write('ADD(i@r3, 0, r@r1)\n')    #Ajoute la lettre du mot
        fc.write('ADD(r3, 1, r3)\n')        #Décale l'indice pour pointer sur la lettre suivante
        fc.write('SUB(r4, 1, r4)\n')
        fc.write('JE(r4, 0, 2)\n')
        fc.write('JUMP(-5)\n')

        #Changement de l'état courant
        fc.write('ADD(i@r3, 0, r0)\n')
        fc.write('JUMP(14)\n')     #JUMP car on a trouvé une transition donc on va traiter la lettre suivante si le mot n'est pas terminé

        #Si on a regardé toutes les transitions mais aucune qui correspond à notre état c'est que c'est pas reconnu
        fc.write('JE(r7, i@r6, 21)\n')
        
        #Sinon on continue de parcourir les transitions et il faut mettre le pointeur de transition sur la suivante
        #Si la non similarité provenait de q alors r3 pointait sur l'elt 1 de la transition donc on réalise ces instructions et ainsi de suite
        fc.write('ADD(r3, 3, r3)\n')      #Atteindre la position de la taille du mot à écrire dans la pile si la transition était la bonne
        fc.write('ADD(i@r3, r3, r3)\n')   #Se déplacer de la taille du mot
        fc.write('ADD(r3, 2, r3)\n')      #+1 pour être sur l'elt 1 de la transition suivante
        fc.write('JUMP(-25)\n')
        #Si la non similarité provenait de la lettre de la transition
        fc.write('ADD(r3, 2, r3)\n')
        fc.write('ADD(i@r3, r3, r3)\n')
        fc.write('ADD(r3, 2, r3)\n')
        fc.write('JUMP(-4)\n')
        #Si la non similarité provenait du sommet de pile
        fc.write('ADD(r3, 1, r3)\n')    #taille mot
        fc.write('ADD(i@r3, r3, r3)\n') #fin mot
        fc.write('ADD(r3, 2, r3)\n')    #+1 pour se placer sur l'elt 1 de la transition suivante
        fc.write('JUMP(-4)\n')

        #Test fin du mot
        fc.write('SUB(r5, 1, r5)\n')      #Diminue le compteur pour la taille du mot
        fc.write('JE(r5, 0, 5)\n')        #Si compteur 0 ça veut dire que tout le mot a été lu donc que le mot est reconnu

        #Si pas fin du mot mais qu'une transition a été trouvé pour la lettre on passe à la lettre suivante
        fc.write('ADD(r2, 1, r2)\n')    #Incrémente l'indice de la tête de lecture du mot
        fc.write('ADD(0, 0, r7)\n')       #Rénitialise le compteur du nombre de transition testée
        fc.write('ADD(i1, 3, r3)\n')    #Rénitialise le pointeur des transitions
        fc.write('JUMP(-39)\n')           #Recommence le test des transitions pour la nouvelle lettre

        #Mot reconnu
        fc.write('JNE(r0, 1, 4)\n')     #Si l'état courant n'est pas l'état final alors le mot n'est pas reconnu
        fc.write('JNE(r@r1, 0, 3)\n')   #Si l'état courant est l'état final mais que la pile n'est pas vide alors mot pas reconnu
        fc.write('ADD(0, 0, o0)\n')     #Si état final et pile vide alors mot reconnu
        fc.write('JUMP(2)\n')
        #Mot non reconnu
        fc.write('ADD(1, 0, o0)\n')  


def simulationAP(nameFile, mot, fic_transitions):
    '''Fonction principale permettant la simulation d'un automate à pile avec une machine RAM'''

    #Initialisation des registres de l'entrée
    registre_i = registres_entree(mot, fic_transitions)

    with open(nameFile, 'w') as fc :
        #Ecriture de la taille de l'entrée
        fc.write(str(len(registre_i))+', ')

        #Ecriture de l'entrée
        for i in range(len(registre_i)):
            if i == len(registre_i)-1 :
                fc.write(str(registre_i[i])+'\n')
            else :
                fc.write(str(registre_i[i])+', ')
    
    #Initialise les registres pour convertir l'automate à pile en code RAM
    initialisation_registre_AP(nameFile)
    
    #Appelle de la fonction pour générer les lignes de code RAM
    generation_CodeRAM(nameFile)

    return

# Affichage des résultats de la question 6 :
#print(simulationAP('codeRAMtestNegatif.txt', '1111000', 'automateApile.txt'))
#print(simulationAP('codeRAMtestPostif.txt', '11110000', 'automateApile.txt'))
#print(affichage_resultats_terminal(analyse_programme("codeRAMtest1.txt")))

#print(affichage_resultats_fichier(analyse_programme("codeRAMtest1.txt"), 'executionCodeRAM_AP.txt'))
#print(affichage_resultats_fichier(analyse_programme("codeRAMtestPostif.txt"), 'executionCodeRAM_APpositif.txt'))
#print(affichage_resultats_fichier(analyse_programme("codeRAMtestNegatif.txt"), 'executionCodeRAM_AP_testNegatif.txt'))



### Question 7 :
### Faire tourner cette machine RAM sur un automate à pile reconnaissant le langage {anbn | n ∈ N}

# Affichage des résultats de la question 7 :
#print(...)


##### PARTIE 3 : Optimisation de machine RAM

### Question 8 :
### On va représenter le code de la RAM de manière structurée par un graphe orienté. Chaque
### instruction est représentée par un sommet du graphe. Il y a un arc entre deux instructions si on peut
### passer de la première à la seconde en un pas de calcul. Donner une fonction qui créé ce graphe à partir
### du code d’une machine. Les instructions arithmétiques et le JUMP sont de degré sortant 1, tandis que les
### instructions conditionnelles sont de degré sortant 2.

def creation_graphe(code):
    ''' Créé le graphe (représenté sous forme d'un dictionnaire de la machine RAM dont le code est donné en entrée'''

    # Initialisation du dictionnaire avec le sommet de départ D pointant vers la première instruction
    dico_graphe = {'D':[0]}

    for ind_instr in range(len(code)):      # pour chaque instruction
        match_jump = re.match(regex_jump, code[ind_instr])
        match_jumps_spe = re.match(regex_jumps_spe, code[ind_instr])
        if match_jump:          # si c'est un JUMP
            arg1 = int(match_jump.group(2))
            dico_graphe[str(ind_instr)] = [str(ind_instr+int(arg1))]
        elif match_jumps_spe:   # si c'est un JE ou JL
            arg3 = match_jumps_spe.group(4)
            dico_graphe[str(ind_instr)] = [str(ind_instr+1), str(ind_instr+int(arg3))]
        else:     # si c'est une instruction ADD, SUB, MULT ou DIV 
            dico_graphe[str(ind_instr)] = [str(ind_instr+1)]

    return dico_graphe


# Affichage des résultats de la question 8 :
#code = ['ADD(20, 0, o0)', 'JL(i0, 6, 2)', 'ADD(35, 0, o1)', 'ADD(21, 0, o2)']
#graphe_RAM = creation_graphe(code)
#print(graphe_RAM)


### Question 9
### On va appliquer une optimisation d’élimination du code mort. A partir du graphe représentant `
### le code, calculer tous les sommets accessibles à partir de la première instruction.
### Tous les sommets non accessibles correspondent à des instructions qui ne seront jamais exécutées.
### Supprimer ces instructions dans votre code.


def elim_code_mort(code_RAM:list, graphe_RAM:dict):
    ''' Elimine de la machine RAM les instructions qui ne seront jamais exécutées'''

    # Stockage des instructions pouvant être atteintes
    instr_executees = []
    for instr_atteinte in graphe_RAM.values():
        for i in instr_atteinte:
            instr_executees.append(int(i))
    instr_executees = set(instr_executees)
    print('IE : ', instr_executees)

    # Vérification qu'il n'existe pas d'autres instructions
    instr_non_atteintes = []
    for instr in range(len(code_RAM)):
        if instr not in instr_executees:
            instr_non_atteintes.append(instr)
    print('INA : ', instr_non_atteintes)
    
    # Suppression des instructions jamais atteintes
    code_RAM_vivant = code_RAM.copy() # code_RAM sans le code mort
    if instr_non_atteintes != []:       # s'il y a une ou plusieurs instructions à enlever
        for instr in instr_non_atteintes:
            code_RAM_vivant.pop(instr)
    
    return code_RAM_vivant

def ecrit_code_vivant(code_RAM_vivant:list, nom_fichier:str):
    ''' Ecris le code de la machine RAM dans un nouveau fichier'''

    fic = open(nom_fichier, 'w')
    for ligne in code_RAM_vivant:
        fic.write(ligne+'\n')
    fic.close()

    return


# Affichage des résultats de la question 9 :
#code = ['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'JUMP(2)', 'ADD(3, 0, o2)', 'ADD(4, 0, o3)']
#graphe_RAM = creation_graphe(code)
#print(graphe_RAM)
#ecrit_code_vivant(elim_code_mort(code, graphe_RAM), 'code_vivant.txt')


### Question 10 (BONUS):
### Proposer une méthode pour combiner plusieurs instructions en une seule. Par
### exemple, les deux instructions consécutives ADD(4,0,r1), ADD(r1,9,r1) peuvent être remplacées par
### ADD(13,0,r1), si dans le graphe le sommet ADD(r1,9,r1) n’a comme prédécesseur que ADD(4,0,r1).


def trouve_predecesseurs(graphe:dict, sommet:int):
    ''' Retourne les prédecesseurs d'un sommet dans un graphe sous forme de dictionnaire'''
    pred = []
    for key,value in graphe.items():
        if str(sommet) in value:
            pred.append(key)
    return pred


def combine_instr(code_RAM:list, graphe_RAM:dict):
    ''' Combine plusieurs lignes d'instruction en une seule, en particulier quand il s'agit de deux ADD'''

    liste_type_instr = []   # liste qui contiendra le type (ADD, SUB, ...) de chaque instruction
    liste_arg_instr = []    # liste qui contiendra les arguments des instructions de type ADD, SUB, MULT et DIV (sous forme de tuples)

    for instr in code_RAM:
        match_instruc = re.match(regex_instruction, instr)
        if match_instruc:
            type_operation = match_instruc.group(1)
            liste_type_instr.append(type_operation)
            arg1 = match_instruc.group(2)
            arg2 = match_instruc.group(3)
            arg3 = match_instruc.group(4)
            liste_arg_instr.append((arg1, arg2, arg3))

        else:
            liste_type_instr.append('J')    # pour indiquer que l'instruction n'est pas un ADD ni SUB ni MULT ni DIV
            liste_arg_instr.append('J')

    for op in range(len(liste_type_instr)-1):
        if liste_type_instr[op] == 'ADD' and liste_type_instr[op+1] == 'ADD':
            arg_op = liste_arg_instr[op]
            arg_op_suivant = liste_arg_instr[op+1]
            predecesseurs = trouve_predecesseurs(graphe_RAM, op+1)
            if (arg_op[2] == arg_op_suivant[0]) and (arg_op_suivant[0] == arg_op_suivant[2]) and len(predecesseurs) == 1:            
                # Ajout de la nouvelle instruction
                valeur = int(liste_arg_instr[op][0]) + int(liste_arg_instr[op][1]) + int(liste_arg_instr[op+1][1])
                code_RAM[op] = 'ADD(' + str(valeur) + ', 0, ' + liste_arg_instr[op+1][2] + ')'    # remplacer l'instruction
                code_RAM.pop(op+1)  # Supprimer l'instruction

    return code_RAM
    
# Affichage des résultats de la question 10 :
#code = ['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'ADD(3, 0, r0)', 'ADD(r0, 4, r0)']      # modification
#code = ['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'JUMP(2)', 'ADD(3, 0, r0)', 'ADD(r0, 4, r0)']       # pas de modification
#print(combine_instr(code, creation_graphe(code)))


### Fonction pour exécuter toutes les questions

def execute_projet():
    print('Question 1 :')
    print(info_code_RAM(read_RAM('test2.txt')))
    print('Question 2 :')
    print(analyse_instructions(0))
    print(analyse_instructions(1))
    print(analyse_instructions(2))
    print(analyse_instructions(3))
    print('Question 3 :')
    print(analyse_programme("test3.txt"))
    print('Question 4 :')
    print(analyse_programme("question1_ex code recherche max.txt"))
    print('Question 5 :')
    print('a^b : ', analyse_programme("ApuissanceB.txt"))
    print('tri a bulle : ', analyse_programme("triAbulle.txt"))
    print('Question 6 :')
    print()
    print('Question 7 :')
    print()
    print('Question 8 :')
    print(creation_graphe(['ADD(20, 0, o0)', 'JL(i0, 6, 2)', 'ADD(35, 0, o1)', 'ADD(21, 0, o2)']))
    print('Question 9 :')
    code = ['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'JUMP(2)', 'ADD(3, 0, o2)', 'ADD(4, 0, o3)']
    graphe_RAM = creation_graphe(code)
    print(elim_code_mort(code, graphe_RAM), 'code_vivant.txt')
    ecrit_code_vivant(elim_code_mort(code, graphe_RAM), 'code_vivant.txt')
    print('Question 10 :')
    code = ['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'ADD(3, 0, r0)', 'ADD(r0, 4, r0)']
    print(combine_instr(code, creation_graphe(code)))

    return

execute_projet()