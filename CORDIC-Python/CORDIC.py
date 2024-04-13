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
    for i in range(32):
        array.append(int(atan(2 ** - i) * atan_scale))

    return array


def hexadecimate_array(array):
    """
    Return hex values of the arc-tangent array
    """
    # This function will be used for .asm program to generate array
    for idx, elem in enumerate(array):
        array[idx] = f"{elem:#0{10}x}"
    return array


def convert_to_int(value):
    """
    Return integer value (very big value) of decimal portion
    """
    string_value = str(value)
    split_value = string_value.split('.')
    return int((split_value[1])[:9])

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


def SCALE():
    return 2**30


def CORDIC(theta_deg, ACAN_TABLE, iterations):
    """
    Cordic Algorithm:
    Find cosine and sine through iterations
    :param theta_deg: Angle in degrees
    :param ACAN_TABLE: Table of precomputed arctangent
    :param iterations: Number of iterations
    :return: Tuple of cosine and sine values
    """
    # Initial point on a plot
    K = int(K_value(32) * SCALE())
    x, y, z = int(K), 0, theta_deg

    # Fetch scaling factor

    for i in range(iterations):

        dx, dy, dz = y >> i, x >> i, ACAN_TABLE[i]
        # Determine rotation based on an angle sig
        if z < 0:
            x += dx
            y -= dy
            z += dz

        else:
            x -= dx
            y += dy
            z -= dz

    # Scale and return cosine and sine values
    return {"Sine": y, "Cosine": x}


#  ------------------------------------------
#  -------------------Main-------------------
#  ------------------------------------------

if __name__ == "__main__":
    # scale = 0x26DD3B6A
    # cordic_K = 0x100000000

    table = generate_atans()
    len_of_array = len(table)
    scale = SCALE()

    angle = pi / 6
    fixed_angle = angle * scale
    actual_sin = sin(angle)
    actual_cos = cos(angle)
    cordic_dict = CORDIC(fixed_angle, table, len_of_array)

    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("Angle:", angle)
    print("Actual Sin:", actual_sin)
    print("CORDIC Sin:", cordic_dict["Sine"] / scale)
    print("Actual Cos:", actual_cos)
    print("CORDIC Cos:", cordic_dict["Cosine"] / scale)
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    Scaled_K = int(K_value(32) * SCALE())
    print("Arctangent table in int: ", generate_atans())
    print("Arctangent table in hex: ", hexadecimate_array(generate_atans()))
    print("Hex value of K constant: ", hex(convert_to_int(K_value(32))))
    print("Scale K constant: ", Scaled_K, " == ", hex(Scaled_K))
    print("Scale: ", SCALE())
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
