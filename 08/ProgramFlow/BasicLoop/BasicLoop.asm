//Bootstrap code
// ['push', 'constant', '0']
@0 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1
// ['pop', 'local', '0']
@0
 D=A
 @LCL
 D=D+M
 @R13
 M=D
 @SP
 M=M-1
 A=M
 D=M
 @R13
 A=M
 M=D
(LOOP_START)
// ['push', 'argument', '0']
@0
 D=A
 @ARG
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
// ['push', 'local', '0']
@0
 D=A
 @LCL
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
//add
@SP 
A=M 
A=A-1 
D=M 
A=A-1 
M=M+D 
@SP 
M=M-1
// ['pop', 'local', '0']
@0
 D=A
 @LCL
 D=D+M
 @R13
 M=D
 @SP
 M=M-1
 A=M
 D=M
 @R13
 A=M
 M=D
// ['push', 'argument', '0']
@0
 D=A
 @ARG
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
// ['push', 'constant', '1']
@1 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1
//sub
@SP 
A=M 
A=A-1 
D=M 
A=A-1 
M=M-D 
@SP 
M=M-1
// ['pop', 'argument', '0']
@0
 D=A
 @ARG
 D=D+M
 @R13
 M=D
 @SP
 M=M-1
 A=M
 D=M
 @R13
 A=M
 M=D
// ['push', 'argument', '0']
@0
 D=A
 @ARG
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
@SP
 M=M-1
 A=M
 D=M
 @LOOP_START
 D;JGT
// ['push', 'local', '0']
@0
 D=A
 @LCL
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
(END) 
@END 
0;JMP 