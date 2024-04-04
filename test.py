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
    print("YES CA MARCHE !!!!!!!!!!!!!!")
    type_operation = res2.group(1)
    arg1 = res2.group(2)
    arg2 = res2.group(3)
    arg3 = res2.group(4)

    print(type_operation, arg1, arg2, arg3)
