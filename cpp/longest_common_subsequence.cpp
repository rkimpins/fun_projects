/*
 * This is an implementation of an algorithmn discussed in class
 * for solving the longest common subsequence problem using
 * bottem up dynamic programming
 * Author : Randal Kimpinski
 * Date : March 18, 2019
 */

#include <iostream>
using namespace std;

int main() {
  // Set strings to be computed
  string s1 = "abdklsdfac";
  string s2 = "asekjhvsaddsf";
  // Initialize dynamic matrix
  int n1 = s1.length();
  int n2 = s2.length();
  int M[n1][n2] = {{0}};

  // Set 0's
  for (int i = 0; i < n1; i++) {
    M[i][0] = 0;
  }
  // Set 0's
  for (int j = 0; j < n2; j++) {
    M[0][j] = 0;
  }
  // Algorithmn for dynamic stuff
  for (int i = 0; i < n1; i++) {
    for (int j = 0; j < n2; j++) {
      if (s1[i] == s2[j]) {
        M[i][j] = M[i-1][j-1] + 1;
      } else {
        M[i][j] = max(M[i-1][j], M[i][j-1]);
      }
    }
  }


  // Print the resulting array
  for (int i = 0; i < n1; i++) {
    for (int j = 0; j < n2; j++) {
      cout << M[i][j] << " ";
    }
    cout << endl;
  }

  return 0;
}

