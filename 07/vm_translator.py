import code_writer
import vm_parser


def main(vm):
    asm = ''
    vm_lines = vm_parser.strip(vm) #strip comments and whitespace
    for line in vm_lines:
        commands = line.split() #separate commands, remove whitespace
        if len(commands) == 1:
            asm = asm + code_writer.writeArithmetic(commands[0])
        else:
            asm = asm + code_writer.writePushPop(commands)
    return asm + code_writer.end_loop()

if __name__ == "__main__":
    # in = open(r"StackArithmetic\SimpleAdd\SimpleAdd.vm", "r")
    # convert = main(simpleAdd_vm)
    # out = open("StackArithmetic\SimpleAdd\simpleAdd.asm", "w")
    # out.write(convert)
    file_in = open(r"StackArithmetic\StackTest\StackTest.vm", "r")
    convert = main(file_in)
    out = open("StackArithmetic\StackTest\StackTest.asm", "w")
    out.write(convert)