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
regex_jumps_spe = re.compile(r'(JE|JL)\((\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(-?\d+)\)')

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
#print(read_RAM('test2.txt))


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

    #récupère la position en cours dans l'execution du code RAM
    instruction = dico_elt_RAM['codeRAM'][i_instruc]

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
    print(dico_elt_RAM)

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


def affichage_resultats_fichier(liste_config:list, nom_fichier:str):

    fic = open(nom_fichier, 'w')
    
    for i_config in range(len(liste_config)):
        fic.write('iteration '+str(i_config)+'\n')
        reg_i = liste_config[i_config]['registres_i']
        reg_r = liste_config[i_config]['registres_r']
        reg_o = liste_config[i_config]['registres_o']
        
        for k in range(len(reg_i)):
            fic.write('i'+str(k)+'  ')
        fic.write('     ')
        for k in range(len(reg_r)):
            fic.write('r'+str(k)+'  ')
        fic.write('     ')
        for k in range(len(reg_o)):
            fic.write('o'+str(k)+'  ')

        fic.write('\n')


        for k in range(len(reg_i)):
            fic.write(str(reg_i[k])+(4-len(str(reg_i[k])))*' ')
        fic.write('     ')
        for k in range(len(reg_r)):
            fic.write(str(reg_r[k])+(4-len(str(reg_r[k])))*' ')
        fic.write('     ')
        for k in range(len(reg_o)):
            fic.write(str(reg_o[k])+(4-len(str(reg_o[k])))*' ')
        fic.write('\n')
        fic.write('______________________________________________________________________\n')

    fic.close()

    return

# Affichage des résultats de la question 4 :
#print(analyse_programme("question1_ex code recherche max.txt"))
#print(affichage_resultats_terminal(analyse_programme("test2.txt")))
#print(affichage_resultats_fichier(analyse_programme("test2.txt")))


### Question 5:
### Donner le code des machines de RAM suivantes :
### - Avec en entrée deux entiers a et b, calculer a^b => fichier ApuissanceB.txt
print(analyse_programme("ApuissanceB.txt"))
### - Avec comme entrée un tableau d’entiers, écrire le tableau trié dans la sortie (par un tri à bulle) => fichier triAbull.txt
print(analyse_programme("triAbulle.txt"))



# lignes de codes de tests que je garde de côté au cas où

#print(instruction_ADD('ADD(i1, 0, r1)', [['10', '7', ' 25', ' 14', ' 68', ' 39', ' 50', ' 92', ' 3', ' 61', ' 18'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]))

#info_code_RAM(read_RAM("question1_ex code recherche max.txt"))
#print(instruction_ADD(dico_elt_RAM['codeRAM'][0], [dico_elt_RAM['registres_i'], dico_elt_RAM['registres_r'], dico_elt_RAM['registres_o']]))
#print(dico_elt_RAM['registres_r'])


##### PARTIE 2 : Automate à pile

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

#print(registres_entree('01010001', 'automateApile1.txt'))

# Affichage des résultats de la question 6 :


### Question 7 :
### Faire tourner cette machine RAM sur un automate à pile reconnaissant le langage {anbn | n ∈ N}




# Affichage des résultats de la question 7 :

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
#ecrit_code_vivant(elim_code_mort(code, graphe_RAM), 'code_vivant.txt')


### Question 10 (BONUS):
### Proposer une méthode pour combiner plusieurs instructions en une seule. Par
### exemple, les deux instructions consécutives ADD(4,0,r1), ADD(r1,9,r1) peuvent être remplacées par
### ADD(13,0,r1), si dans le graphe le sommet ADD(r1,9,r1) n’a comme prédécesseur que ADD(4,0,r1).

def combine_instr(code_RAM:list):
    ''' Combine plusieurs instructions en une seule si cela est possible '''

    duo_op_compatibles = [('ADD', 'ADD'), ('ADD', 'SUB'), ('SUB', 'ADD'), ('SUB', 'SUB'),
                          ('MULT', 'MULT'), ('MULT', 'DIV'), ('DIV', 'MULT'), ('DIV', 'DIV')]

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
    print(liste_type_instr)
    print(liste_arg_instr)

    for op in range(len(liste_type_instr)-1):
        if (liste_type_instr[op], liste_type_instr[op+1]) in duo_op_compatibles:
            arg_op = liste_arg_instr[op]
            arg_op_suivant = liste_arg_instr[op+1]
            if (arg_op[2] == arg_op_suivant[0]) and (arg_op_suivant[0] == arg_op_suivant[2]):
                pass
            elif (arg_op[2] == arg_op_suivant[1]) and (arg_op_suivant[1] == arg_op_suivant[2]):
                pass

    return

def combine_instr2(code_RAM:list):

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
            if (arg_op[2] == arg_op_suivant[0]) and (arg_op_suivant[0] == arg_op_suivant[2]):            
                # Ajout de la nouvelle instruction
                valeur = liste_arg_instr[op][0] + liste_arg_instr[op][1] + liste_arg_instr[op+1][1]
                code_RAM[op] = 'ADD(' + str(valeur) + ', 0' + liste_arg_instr[op+1][2] + ')'    # remplacer l'instruction
                code_RAM.pop(op+1)  # Supprimer l'instruction
        return
    
# Affichage des résultats de la question 10 :
#combine_instr(['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'JUMP(2)', 'ADD(3, 0, o2)', 'ADD(4, 0, o3)'])


### Fonction pour exécuter toutes les questions

def execute_projet():
    print('Question 1 :')
    print()
    print('Question 2 :')
    print()
    print('Question 3 :')
    print()
    print('Question 4 :')
    print()
    print('Question 5 :')
    print()
    print('Question 6 :')
    print()
    print('Question 7 :')
    print()
    print('Question 8 :')
    print()
    print('Question 9 :')
    print()
    print('Question 10 :')
    print()

    return

execute_projet()