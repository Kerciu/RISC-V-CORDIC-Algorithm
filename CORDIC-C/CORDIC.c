#include <stdio.h>


void CORDIC(int ACAN_TABLE[], int acan_size, int theta_deg, int* result) {
    int K = 0x2431f1c7;
    int x_point = K;
    int y_point = 0;
    int z = theta_deg;

    for(int i = 0; i < acan_size; ++i) {
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

    result[0] = x_point;
    result[1] = y_point;
    }
}

int power_of(int degree) {
    for (int i = 0; i < degree; i++) {
        degree *= degree;
    }
    return degree;
}


int main() {

    int ACAN_TABLE[] = {0x3243f6a8, 0x1dac6705, 0xfadbafc, 0x7f56ea6,
        0x3feab76, 0x1ffd55b, 0xfffaaa, 0x7fff55, 0x3fffea, 0x1ffffd,
        0xfffff, 0x7ffff, 0x3ffff, 0x1ffff, 0xffff, 0x7fff, 0x3fff,
        0x1fff, 0xfff, 0x7ff, 0x3ff, 0x1ff, 0xff, 0x7f, 0x3f, 0x1f,
	    0xf, 0x8, 0x4, 0x2, 0x1, 0x0};
    int size = sizeof(ACAN_TABLE) / sizeof(ACAN_TABLE[0]);


    int cordic_result[2];
    float angle = (3141592653) / 3;
    CORDIC(ACAN_TABLE, size, angle, cordic_result);

    int sine = cordic_result[1];
    int cosine = cordic_result[0];

    printf("Sine: %d", sine, '\n');
    printf(" Cosine: %d", cosine);
    return 0;
}