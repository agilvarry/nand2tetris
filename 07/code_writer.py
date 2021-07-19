arithmetic = {
    'add': '@SP \nA=M \nA=A-1 \nD=M \nA=A-1 \nM=M+D \n@SP \nM=M-1\n'
}


def writeArithmetic(command):
    comment = f"//'{command}\n"
    return arithmetic[command]

def writePushPop(commands):
    comment = f"// {commands}\n"
    if commands[0] == 'push':
        return f"@{commands[2]} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1\n"

def end_loop():
    return "(END) \n@END \n0;JMP "