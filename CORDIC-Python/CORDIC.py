# Python implementation for cordic algorithm

def CORDIC(theta, N):
    x = 0               # Wartość początkowa sinus
    y = 0x9B        # Wartość początkowa cosinus  / /  155
    angle = theta       # Kąt

    acan_table = [61, 45, 24, 12, 6, 3, 2, 1]
    # acan_table = [0x3FDFFFFFFF993, 0x3FDFFFFFE36F, 0x3FDFFFFF1C76,
    #               0x3FDFFFFDDEDD, 0x3FDFFFFA26C4, 0x3FDFFFF40F3B,
    #               0x3FDFFFE03823, 0x3FDFFFBBBD2E]

    for i in range(N):
        if angle < 0:
            new_x = x + (y >> i)       # Przesuwamy o i miejsc bitowych w prawo
            new_y = y - (x >> i)
            angle += acan_table[i % len(acan_table)]
        else:
            new_x = x - (y >> i)
            new_y = y + (x >> i)
            angle -= acan_table[i % len(acan_table)]

        x, y = new_x, new_y

    return x, y


# Decide precision level
N = 15
# Input angle
theta = 50
cordic = CORDIC(theta, N)
print(f"Sin({theta}): {cordic[0]}, Cos({theta}): {cordic[1]}")
