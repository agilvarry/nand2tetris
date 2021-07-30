import code_writer
import vm_parser
import os

def main(vm,file_name):
    line_num = 0
    asm = ''
    vm_lines = vm_parser.strip(vm) #strip comments and whitespace

    for line in vm_lines:
        commands = line.split() #separate commands, remove whitespace
        if commands[0] == 'return':
            asm = asm + code_writer.writeReturn(commands[0])
        elif len(commands) == 1: #arithmetic operation
            asm = asm + code_writer.writeArithmetic(commands[0], line_num)
        elif commands[0] == 'label':
            asm = asm + code_writer.writeLabel(commands[1])
        elif commands[0] == 'if-goto':
            asm = asm + code_writer.writeIf(commands[1])
        elif commands[0] == "goto":
            asm = asm + code_writer.writeGoto(commands[1])    
        elif commands[0] == 'function':
            asm = asm + code_writer.writeFunction(commands) 
        elif commands[0] == 'call':
            asm = asm + code_writer.writeCall(commands, line_num) 
        else: #pushpop
            asm = asm + code_writer.writePushPop(commands, file_name)
        line_num = line_num+1   
    
    return asm + code_writer.end_loop()

if __name__ == "__main__":
    in_folder = r'C:\Users\agilvarry\Documents\github\nand2tetris\08\FunctionCalls\NestedCall'
    comment = '//Bootstrap code\n'
    final_asm = comment + "@256\n D=A\n @SP\n M=D\n" + code_writer.writeCall(['call', 'Sys.init','0'])

    for root, dirs, files in os.walk(in_folder):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.vm'):
                file_name = file.split(".")[0] #this gets the name of the file minus.vm for static variable and function names
                
                file_in = open(in_folder + "\\"+ file, "r")

                final_asm = final_asm + main(file_in, file_name)
               
    f_name = in_folder.split("\\")[-1] #this gets the directory name for the output file
    print(f_name)
    out = open(in_folder +"\\"+ f_name+".asm", "w")
    out.write(final_asm)