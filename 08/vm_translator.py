import code_writer
import vm_parser


def main(vm):
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
        else: #pushpop
            asm = asm + code_writer.writePushPop(commands)
        line_num = line_num+1   
    
    return asm + code_writer.end_loop()

if __name__ == "__main__":
    file_in = open(r"FunctionCalls\SimpleFunction\SimpleFunction.vm", "r")
    convert = main(file_in)
    out = open("FunctionCalls\SimpleFunction\SimpleFunction.asm", "w")
    out.write(convert)