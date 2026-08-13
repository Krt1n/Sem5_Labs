	AREA RESET,DATA,READONLY
	EXPORT __Vectors
__Vectors
	DCD 0x10001000
	DCD Reset_Handler
	ALIGN
	AREA mycode,CODE,READONLY
	ENTRY
	EXPORT Reset_Handler
Reset_Handler
	LDR R0, =N1; Address of Minuend (N1)
    LDR R1, =N2; Address of Subtrahend (N2)
    LDR R2, =DIFF; Address of Result (DIFF)
	
	LDR R3,[R0],#4 ;Load next word from R0
	LDR R4,[R1],#4 ;Load next word from R1
	SUBS R5,R3,R4 ; R5 = R3-R4
	STR R5,[R2],#4 ;Store result word in DIFF
	MOV R6,#3
	
UP	LDR R3,[R0],#4; Load next word from N1
	LDR R4,[R1],#4; Load next word from N2
	SBCS R5,R3,R4; R5 = R3 - R4 - Borrow (SBCS uses Carry flag)
	STR R5,[R2],#4; Store word in DIFF
	
	SUB R6,#1; Doesn't alter carry flag
	TEQ R6,#0; Check if counter is 0 (Does NOT alter Carry flag)
	BNE UP
STOP B STOP
N1 DCD 0x456789AB, 0x3456789A, 0x23456789, 0x89ABCDEF
N2 DCD 0x11111111, 0x22222222, 0x33333333, 0x44444444
	AREA myarea,DATA,READWRITE
DIFF DCD 0,0,0,0
	END

	