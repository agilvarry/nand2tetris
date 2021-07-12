import asm_parser
import asm_code




def main(asm):
    open_ram = 16
    #strip comments from asm
    instructions = asm_parser.get_instructions(asm)     
    #first pass add (LABELS) to symbol table 
    idx1 = 0  
    for i in instructions:
        instruction_type = asm_parser.instruction_type(i[0])
        if instruction_type == 'L':
            sym = i.strip('()')
            asm_parser.symbols[sym] = idx1
        else:
            idx1=idx1+1
    #second pass add new variable, parse to binary
    
    for i in instructions:
        current = ""
        
        if instruction_type == 'A':
            if i[0] not in asm_parser.symbols:
                asm_parser.symbols[i] = open_ram
                open_ram = open_ram + 1
            current = asm_parser.symbol(i)
        elif instruction_type == 'L':
            current = asm_parser.symbol(i)
        elif instruction_type == 'C':
            current = asm_parser.get_c(i)

        print(current)    
            #TODO convert to Binary

if __name__ == "__main__":
    #add = open(r"add/Add.asm", "r")
    max = open(r"max/Max.asm", "r")
    #pong = open(r"pong/Pong.asm", "r")
    #rect = open(r"rect/Rect.asm", "r")
    # execute only if run as a script
    main(max)