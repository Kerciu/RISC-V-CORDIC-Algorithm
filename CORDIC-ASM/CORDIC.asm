# Concidering that I cannot use floating-point integers,
# I will ask user for and input in already scaled form
	.data
prompt: .asciz "Enter angle in: "
prompt_error: .asciz "You have provided wrong input"

ACAN_TABLE: .word 0x3243f6a8, 0x1dac6705, 0x0fadbafc, 0x07f56ea6, 0x03feab76, 0x01ffd55b, 0x00fffaaa, 0x007fff55, 0x003fffea, 0x001ffffd, 0x000fffff, 0x0007ffff, 0x0003ffff, 0x0001ffff, 0x0000ffff, 0x00007fff, 0x00003fff, 0x00001fff, 0x00000fff, 0x000007ff, 0x000003ff, 0x000001ff, 0x000000ff, 0x0000007f, 0x0000003f, 0x0000001f, 0x0000000f, 0x00000008, 0x00000004, 0x00000002, 0x00000001, 0x00000000
K: .word 0x26DD3B6A
SCALE: .word 0x40000000		# 2^30 == 0x40000000 == 1073741824.0
	.text
	.global main
main:
	li a7, 4
	la a0, prompt
	ecall
	
	li a7, 5
	mv t0, a0
	ecall
	
end:
	li a7, 10
	ecall