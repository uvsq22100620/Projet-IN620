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
regex_chiffre = re.compile(r'\d+')    
regex_indirection = re.compile(r'([iro])@(i|r)(\d+)')
regex_instruction = re.compile(r'(ADD|SUB|DIV|MULT)\((\d+|r\d+|i\d+|o\d+|([ir])@(i|r)(\d+)),\s*(\d+|r\d+|i\d+|o\d+|([ir])@(i|r)(\d+)),\s*(\d+|r\d+|o\d+|([iro])@(i|r)(\d+))\)')
regex_jump = re.compile(r'(JUMP)\((\d+)\)')
regex_jumps_spe = re.compile(r'(JE|JL)\((\d+|r\d+|i\d+|o\d+|([ir])@(i|r)(\d+)),\s*(\d+|r\d+|i\d+|o\d+|([ir])@(i|r)(\d+)),\s*(\d+)\)')

## Dico
dico_type_registre = {'i': "registres_i", 'r':"registres_r", 'o':"registres_o"}
dico_elt_RAM = {}       #dico de stockage des différents éléments de la machine RAM à générer



##### PARTIE 1 : Simulation de l'exécution d'une machine RAM

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
    for i in range(1, taille+1) :       
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

def desc_registre(registre):
    '''Fonction qui prend en entrée un registre avec le format i|r|o suivit d'un chiffre (par exemple r0)
    et renvoie le type du registre et l'indice du registre'''

    match_registre = re.search(regex_registre, registre)
    print(match_registre, registre)
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

        if desc_arg1[0] == 'o':
            raise Exception("L'instruction est erronée. Vous ne pouvez pas lire les registres de type Output")
            
        arg2 = int(dico_elt_RAM[dico_type_registre[desc_arg2[0]]][desc_arg2[1]])

    #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
    desc_arg3 = desc_registre(arg3)

    if desc_arg3[0] == 'i':
        raise Exception("L'instruction est erronée. Vous ne pouvez pas écrire dans les registres de type Input")

    #Realisation de l'instruction ADD en mettant à jour les registres du dico global
    dico_elt_RAM[dico_type_registre[desc_arg3[0]]][desc_arg3[1]] = int(arg1) + int(arg2)

    return True

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

    return True  

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

    return True  

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

    return True  

def gestion_indirection(registre):
    '''Fonction permettant de gérer l'indirection des registres
    ex : i@r1 correspond au registre ik avec k la valeur dans r1'''

    match = re.match(regex_indirection, registre)
    
    if match :
        registre_type = match.group(1)  # Type de registre (I, R ou O)
        registre_k = match.group(2)  # i ou r
        k = int(match.group(3))  # Chiffre après le r

    indice = dico_elt_RAM[dico_type_registre[registre_k]][k]

    return registre_type + indice

#info_code_RAM(read_RAM("question1_ex code recherche max.txt"))
#print(gestion_indirection('i@i1'))


def analyse_instructions(i_instruc):
    '''Fonction permettant l'analyse d'une instruction de la machine RAM à partir d'une configuration. 
    L'indice est renseigné en paramètre et les registres sont récupérés dans le dictionnaire global'''
    
    #récupère la position en cours dans l'execution du code RAM
    instruction = dico_elt_RAM['codeRAM'][i_instruc[0]]

    match_instruc = re.match(regex_instruction, instruction)
        
    if match_instruc :
        type_operation = match_instruc.group(1)
        arg1 = match_instruc.group(2)
        arg2 = match_instruc.group(3)
        arg3 = match_instruc.group(4)
    else :
        raise Exception("L'instruction n'est pas valide")
    
    #traitement des cas avec indirection
    match_arg1 = re.match(regex_indirection, arg1)
    match_arg2 = re.match(regex_indirection, arg2)

    if match_arg1 :
        arg1 = gestion_indirection(arg1)

    if match_arg2 :
        arg2 = gestion_indirection(arg2)

    #appel de la fonction correspondant à l'instruction
    if type_operation == 'ADD' :
        nv_i_instr = i_instruc + 1  # à optimiser avec un if
        return instruction_ADD(arg1, arg2, arg3)
 
    elif type_operation == 'SUB' :
        nv_i_instr = i_instruc + 1
        return instruction_SUB(arg1, arg2, arg3)
           
    elif type_operation == 'DIV' :
        nv_i_instr = i_instruc + 1
        return instruction_DIV(arg1, arg2, arg3)

    elif type_operation == 'MULT':
        nv_i_instr = i_instruc + 1
        return instruction_MULT(arg1, arg2, arg3)
    
    elif type_operation == 'JUMP':
        nv_i_instr = i_instruc + arg1
        return analyse_instructions((i_instruc + arg1, 0))      # on rappelle la fonction en changeant l'indice de la ligne à évaluer

    elif type_operation == 'JE':
        if arg1 == arg2:
            nv_i_instr = i_instruc + arg3
            return analyse_instructions((i_instruc + arg3, 0))
        else:
            nv_i_instr = i_instruc + 1  

    else:
        if arg1 > arg2:
            nv_i_instr = i_instruc + arg3
            return analyse_instructions((i_instruc + arg3, 0))
        else :
            nv_i_instr = i_instruc + 1      

    return [nv_i_instr, dico_elt_RAM]
       

info_code_RAM(read_RAM("question1_ex code recherche max.txt"))
print(analyse_instructions((0, 0)))
print(dico_elt_RAM['registres_r'])
print(analyse_instructions((1, 0)))
print(dico_elt_RAM['registres_r'])
print(analyse_instructions((2, 0)))
print(dico_elt_RAM['registres_r'])
print(analyse_instructions((3, 0)))
print(dico_elt_RAM['registres_r'])
print('mon analyse : ', analyse_instructions((4,0)))
# lignes de codes de tests que je garde de côté au cas où

#print(instruction_ADD('ADD(i1, 0, r1)', [['10', '7', ' 25', ' 14', ' 68', ' 39', ' 50', ' 92', ' 3', ' 61', ' 18'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]))

#info_code_RAM(read_RAM("question1_ex code recherche max.txt"))
#print(instruction_ADD(dico_elt_RAM['codeRAM'][0], [dico_elt_RAM['registres_i'], dico_elt_RAM['registres_r'], dico_elt_RAM['registres_o']]))
#print(dico_elt_RAM['registres_r'])