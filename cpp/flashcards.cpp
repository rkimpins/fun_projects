/*
 * This program is to practice flash cards for powers of 2
 * By: Randal Kimpinski
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


int main(void) {
        int two[11][2] = {
                {0,1},
                {1,2},
                {2,4},
                {3,8},
                {4,16},
                {5,32},
                {6,64},
                {7,128},
                {8,256},
                {9,512},
                {10,1024}
        };
        float w[11] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
        float f_ran;
        int length = 11;
        int sum = 0;
        int ran1, ran2, ans;
        srand(time(NULL));
        while (1) {
                // Sum weights
                sum = 0;
                for(int i = 0; i < length; ++i) {
                        sum += w[i];
                }
                printf("Total sum:%d\n", sum);

                for (int i = 0; i < 11; ++i) {
                        printf("%d:%f\n", i, w[i]);
                }


                // Generate random in range of sum
                f_ran = fmod(rand(), sum);
                ran2 = rand()%2;
                printf("Random Number:%f\n", f_ran);

                // Find index using weighted distribution
                int i = 0;
                while (f_ran >= 0) {
                        f_ran -= w[i];
                        ++i;
                }
                ran1 = i - 1;
                printf("Random Index:%d\n", ran1);


                if (ran2 == 0) {
                        printf("2^%d:", two[ran1][ran2]);
                        scanf("%d", &ans);

                        if (ans == two[ran1][1]) {
                                printf("Correct\n");
                                w[ran1] /= 1.5;
                        } else {
                                printf("Incorrect\n");
                                printf("Answer: %d", two[ran1][1]);
                                w[ran1] *= 1.5;
                        }

                } else {
                        printf("log2 of %d:", two[ran1][ran2]);
                        scanf("%d", &ans);
                        
                        if (ans == two[ran1][0]) {
                                printf("Correct\n");
                                w[ran1] /= 1.5;
                        } else {
                                printf("Incorrect\n");
                                printf("Answer: %d", two[ran1][0]);
                                w[ran1] *= 1.5;
                        }
                }
        }
        return 0;
}
