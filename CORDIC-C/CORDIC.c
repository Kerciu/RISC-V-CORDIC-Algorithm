// ---------------------------------------------
// C implementation for cordic algorithm
// This program does not use floats nor doubles
// ---------------------------------------------
//          Made by Kacper Górski
// ---------------------------------------------
// The CORDIC algorithm is a numerical method for computing trigonometric functions.
// It uses a series of shifts and additions to approximate functions like sine and cosine.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// ------------------------------------------------------
// Pi constant
#define M_PI 3.14159265358979323846

// CORDIC K constant << 30 (scaled by 2^30)
#define K 0x26DD3B6A

// Scaling factor used for working on fixed-point integers
// 2^30
#define SCALE 1073741824.0
// ------------------------------------------------------

// ------------------------------------------------------
//                  CORDIC ALGORITHM
// ------------------------------------------------------
// Calculates sine and cosine using CORDIC algorithm
// Takes in:
//      - theta_deg: Angle in radians scaled by SCALE
//      - ACAN_TABLE: Precomputed arctanget table
//      - ACAN_SCALE: Size of arctangent table
// Returns:
//      An array containing the calculated sine and cosine
// ------------------------------------------------------

int* CORDIC(int theta_deg, int ACAN_TABLE[], int ACAN_SIZE) {
    int x_point = K;
    int y_point = 0;
    int z = theta_deg;
    int i;

    // CORDIC algorithm iteration
    for(i = 0; i < ACAN_SIZE; ++i) {
        int dx = y_point >> i;
        int dy = x_point >> i;
        int dz = ACAN_TABLE[i];

        if (z < 0) {
            x_point += dx;
            y_point -= dy;
            z += dz;
        }
        else {
            x_point -= dx;
            y_point += dy;
            z -= dz;
        }
    }

    // Allocate memory for the result
    int* result = (int*)malloc(2 * sizeof(int));
    if (result == NULL) {
        return NULL;
    }

    result[0] = x_point;
    result[1] = y_point;
    return result;
}
// ------------------------------------------------------

// ------------------------------------------------------
//                          main
// ------------------------------------------------------
int main() {
    // Precomputed arcus tangent table, each record multiplied by SCALE.
    // acan(2^-n) where n is <0, 31>
    int ACAN_TABLE[]  = {
        0x3243f6a8, 0x1dac6705, 0x0fadbafc, 0x07f56ea6, 0x03feab76,
        0x01ffd55b, 0x00fffaaa, 0x007fff55, 0x003fffea, 0x001ffffd,
        0x000fffff, 0x0007ffff, 0x0003ffff, 0x0001ffff, 0x0000ffff, 0x00007fff, 0x00003fff,
        0x00001fff, 0x00000fff, 0x000007ff, 0x000003ff, 0x000001ff, 0x000000ff, 0x0000007f, 0x0000003f, 0x0000001f,
        0x0000000f, 0x00000008, 0x00000004, 0x00000002, 0x00000001, 0x00000000,
    };

    // Precomputed size of arcus tangent table
    int ACAN_SIZE = 32;

    // Angle in radians
    double angle_deg = M_PI / 6.0;
    // Scaling the angle
    double scaled_angle = angle_deg * SCALE;

    // Evoke cordic function to calculate sine and cosine
    int* cordic_result = CORDIC(scaled_angle, ACAN_TABLE, ACAN_SIZE);

    if (cordic_result == NULL) {
        return -1;
    }

    // Visually compare real sine and cosine with cordic records
    double real_sine = sin(angle_deg);
    double real_cosine = cos(angle_deg);

    // Print result
    printf("Sine: %f\n", real_sine);
    printf("Sine computed by cordic: %f\n", cordic_result[1] / SCALE);
    printf("Cosine: %f\n", real_cosine);
    printf("Cosine computed by cordic: %f\n", cordic_result[0] / SCALE);

    // Free dynamically allocated memory
    free(cordic_result);
    return 0;
}
// ------------------------------------------------------
