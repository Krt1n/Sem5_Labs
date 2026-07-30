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
	LDR R0,=SRC ;Address of SRC
	LDR R1,[R0] ;Stores SRC's value in R1
	
	LDR R2,=DST
	STR R1,[R2] ;Stores the value R2 in R1 which is is the destination address
	
	ADD R0,#4 ;Adds 4 to the SRC address cause each 32 bit number occupies 4 positions in the stack
	ADD R2,#4 ;Similarly
	
	LDR R3,[R0]
	STR R3,[R2]
STOP B STOP
SRC DCD 0x00000001,0x00000002
	AREA mydata,DATA,READWRITE
DST DCD 0,0
	END
