# Concidering that I cannot use floating-point integers,
# I will ask user for input in already scaled form
	.data
prompt: .asciz "Enter angle in: "
prompt_error: .asciz "You have provided wrong input"
sine_output: .asciz "\nSine: "
cosine_output: .asciz "\nCosine: "

ACAN_TABLE: .word 0x3243f6a8, 0x1dac6705, 0x0fadbafc, 0x07f56ea6, 0x03feab76, 0x01ffd55b, 0x00fffaaa, 0x007fff55, 0x003fffea, 0x001ffffd, 0x000fffff, 0x0007ffff, 0x0003ffff, 0x0001ffff, 0x0000ffff, 0x00007fff, 0x00003fff, 0x00001fff, 0x00000fff, 0x000007ff, 0x000003ff, 0x000001ff, 0x000000ff, 0x0000007f, 0x0000003f, 0x0000001f, 0x0000000f, 0x00000008, 0x00000004, 0x00000002, 0x00000001, 0x00000000
K: .word 0x26DD3B6A
SCALE: .word 0x40000000		# 2^30 == 0x40000000 == 1073741824.0
.eqv ACAN_SIZE 0x20

	.text
	.global main
main:	
	li a7, 4		# Load in prompt
	la a0, prompt
	ecall
	
	li a7, 5		# Take in user input
	ecall
	mv t2, a0		# Z
	
	li t0, 1685774663	# Pi/2 scaled by 2**30
	bgt a0, t0, error
	li t0, -1685774663
	blt a0, t0, error
	
cordic:
	lw t0, K		# X 
	li t1, 0		# Y
	li t3, 0		# i
	la t4, ACAN_TABLE	# Acan table pointer
	li t5, ACAN_SIZE	# Acan size
	
# for(i = 0; i < ACAN_SIZE; ++i)
acan_table_iteration:
	sra s0, t1, t3		# dX
	sra s1, t0, t3		# dY
	lw s2, (t4)		# dZ
	
	bgtz t2, z_greater_than_zero

	add t0, t0, s0		# x_point += dX 
	sub t1, t1, s1		# y_point -= dY
	add t2, t2, s2		# z += dZ
	j increment_pointer
	
z_greater_than_zero:
	sub t0, t0, s0		# x_point -= dX 
	add t1, t1, s1		# y_point += dY
	sub t2, t2, s2		# z -= dZ

increment_pointer:
	addi t3, t3, 1
	addi t4, t4, 4
	bne t3, t5, acan_table_iteration

end:	
	li a7, 4
	la a0, sine_output
	ecall
	
	li a7, 1
	mv a0, t1
	ecall
	
	li a7, 4
	la a0, cosine_output
	ecall
	
	li a7, 1
	mv a0, t0
	ecall
	
	li  a7, 10
	ecall

error:
	li a7, 4
	la a0, prompt_error
	ecall
	
	li a7, 10
	ecall
