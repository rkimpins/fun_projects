#include <iostream>
#include <math.h>
using namespace std;

// Given an array and its size, appends the inverse of its entries
// ie: 1001 --> 1001 0110
// Array must have atleast double the space of size
void append_inverse(int A[], int size) {
  for (int i = size; i < size * 2; i++) {
    A[i] = (A[i-size] == 0);
  }
  return;
}

// Generates the series up to iters
// Because of how it is generated (by inverting previous entries)
// always returns a series which is a power of 2 less than iters
void generate_series(int A[], int iters) {
  A[0] = 1;
  int i = 1;
  while (i < iters) {
    append_inverse(A,i);
    i*=2;
  }
  return;
}

// Simple print our array
void print_array(int A[], int size) {
  for (int i = 0; i < size; i++) {
    cout << A[i] << ",";
  }
  cout << endl;
}

// Call our methods
int main() {
  int N = 100;
  int *A = new int[N];
  generate_series(A, N/2);
  print_array(A,N);

  delete[] A;
  return 0;
}
