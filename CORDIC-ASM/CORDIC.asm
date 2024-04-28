# -------------------------------------------------------------------------------------
# Program to compute sine and cosine using CORDIC algorithm
# The input angle is expected to be in the range (-pi/2, pi) scaled by (2^30)
# The output values are scaled by 2^30
# The program first prompts the user to enter the angle, then computes sine and cosine,
# and finally prompts the user to scale the computed values to get the result
# -------------------------------------------------------------------------------------
# Made by: Kacper Gorski
# Student index number: 331379
# University email: 01187228@pw.edu.pl
# -------------------------------------------------------------------------------------
	.data
prompt: .asciz "Enter angle in range (-pi/2, pi) scaled by (2^30): "
prompt_error: .asciz "You have provided wrong input"
sine_output: .asciz "\nComputed Sine: "
cosine_output: .asciz "\nComputed Cosine: "
end_prompt: .asciz "\nNow scale the computed values by 2^30 to get the result"

# -------------------------------------------------------------------------------------

ACAN_TABLE: .word 0x3243f6a8, 0x1dac6705, 0x0fadbafc, 0x07f56ea6, 0x03feab76, 0x01ffd55b, 0x00fffaaa, 0x007fff55, 0x003fffea, 0x001ffffd, 0x000fffff, 0x0007ffff, 0x0003ffff, 0x0001ffff, 0x0000ffff, 0x00007fff, 0x00003fff, 0x00001fff, 0x00000fff, 0x000007ff, 0x000003ff, 0x000001ff, 0x000000ff, 0x0000007f, 0x0000003f, 0x0000001f, 0x0000000f, 0x00000008, 0x00000004, 0x00000002, 0x00000001, 0x00000000
K: .word 0x26DD3B6A
SCALE: .word 0x40000000		# 2^30 == 0x40000000 == 1073741824.0
.eqv ACAN_SIZE 0x20

# -------------------------------------------------------------------------------------
	.text
	.global main
main:	
	# Load in prompt
	li a7, 4
	la a0, prompt
	ecall
	
	# Take in user input
	li a7, 5
	ecall
	mv t2, a0		# Save user input in register t2
	
	# Check whether input is within range
	li t0, 1685774663	# Pi/2 scaled by 2**30
	bgt a0, t0, error
	li t0, -1685774663	
	blt a0, t0, error

# -------------------------------------------------------------------------------------
	
cordic:
	# Initialize variables for CORDIC algorithm
	lw t0, K		# X 
	li t1, 0		# Y
	# Z already stored in register t2
	
	li t3, 0		# Initialize i iterator
	la t4, ACAN_TABLE	# Acan table pointer
	li t5, ACAN_SIZE	# Acan size

# -------------------------------------------------------------------------------------
	
	# Iterate through the acan table
acan_table_iteration:
	sra s0, t1, t3		# dX: y_point >> i
	sra s1, t0, t3		# dY: x_point >> i
	lw s2, (t4)		# Load dZ: ACAN_TABLE[i]
	
	# Determine sign of computed angle
	bgtz t2, z_greater_than_zero

	# Computed angle is less than 0
	add t0, t0, s0		# x_point += dX 
	sub t1, t1, s1		# y_point -= dY
	add t2, t2, s2		# z += dZ
	j increment_pointer
	
	# Computed angle is greater than 0
z_greater_than_zero:
	sub t0, t0, s0		# x_point -= dX 
	add t1, t1, s1		# y_point += dY
	sub t2, t2, s2		# z -= dZ

increment_pointer:
	addi t3, t3, 1		# Increment i in for loop
	addi t4, t4, 4		# Increment acan table pointer
	bne t3, t5, acan_table_iteration	# Loop

# -------------------------------------------------------------------------------------

	# Output results
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
	
	li a7, 4
	la a0, end_prompt
	ecall
	
	li  a7, 10
	ecall

# -------------------------------------------------------------------------------------
	
	# Handle error for out-of-range input
error:
	li a7, 4
	la a0, prompt_error
	ecall
	
	li a7, 10
	ecall
	
# -------------------------------------------------------------------------------------
