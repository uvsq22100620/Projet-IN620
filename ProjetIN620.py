############ IN620-Projet ##############
### LEFEVRE Laura - LE CORRE Camille ###
########################################

#### IMPORTATION DES MODULES ###########
import re

#### VARIABLES GLOBALES ################
## Regex
regex_add = re.compile(r'ADD\((\d+|r\d+|i\d+|o\d+),\s*(\d+|r\d+|i\d+|o\d+),\s*(\d+|r\d+|o\d+)\)')  #regex instruction ex ADD(r0, 0, r1)
regex_registre_result = re.compile(r'([ro])(\d+)')                                                 #regex détail registre dans lequel mettre le resultat de l'instruction ex r10 donne type r et indice 10
regex_registre = re.compile(r'([ir])(\d+)')                                                        #regex détail d'un registre en argument
regex_chiffre = re.compile(r'\d+')                                                                 #vérifier que la chaine de caractère est un chiffre

## Dico
dico_type_registre = {'i':0, 'r':1, 'o':2}






### Question 1 

def read_RAM(fic_in):
    '''Fonction permettant la lecture du fichier dans laquelle le code d'une Machine RAM est stockée 
    et retourne l'ensemble du code dans une liste dont chaque elt correspond à une ligne du code'''

    with open(fic_in, 'r') as fic_in:
        codeRAM = []
        for ligne in fic_in:
            codeRAM.append(ligne[:-1])

    return codeRAM

#print(read_RAM("question1_ex code recherche max.txt"))

def info_code_RAM(codeRAM):
    '''Fonction permettant de récupérer l'entrée de la machine RAM et de créer les différentes listes réprésentant 
    les 3 types de registres (i, r, o)'''

    registres_i = [] 

    entree = codeRAM[0].split(',')
    taille = int(entree[0])
    
    for i in range(1, taille+1) :
        registres_i.append(entree[i])

    registres_r = ['#' for i in range(0, taille*2)]
    registres_o = ['#' for i in range(0, taille*2)]

    return [codeRAM, registres_i, registres_r, registres_o]

#print(info_code_RAM(read_RAM("question1_ex code recherche max.txt")))


def instruction_ADD(instruction, registres):
    '''Fonction permettant l'analyse d'une instruction ADD et effectue l'instruction
    L'arguement registres est une liste des trois listes correspondant aux registres'''

    resultat_add = re.match(regex_add, instruction)

    #Analyse
    if resultat_add:
        arg1 = resultat_add.group(1)
        arg2 = resultat_add.group(2)
        arg3 = resultat_add.group(3)

        #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
        resultat_registre_result = re.search(regex_registre_result, arg3)
        if resultat_registre_result :
            type_registre_result = resultat_registre_result.group(1)
            indice_result = int(resultat_registre_result.group(2))
        
        # Cas ADD avec 2 entiers
        if re.match(regex_chiffre, arg1) and re.match(regex_chiffre, arg2) :    #permet de vérifier si l'argument est un chiffre
            registres[dico_type_registre[type_registre_result]][indice_result] = int(arg1) + int(arg2)

            return registres
        
        # Cas ADD entier + registre
        elif re.match(regex_chiffre, arg1) and not re.match(regex_chiffre, arg2) :
            resultat_registre_arg2 = re.search(regex_registre, arg2)
            
            if resultat_registre_arg2 :
                type_registre_arg2 = resultat_registre_arg2.group(1)
                indice_arg2 = int(resultat_registre_arg2.group(2))

            registres[dico_type_registre[type_registre_result]][indice_result] = int(arg1) + int(registres[dico_type_registre[type_registre_arg2]][indice_arg2])
            
            return registres
        
        # Cas ADD registre + entier
        elif not re.match(regex_chiffre, arg1) and re.match(regex_chiffre, arg2) :
            resultat_registre_arg1 = re.search(regex_registre, arg1)
            
            if resultat_registre_arg1 :
                type_registre_arg1 = resultat_registre_arg1.group(1)
                indice_arg1 = int(resultat_registre_arg1.group(2))

            registres[dico_type_registre[type_registre_result]][indice_result] = int(registres[dico_type_registre[type_registre_arg1]][indice_arg1]) + int(arg2)
            
            return registres
        
        # Cas ADD registre + registre 
        else :
            resultat_registre_arg1 = re.search(regex_registre, arg1)
            resultat_registre_arg2 = re.search(regex_registre, arg2)

            if resultat_registre_arg1 and resultat_registre_arg2 :
                type_registre_arg1 = resultat_registre_arg1.group(1)
                indice_arg1 = int(resultat_registre_arg1.group(2))

                type_registre_arg2 = resultat_registre_arg2.group(1)
                indice_arg2 = int(resultat_registre_arg2.group(2))

            registres[dico_type_registre[type_registre_result]][indice_result] = int(registres[dico_type_registre[type_registre_arg1]][indice_arg1]) + int(registres[dico_type_registre[type_registre_arg2]][indice_arg2])
            
            return registres   
    
    #retourne False quand l'instructions n'est pas correcte (ex : doit écrire dans un registre de type i alors qu'on ne peut que écrire dans r ou o)
    return False

print(instruction_ADD('ADD(i8, i10, r3)', [['10', '7', ' 25', ' 14', ' 68', ' 39', ' 50', ' 92', ' 3', ' 61', ' 18'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]))

