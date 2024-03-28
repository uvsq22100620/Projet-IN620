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
dico_elt_RAM = {}       #dico de stockage des différents éléments de la machine RAM à générer





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
    global dico_elt_RAM

    registres_i = []    #registre input

    entree = codeRAM[0].split(',')      #la première ligne du code correspond à l'entrée (chaque elt de l'entrée est séparé par une virgule)
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
    dico_elt_RAM["registres_o"]=registres_o

    return dico_elt_RAM

#print(info_code_RAM(read_RAM("question1_ex code recherche max.txt")))


def instruction_ADD(instruction, registres):
    '''Fonction permettant l'analyse et le calcul d'une instruction ADD
    L'argument registres est une liste des trois listes correspondant aux registres'''

    resultat_add = re.match(regex_add, instruction)

    #Recupere les different argument de l'instruction
    if resultat_add:
        arg1 = resultat_add.group(1)
        arg2 = resultat_add.group(2)
        arg3 = resultat_add.group(3)

        #Si les arg1 et arg2 sont des registres et pas des entiers on recup la valeur
        if not re.match(regex_chiffre, arg1):   #test si c'est pas un entier
            resultat_registre_arg1 = re.search(regex_registre, arg1)

            if resultat_registre_arg1 :
                type_registre_arg1 = resultat_registre_arg1.group(1)
                indice_arg1 = int(resultat_registre_arg1.group(2))

            arg1 = int(registres[dico_type_registre[type_registre_arg1]][indice_arg1])
            
        if not re.match(regex_chiffre, arg2):
            resultat_registre_arg2 = re.search(regex_registre, arg2)

            if resultat_registre_arg2 :
                type_registre_arg2 = resultat_registre_arg2.group(1)
                indice_arg2 = int(resultat_registre_arg2.group(2))

            arg2 = int(registres[dico_type_registre[type_registre_arg2]][indice_arg2])

        #Recup le type du registre dans lequel mettre le resultat de l'addition (r ou o) et l'indice de ce registre
        resultat_registre_result = re.search(regex_registre_result, arg3)
        if resultat_registre_result :
            type_registre_result = resultat_registre_result.group(1)
            indice_result = int(resultat_registre_result.group(2))
        
        #Realisation de l'instruction ADD
        registres[dico_type_registre[type_registre_result]][indice_result] = int(arg1)+ int(arg2)

        return registres   
    
    #retourne False quand l'instruction n'est pas correcte (ex : doit écrire dans un registre de type i alors qu'on ne peut que écrire dans r ou o)
    return False

#print(instruction_ADD('ADD(i1, 0, r1)', [['10', '7', ' 25', ' 14', ' 68', ' 39', ' 50', ' 92', ' 3', ' 61', ' 18'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]))

info_code_RAM(read_RAM("question1_ex code recherche max.txt"))
print(instruction_ADD(dico_elt_RAM['codeRAM'][0], [dico_elt_RAM['registres_i'], dico_elt_RAM['registres_r'], dico_elt_RAM['registres_o']]))