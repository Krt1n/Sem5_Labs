	AREA RESET,DATA,READONLY
	EXPORT __Vectors
	EXPORT Reset_Handler
N EQU 7 ; No of ele in array
__Vectors
	DCD	0x40001000 ;Stack Pointer
	DCD Reset_Handler ;Reset Vector
	ALIGN 
	AREA selection, CODE, READONLY
	ENTRY
Reset_Handler
	LDR R0,=list 
	LDR R1,=result
	MOV R2,#0
copy
	LDR R3,[R0,R2,LSL #2] ;Read array
	STR R3,[R1,R2,LSL #2] ;copy to result
	ADD R2,R2,#1 
	CMP R2,#N
	BLT copy
	
	LDR R0,=result
	MOV R1,#0
;Selection Sort
;Find minimum element in unsorted part and swap it with array[i]

outer
	CMP R1,#N-1 ;Last Element needs no searching so that only 0-(N-2) are processed
	BGE STOP ;If R1>=N-1, sorting is complete
	MOV R2,R1 ;Assume curr in min and that R2 stores min_idx
	ADD R3,R1,#1; Start searching from next ele bcz R1 is assumed to be min
inner
	CMP R3, #N ;Check if all arr ele's are checked
	BGE swap ; If j reaches 10, min has been found
	LDR R4,[R0,R3,LSL #2] ; Load array[j] into R4
						  ; LSL #2 is basically multiply each index by 4
						  ; bcz each ele is 32 bits
	LDR R5,[R0,R2,LSL #2] ; Load array[min] into R5
						  ; LSL #2 is basically multiply each index by 4
						  ; bcz each ele is 32 bits
	CMP R4,R5			  ;CMP array[j] with curr min
	MOVLO R2,R3 		  ; If array[j] is smaller,R2 stores it's idx as new min
	ADD R3,R3,#1		  ; Move j to next element
	B	inner			  ; Continue the searc for the min
	
swap
	CMP R2,R1 ;check if min already at pos i
	BEQ	next  ;If yes, then no swap is required
	
	LDR R4,[R0,R1,LSL #2] ;Load Array[i]
	LDR R5,[R0,R2,LSL #2] ;Load array[min]

	STR R5,[R0,R1,LSL #2] ;Put the smallest value at pos i
	STR R4,[R0,R2,LSL #2] ;Put old value at the min pos
next
	ADD R1, R1, #1		   ;Move to the next pos
	B outer 			   ; Repeat
STOP B STOP
list DCD 0x10,0x05,0x33,0x24,0x56,0x77,0x21
	AREA data1,DATA,READWRITE
result SPACE N*4
	END