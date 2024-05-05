import re

regex_jump = re.compile(r'(JUMP)\((-?\d+)\)')
res = re.match(regex_jump, 'JUMP(-127)')

#if res:
#    print("YES CA MARCHE !!!!!!!!!!!!!!")
#    print()



regex_instruction = re.compile(r'(ADD|SUB|DIV|MULT)\((\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|i\d+|o\d+|[ir]@[ir]\d+),\s*(\d+|r\d+|o\d+|[ir]@[ir]\d+)\)')
#res2 = re.match(regex_instruction, 'ADD(i@o2, i@r2, i@r0)')
res2 = re.match(regex_instruction, 'ADD(i0, 0, r0)')

if res2:
    #print("YES CA MARCHE !!!!!!!!!!!!!!")
    type_operation = res2.group(1)
    arg1 = res2.group(2)
    arg2 = res2.group(3)
    arg3 = res2.group(4)

    #print(type_operation, arg1, arg2, arg3)

#print(int(-1))


def combine_instr(code_RAM:list):
    ''' Combine plusieurs instructions en une seule si cela est possible '''

    duo_op_compatibles = [('ADD', 'ADD'), ('ADD', 'SUB'), ('SUB', 'ADD'), ('SUB', 'SUB'),
                          ('MULT', 'MULT'), ('MULT', 'DIV'), ('DIV', 'MULT'), ('DIV', 'DIV')]

    liste_type_instr = []   # liste qui contiendra le type (ADD, SUB, ...) de chaque instruction
    liste_arg_instr = []    # liste qui contiendra les arguments des instructions de type ADD, SUB, MULT et DIV (sous forme de tuples)

    for instr in code_RAM:
        match_instruc = re.match(regex_instruction, instr)
        if match_instruc:
            pass
    return

print(eval('(1, 2)'))


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