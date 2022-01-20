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

// Put your code here.

@8192
D=A
@n
M=D // size of screen memory map

@SCREEN
D=A
@address
M=D // base adress of the screen

@i
M=0 // i = 0


(INPUT)
    @KBD
    D=M
    @FILL
    D;JNE // if a key is being pressed, fill the screen
    @CLEAR
    D;JEQ // if a key is not being pressed, clear the screen


(FILL)
    @i
    D=M
    @n
    D=D-M
    @STOP
    D;JGT // if i > n goto STOP

    @address
    D=M
    @i
    A=D+M
    M=-1

    @i
    M=M+1 // i = i+1


    @INPUT
    0;JMP


(CLEAR)
    @i
    D=M
    @n
    D=D-M
    @STOP
    D;JGT // if i > n goto STOP

    @address
    D=M
    @i
    A=D+M
    M=0

    @i
    M=M+1 // i = i+1


    @INPUT
    0;JMP


(STOP)
    @i
    M=0 
    @INPUT
    0;JMP // reset the counter and get the input


(END)
    @END
    0;JMP
