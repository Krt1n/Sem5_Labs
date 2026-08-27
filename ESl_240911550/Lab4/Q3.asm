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
	LDR R0,=list ;R0 points to first array ele
	MOV R1,#10	;R1 = no. of ele
	MOV R2,#0x24 ;R2=element to search for
search_loop
 	LDR R3,[R0],#4 ;Load curr,move to next
	CMP R3,R2 ; Compare arr ele with searh value
	BEQ	found ; If equal, ele found
	SUBS R1,R1,#1 ;decrement counter
	BNE search_loop 
not_found
	MOV R4,#0 ;R4=0 means no element was found
	LDR R5,=0x10000000
	STR R4,[R5]
 	B STOP
found
	MOV R4,#1 ;R4=1 means element was found
	LDR R5,=0x10000000
	STR R4,[R5]
STOP B STOP
list DCD  0x10,0x05,0x33,0x24,0x56,0x77,0x21,0x04,0x87,0x01
	END