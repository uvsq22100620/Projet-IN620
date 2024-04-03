import re

regex_jump = re.compile(r'(JUMP)\((-?\d+)\)')
res = re.match(regex_jump, 'JUMP(-127)')

if res:
    print("YES CA MARCHE !!!!!!!!!!!!!!")
    print()