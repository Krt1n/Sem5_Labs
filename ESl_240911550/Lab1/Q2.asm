	AREA RESET,DATA, READONLY
	EXPORT __Vectors

__Vectors
	DCD 0x10001000
	DCD Reset_Handler
	
	ALIGN
	
	AREA mycode, CODE, READONLY
	ENTRY
	EXPORT Reset_Handler

Reset_Handler
	MOV R3, #5
	LDR R0, =SRC
	LDR R1, =SRC+(N-1)*4
UP	LDR	R2,	[R0],#4
	LDR R4,	[R1]
	
	STR R4,[R0,#-4]
	STR R2,[R1],#-4
	
	SUBS R3,R3,#1
	BNE UP
STOP B STOP
N EQU 10
	AREA mydata,data,readwrite
SRC	DCD 0,0,0,0,0,0,0,0,0,0
	END