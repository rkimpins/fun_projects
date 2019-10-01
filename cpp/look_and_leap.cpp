#include <cstdlib>
#include <iostream>
#include <ctime>
#include <algorithm>
using namespace std;

// Find vaue and index of max
int max(int *A, int N)
{
  int max = 0;
  for (int i = 0; i < N; i++) {
    if (A[i] > max) {
      max = A[i];
    }
  }
  return max;
}

// Look through 37% of numbers, then pick the next number that is bigger
int look_leap(int *A, int N)
{
  int max = 0;
  for (int i = 0; i < N; i++) {
    if ((i > N * 0.37) && A[i] > max) {
      return A[i];
    }
    if (A[i] > max) {
      max = A[i];
    }
  }
  return A[N-1];
}
  
// Return number of times we choose the max value
int gets_max(int *A, int N, int iterations)
{
  int result = 0;
  for (int i = 0; i < iterations; i++) {
    // Shuffle elements
    random_shuffle(&A[0], &A[N]);
    if (max(A, N) == look_leap(A, N)) {
      result++;
    }
  }
  return result;
}

// Return the average ratio of our chosen value compared to the max
float ratio(int *A, int N, int iterations)
{
  float result = 0;
  for (int i = 0; i < iterations; i++) {
    // Shuffle elements
    random_shuffle(&A[0], &A[N]);
    result += (look_leap(A, N) / (float) N);
  }
  return result / iterations;
}

int main()
{
  const int N = 1000;
  int its = 10000;
  int A[N];
  srand(time(0));
  // Assign values
  for (int i = 0; i < N; i ++) {
    A[i] = i;
  }
  // Some results
  cout << "Pop:   " << N << endl;
  cout << "Its:   " << its << endl;
  cout << "Maxs:  " << gets_max(A, N, its) << endl;
  cout << "Ratio: " << ratio(A, N, its) << endl;

  return 0;
}

