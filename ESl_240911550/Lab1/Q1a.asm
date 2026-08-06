	AREA RESET, DATA, READONLY
	EXPORT __Vectors
	
__Vectors
	DCD 0x10001000
	DCD Reset_Handler
	
	ALIGN
	
	AREA mycode,CODE,READONLY
	ENTRY 
	EXPORT Reset_Handler

Reset_Handler
	MOV R0, #10
	LDR R1,=SRC
	LDR R2,=DST
UP	LDR R3, [R1], #4
	STR R3,[R2], #4
	SUBS R0, #1
	BNE UP
STOP B STOP
SRC DCD 0x1234,0x5678,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8
	AREA mydata,data,readwrite

DST DCD 0,0,0,0,0,0,0,0,0,0
	END