arithmetic = {
    'add': '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=M+D \n@SP \nM=M-1\n',
    'sub' : '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=M-D \n@SP \nM=M-1\n',
    'neg' : '@SP \nA=M \nA=A-1 \nD=M \nM=M-D \nM=M-D\n',
    'and' : '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=D&M \n@SP \nM=M-1\n',
    'or' : '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=D|M \n@SP \nM=M-1\n',
    'not' : '@SP \nA=M \nA=A-1 \nM=!M \n'
}
temp = {
    "0": "@5",
    "1": "@6",
    "2": "@7",
    "3": "@8",
    "4": "@9",
    "5": "@10",
    "6": "@11",
    "7": "@12"
}
segments = {
    "local": "LCL",
    "argument" : "ARG",
    "this" : "THIS",
    "that" : "THAT"
}
pointer = {
    "0": "@THIS",
    "1": "@THAT"
}


def writeArithmetic(command, line_num):
    
    if command == 'eq':
       return f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @EQ{line_num}\n D;JEQ\n @NEQ{line_num}\n 0;JMP\n (EQ{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\nM=-1\n @CONT{line_num}\n 0;JMP\n (NEQ{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    elif command =='lt':
        return f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @LT{line_num}\n D;JLT\n @NLT{line_num}\n 0;JMP\n (LT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=-1\n @CONT{line_num}\n 0;JMP\n (NLT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    elif command == "gt":
        return f"@SP\n A=M\n A=A-1\n D=M\n A=A-1\n D=M-D\n @GT{line_num}\n D;JGT\n @NGT{line_num}\n 0;JMP\n (GT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=-1\n @CONT{line_num}\n 0;JMP\n (NGT{line_num})\n @SP\n A=M\n A=A-1\n A=A-1\n M=0\n (CONT{line_num})\n @SP\n M=M-1\n"
    else:    
        return arithmetic[command]

def writePushPop(commands,file_name =""):
    
    if commands[0] == 'push':
        if commands[1] == 'constant':
            return f"@{commands[2]} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1\n"
        elif commands[1] == "temp":
            return f"{temp[commands[2]]}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n" 
        elif commands[1] == "pointer":
            return f"{pointer[commands[2]]}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
        elif commands[1] == "static":
            return f"@{file_name}.{commands[2]}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n" 
        else:
            return f"@{commands[2]}\n D=A\n @{segments[commands[1]]}\n A=D+M\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n" 
    if commands[0] == 'pop':
        if commands[1] == "temp":
            return f"@SP\n M=M-1\n A=M\n D=M\n {temp[commands[2]]}\n M=D\n" 
        elif commands[1] == "pointer":
            return f"@SP\n M=M-1\n A=M\n D=M\n {pointer[commands[2]]}\n M=D\n" 
        elif commands[1] == "static":
            return f"@SP\n M=M-1\n A=M\n D=M\n @{file_name}.{commands[2]}\n M=D\n" 
        else:    
            return f"@{commands[2]}\n D=A\n @{segments[commands[1]]}\n D=D+M\n @R13\n M=D\n @SP\n M=M-1\n A=M\n D=M\n @R13\n A=M\n M=D\n" 

def writeLabel(command):
    return f"({command})\n"           

def writeIf(command):
    return f"@SP\n M=M-1\n A=M\n D=M\n @{command}\n D;JNE\n"

def writeGoto(command):
    return f"@{command}\n 0;JMP\n"    

def writeFunction(commands):
    i = int(commands[2])
    pushCommand = ['push', 'constant', '0']
    local = ""
    while i > 0:
        print(i)
        local = local + writePushPop(pushCommand)
        i = i - 1
    return f"({commands[1]})\n {local}"

def writeReturn(command):
    
    return "@LCL \n D=M \n @endFrame \n M=D \n @5 \n  D=A \n  @endFrame \n A=M-D \n D=M \n @retAddr \n M=D \n @SP\n M=M-1 \n @SP\n A=M \n D=M \n @ARG \n A=M \n M=D \n @ARG \n D=M+1 \n @SP \n M=D \n @1 \nD=A\n @endFrame\n A=M-D\n D=M \n @THAT \n M=D \n @2 \n D=A\n @endFrame\n A=M-D\n D=M \n @THIS \n M=D \n @3 \n D=A\n @endFrame\n A=M-D\n D=M \n @ARG \n M=D \n @4 \n D=A\n @endFrame\n A=M-D\n D=M \n @LCL \n M=D \n @retAddr \n A=M \n 0;JMP \n"

def writeCall(commands,line_num):
    returnAddress = f"{commands[1]}.return.{line_num}"
    nArgs = commands[2]
    return f"@{returnAddress} \n D=A \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n @LCL \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n @ARG \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n @THIS \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n @THAT \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n @5 \n D=A \n @{nArgs} \n D=D+A \n @SP \n D=M-D \n @ARG \n M=D \n @SP \n D=M  \n @LCL \n M=D \n @{commands[1]}\n  0;JMP\n ({returnAddress}) \n"

def end_loop():
    return "(END) \n@END \n0;JMP "