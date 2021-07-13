import asm_parser
import asm_code

def main(asm):
    final_binary = ""
    open_ram = 16
    #strip comments from asm
    first_pass = asm_parser.get_instructions(asm)
    second_pass = []     
    #first pass add (LABELS) to symbol table 
    idx1 = 0  
    for i in first_pass:
        instruction_type = asm_parser.instruction_type(i[0])
        if instruction_type == 'L': #add (LABELS) to symbols list
            sym = asm_parser.strip_paren(i)
            asm_parser.symbols[sym] = idx1
        else:
            idx1=idx1+1
            second_pass.append(i) #remove (LABELS) from instructions for second pass

    #second pass add new variable, parse to binary
    for i in second_pass:
        current = ""
        instruction_type = asm_parser.instruction_type(i[0])
        
        if instruction_type == 'A':
            a=asm_parser.strip_at(i)
            if a not in asm_parser.symbols and not a.isnumeric():
                print(i, open_ram)
                asm_parser.symbols[a] = open_ram
                open_ram = open_ram + 1
               
            current = asm_parser.symbol(instruction_type, i)
            bin = "{:0>16b}".format(current) #convert register decimal to 16 bit binary

        elif instruction_type == 'L':
            current = asm_parser.symbol(instruction_type, i)
            bin = "{:0>16b}".format(current) #convert register decimal to 16 bit binary
           
        elif instruction_type == 'C':
            c=asm_parser.get_c(i)
            current = asm_code.c_to_binary(c) #get 13 bit c insruction
            bin = "111" + current #add 3 1's to front 6o complete instruction

        final_binary = final_binary + bin + '\n' 
    return final_binary       

if __name__ == "__main__":
    add_asm = open(r"add/Add.asm", "r")
    add_bin = main(add_asm)
    add_hack = open("add.hack", "w")
    add_hack.write(add_bin)
    max_asm = open(r"max/Max.asm", "r")
    max_bin = main(max_asm)
    max_hack = open("max.hack", "w")
    max_hack.write(max_bin)
    pong_asm = open(r"pong/Pong.asm", "r")
    pong_bin = main(pong_asm)
    pong_hack = open("pong.hack", "w")
    pong_hack.write(pong_bin)
    rect_asm = open(r"rect/Rect.asm", "r")
    rect_bin = main(rect_asm)
    rect_hack = open("rect.hack", "w")
    rect_hack.write(rect_bin)