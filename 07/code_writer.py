arithmetic = {
    'add': '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=M+D \n@SP \nM=M-1\n',
    'sub' : '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=M-D \n@SP \nM=M-1\n',
    'neg' : '@SP \nA=M \nA=A-1 \nD=M \nM=M-D \nM=M-D\n',
    'and' : '',
    'or' : '',
    'not' : ''
}


def writeArithmetic(command, line_num):
    comment = f"//{command}\n"
    if command == 'eq':
       return comment + f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @EQ{line_num}\n D;JEQ\n @NEQ{line_num}\n 0;JMP\n (EQ{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\nM=-1\n @CONT{line_num}\n 0;JMP\n (NEQ{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    elif command =='lt':
        return comment + f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @LT{line_num}\n D;JLT\n @NLT{line_num}\n 0;JMP\n (LT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=-1\n @CONT{line_num}\n 0;JMP\n (NLT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    elif command == "gt":
        return comment + f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @GT{line_num}\n D;JGT\n @NGT{line_num}\n 0;JMP\n (GT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=-1\n @CONT{line_num}\n 0;JMP\n (NGT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    else:    
        return comment + arithmetic[command]

def writePushPop(commands):
    comment = f"// {commands}\n"
    if commands[0] == 'push':
        return comment + f"@{commands[2]} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1\n"

def end_loop():
    return "(END) \n@END \n0;JMP "