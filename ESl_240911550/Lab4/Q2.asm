	AREA RESET,DATA,READONLY
	EXPORT __Vectors
	EXPORT Reset_Handler
__Vectors
	DCD	0x10001000 ;Stack Pointer
	DCD Reset_Handler ;Reset Vector
	ALIGN 
	AREA selection, CODE, READONLY
	ENTRY
Reset_Handler
	MOV R0, #5 ; Number whose factorial is required
	BL factorial ; Call recursive function
	
	LDR R1, =0x10000000
	STR R0,[R1]
STOP B STOP
; Recursive Factorial Function, R0=n, returns n! in R0 
factorial
	CMP R0,#0 ; Check if n = 0
	BEQ base ; 0! = 1
	PUSH {R0,LR} ; Save n and return address
	SUB R0,R0, #1; Calculate factorial(n-1)
	BL factorial
	POP {R1,LR}; Restore original n and return address
	MUL R0,R1,R0; R0 = n * factorial(n-1)
	BX LR; Return to caller
base
	MOV R0,#1 ; Base case: 0! = 1
	BX LR
	
	END