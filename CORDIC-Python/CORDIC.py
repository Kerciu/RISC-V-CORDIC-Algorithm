# Python implementation for cordic algorithm
from math import atan, sin, cos, pi, sqrt


def generate_atans():
    atan_scale = 0x40000000
    array = []
    for i in range(20):
        array.append(int(atan(2 ** - i) * atan_scale))

    return array


def hexadecimate_array(array):
    for idx, elem in enumerate(array):
        array[idx] = hex(elem)
    return array


def K_value(iterations):
    K = 1.0
    for i in range(0, iterations):
        K = K * (1.0 / sqrt(1 + 2.0 ** (-2 * i)))
    return K


def CORDIC(theta_deg, iterations):
    xy_point = (1, 0)
    K = K_value(iterations)

    for i in range(0, iterations):

        d = 1.0
        if theta_deg < 0:
            d = -1.0

        x, y = xy_point[0], xy_point[1]

        xy_point = (x - (d * (2.0 ** (-i))) * y, y + (d * (2.0 ** (-i))))
        theta_deg = theta_deg - (d * atan(2 ** (-i)))

    return K * xy_point[0], K * xy_point[1]


if __name__ == "__main__":
    scale = 0x26DD3B6A
    table = generate_atans()
    len_of_array = len(table)
    cordic_K = 0x100000000

    angle = pi / 2
    actual_sin = sin(angle)
    actual_cos = cos(angle)
    cordic_cos, cordic_sin = CORDIC(angle, len_of_array)

    print("Angle:", angle)
    print("Actual Sin:", actual_sin)
    print("CORDIC Sin:", cordic_sin)
    print("Actual Cos:", actual_cos)
    print("CORDIC Cos:", cordic_cos)
