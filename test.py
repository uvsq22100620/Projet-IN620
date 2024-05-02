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

print(int(-1))


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
            #if liste_arg_instr[op]

    return

combine_instr(['ADD(1, 0, o0)', 'ADD(2, 0, o1)', 'JUMP(2)', 'ADD(3, 0, o2)', 'ADD(4, 0, o3)'])