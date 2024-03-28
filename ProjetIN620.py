############ IN620-Projet ##############
### LEFEVRE Laura - LE CORRE Camille ###
########################################

### Question 1 

def read_RAM(fic_in):
    '''Fonction permettant la lecture du fichier dans laquelle le code d'une Machine RAM est stockée'''

    with open(fic_in, 'r') as fic_in:
        codeRAM = []
        for ligne in fic_in:
            codeRAM.append(ligne[:-1])

    return codeRAM

print(read_RAM("question1_ex code recherche max.txt"))