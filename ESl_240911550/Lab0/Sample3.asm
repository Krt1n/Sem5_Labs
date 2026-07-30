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
	LDRH R1,[R0] ;Stores SRC's value in R1
	
	LDR R2,=DST
	STRH R1,[R2] ;Stores the value R2 in R1 which is is the destination address
	
	ADD R0,#2 ;Adds 4 to the SRC address cause each 32 bit number occupies 4 positions in the stack
	ADD R2,#2 ;Similarly
	
	LDRH R3,[R0]
	STRH R3,[R2]
STOP B STOP
SRC DCW 0x00000001,0x00000002
	AREA mydata,DATA,READWRITE
DST DCW 0,0
	END
