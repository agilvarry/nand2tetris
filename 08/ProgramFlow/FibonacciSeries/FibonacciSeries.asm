// ['push', 'argument', '1']
@1
 D=A
 @ARG
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
// ['pop', 'pointer', '1']
@SP
 M=M-1
 A=M
 D=M
 @THAT
 M=D
// ['push', 'constant', '0']
@0 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1
// ['pop', 'that', '0']
@0
 D=A
 @THAT
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
// ['push', 'constant', '1']
@1 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1
// ['pop', 'that', '1']
@1
 D=A
 @THAT
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
// ['push', 'constant', '2']
@2 
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
(MAIN_LOOP_START)
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
 @COMPUTE_ELEMENT
 D;JGT
@END_PROGRAM
 0;JMP
(COMPUTE_ELEMENT)
// ['push', 'that', '0']
@0
 D=A
 @THAT
 A=D+M
 D=M
 @SP
 A=M
 M=D
 @SP
 M=M+1
// ['push', 'that', '1']
@1
 D=A
 @THAT
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
// ['pop', 'that', '2']
@2
 D=A
 @THAT
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
// ['push', 'pointer', '1']
@THAT
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
//add
@SP 
A=M 
A=A-1 
D=M 
A=A-1 
M=M+D 
@SP 
M=M-1
// ['pop', 'pointer', '1']
@SP
 M=M-1
 A=M
 D=M
 @THAT
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
@MAIN_LOOP_START
 0;JMP
(END_PROGRAM)
(END) 
@END 
0;JMP 