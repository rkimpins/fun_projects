/*
 * Given a number, how many times can we multiply all of its
 * digits together before we arrive at a single digit number
 * ex: 279 --> 2*7*9 = 126 --> 1*2*6=12 --> 1*2 --> 2 --> DONE
 * Current Largest I have found is
 * MAX: 26888999 with 9 steps
 * 26888999 > 4478976 > 338688 > 27648 > 2688 > 768 > 336 > 54 > 20 > 0
 * Inspired by the Numberphile https://www.youtube.com/watch?v=Wim9WJeDTHQ
 * 277777788888899 is current record holder with 11 steps
 * Some potential efficiency increases
 * Ordering doesn't matter
 * 5*2=10 can never show up (except maybe last step)
 * 2*4 = 8, so we can replace any 2,4 with an 8
 * also 3*3
*/

#include <iostream>
using namespace std;

int multiply_digits(int x) {
  int result = 1;
  while (x) {
    result *= x % 10;
    x /= 10;
  }
  return result;
}

int num_steps_v(int x) {
  cout << "Val: " << x << endl;
  if (x < 10) {
    return 0;
  } else {
    return num_steps_v(multiply_digits(x)) + 1;
  }
}

int num_steps(int x) {
  if (x < 10) {
    return 0;
  } else {
    return num_steps(multiply_digits(x)) + 1;
  }
}

int main() {
  int max = 0;
  int temp_max;
  int max_val = 0;
  for (int i = 0; i < 100000000; i++) {
    temp_max = num_steps(i);
    if (temp_max > max) {
      max_val = i;
      max = temp_max;
    }
    cout << i << ":" << temp_max << endl;
  }
  cout << "MAX:";
  cout << max_val << ":" << max << endl;
  num_steps_v(max_val);
  
  return 0;
}

