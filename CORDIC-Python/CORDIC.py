# ------------------------------------------
# Python implementation for cordic algorithm
# ------------------------------------------
# Made by Kacper Górski
# ------------------------------------------
from math import atan, sin, cos, pi, sqrt

#  ------------------------------------------
# ------------Auxiliary Functions------------
#  ------------------------------------------


def generate_atans():
    """
    Generate array of arc-tangent
    """
    atan_scale = 0x40000000
    array = []
    for i in range(20):
        array.append(int(atan(2 ** - i) * atan_scale))

    return array


def hexadecimate_array(array):
    """
    Return hex values of the arc-tangent array
    """
    # This function will be used for .asm program to generate array
    for idx, elem in enumerate(array):
        array[idx] = hex(elem)
    return array

#  ------------------------------------------
#  ------------------CORDIC------------------
#  ------------------------------------------


def K_value(iterations):
    """
    Determine scaling factor
    """
    K = 1.0
    for i in range(0, iterations):
        K = K * (1.0 / sqrt(1 + 2.0 ** (-2 * i)))
    return K


def CORDIC(theta_deg, iterations):
    """
    Cordic Algorithm:
    Find cosine and sine through iterations
    :param theta_deg: Angle in degrees
    :param iterations: Number of iterations
    :return: Tuple of cosine and sine values
    """
    # Initial point on a plot
    xy_point = (1, 0)

    # Fetch scaling factor
    K = K_value(iterations)

    for i in range(0, iterations):

        # Determine rotation based on an angle sign
        d = 1.0
        if theta_deg < 0:
            d = -1.0

        # Extract x and y coordinates
        x, y = xy_point[0], xy_point[1]

        # Update coordinates using CORDIC algorithm equations
        xy_point = (x - (d * (2.0 ** (-i))) * y, y + (d * (2.0 ** (-i))))

        # Update angle
        theta_deg = theta_deg - (d * atan(2 ** (-i)))

    # Scale and return cosine and sine values
    return K * xy_point[0], K * xy_point[1]


#  ------------------------------------------
#  -------------------Main-------------------
#  ------------------------------------------

if __name__ == "__main__":
    # scale = 0x26DD3B6A
    # cordic_K = 0x100000000

    table = generate_atans()
    len_of_array = len(table)

    angle = pi / 6
    actual_sin = sin(angle)
    actual_cos = cos(angle)
    cordic_cos, cordic_sin = CORDIC(angle, len_of_array)

    print("Angle:", angle)
    print("Actual Sin:", actual_sin)
    print("CORDIC Sin:", cordic_sin)
    print("Actual Cos:", actual_cos)
    print("CORDIC Cos:", cordic_cos)
