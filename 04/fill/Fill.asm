// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


@8192 // get the size of the screen
D=A
@SCREEN
D=D+A //add it to the address of ther screen to tHe end address
@screensize
M=D

@RESET
0;JMP

// set the pointer to start at the value of screen
(RESET)
    @SCREEN
    D=A
    @pointer
    M=D
    @LOOP 
    0;JMP

//check if a key is pressed or not
(LOOP)
    @KBD
    D=M
    @BLACK
    D;JGT
    @WHITE
    D;JEQ

//set the pixel value
(BLACK)
    @pixel
    M=-1
    @FILL
    0;JMP

(WHITE)
    @pixel
    M=0
    @FILL
    0;JMP

(FILL)
    @pixel //get the pixel value, set it to D
    D=M
    @pointer //set address to pointer, and 
    A=M //new address and value of pointer
    M=D //value of new address to pixel color
    @pointer
    M=M+1 //increment pointer
    D=M //set pointer to D
    @screensize
    D=M-D //get difference between screen size and pointer
    @RESET
    D;JLE
    @LOOP
    0;JMP
    

