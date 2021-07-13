symbols = {
    'R0':0,
    'R1':1,
    'R2':2,
    'R3':3,
    'R4':4,
    'R5':5,
    'R6':6,
    'R7':7,
    'R8':8,
    'R9':9,
    'R10':10,
    'R11':11,
    'R12':12,
    'R13':13,
    'R14':14,
    'R15':15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN':16384,
    'KBD':24576    
}

def get_instructions(asm):
    instructions = []
    for i in asm.read().splitlines():
        if len(i) > 0:
            if i[0] != '/' and i[1] !='/':
                v = filter_comment(i)
                instructions.append(v)
    return instructions            

def filter_comment(line):
    i = line.split('//')
    return i[0].strip()

def instruction_type(i):
    if i == '(':
        return 'L'
    elif i == '@':
        return 'A'
    else:
        return 'C'        

def strip_paren(s):
    return s.strip('()')

def strip_at(s):
    return s.strip('@')


def symbol(type, s):
    if type == "L":
        i = strip_paren(s)
    elif type == "A":
        i = strip_at(s)
    if i.isnumeric():
        return int(i)
    else:
        return symbols[i]     

def get_c(c):
    instr = c
    if "=" in instr:
        split1 = instr.split("=")
        dest = split1[0]
        instr = split1[1]
    else:
        dest = ""    
    if ";" in instr:
        split2 = instr.split(";")
        comp = split2[0]
        jmp = split2[1]
    else:
        jmp = ""    
        comp = instr    

    return[dest,comp,jmp]
