	AREA RESET,DATA,READONLY
	EXPORT __Vectors
__Vectors
	DCD	0x10001000; SP
	DCD Reset_Handler; Reset Vector
	ALIGN
	
	AREA mycode,CODE,READONLY
	ENTRY
	EXPORT Reset_Handler
	
Reset_Handler
	LDR	R0,=NUM
	LDR R3,=RESULT
	LDRB R1,[R0]
	
	; Upper Nibble
	LSR	R2,R1,#4
	CMP R2,#0xA
	ADDLO R2,R2,#0x30
	ADDHS R2,R2,#0x37
	STRB	R2,[R3]
	
	;Lower Nibble
	AND R2,R1,#0x0F
	CMP R2,#0xA
	ADDLO R2,R2,#0x30
	ADDHS R2,R2,#0x37
	STRB	R2,[R3,#1]
STOP B STOP
NUM DCB 0x21
	AREA mydata,DATA,READWRITE
RESULT SPACE 2
	END

	
	