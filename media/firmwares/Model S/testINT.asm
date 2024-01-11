
; You may customize this and other start-up templates; 
; The location of this template is c:\emu8086\inc\0_com_template.txt

org 100h 
  
MOV AL, -5
SUB AL, 127   ; AL = 7Ch (124) 
;INT          ; Or INT 0
INT 4h         ; Or INTO process error.
mov bx,4
 
int 3h
;IRET

; read character from standard input    	      
mov ah, 1h    ; keyboard input handler
int 21h      ; BIOS interrupt.
mov dh,al    ; the input stored in AL
	
MOV AH, 0Eh  ; teletype output 
MOV AL, 'A'
INT 10h      ; BIOS interrupt.

MOV AH, 2h    ; teletype output
MOV DL, 'B'
INT 21h      ; BIOS interrupt.

ret




