/*
 * This program uses back tracking to solve a sodoku puzzle
 * inputed from a file
 */
#include <iostream>
#include <set>
using namespace std;

// Print the sodoku puzzle
void print(int M[]) {
  int i = 0;
  while (i < 81) {
    cout << M[i] << " ";
    i++;
    if (i%9 == 0) {
      cout << endl;
    }
  }
  return;
}
// Return true if the puzzle is invalid and not worth continuing
// So we check all the columns, the rows, and the boxes
bool reject(int M[]) {
  int debug = 0;
  int val;
  set<int> x;
  // Check rows
  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < 9; j++) {
      val = M[i*9+j];
      if (debug) {
        cout << val << " ";
      }
      if (val && x.find(val)!=x.end()) {
        if (debug) {
          cout << "Invalid puzzle";
        }
        return true;
      }
      x.insert(val);
    }
    x.clear();
    if (debug) {
      cout << endl;
    }
  }
  // Check columns
  for (int j = 0; j < 9; j++) {
    for (int i = 0; i < 9; i++) {
      val = M[i*9+j];
      if (debug) {
        cout << val << " ";
      }
      if (val && x.find(val)!=x.end()) {
        if (debug) {
          cout << "Invalid puzzle";
        }
        return true;
      }
      x.insert(val);
    }
    x.clear();
    if (debug) {
      cout << endl;
    }
  }
  // Check the boxes
  for (int k = 0; k < 3; k++) {
    for (int l = 0; l < 3; l++) {
      for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
          val = M[k*27+l*3+i*9+j];
          if (debug) {
            cout << val << " ";
          }
          if (val && x.find(val)!=x.end()) {
            if (debug) {
              cout << "Invalid puzzle";
            }
            return true;
          }
          x.insert(val);
        }
      }
      x.clear();
      if (debug) {
        cout << endl;
      }
    }
  }
  return false;
}

// Return true if the puzzle is valid and complete
bool accept(int M[]) {
  // If invalid, this is not a complete solution
  if (reject(M)) {
    return false;
  }
  // If any entry is 0, this is not a complete solution
  for (int i = 0; i < 81; i++) {
    if (M[i] == 0) {
      return false;
    }
  }
  return true;
}

// Generate the first extension of a canadite c (incrementing empty value)
// Genereate the next alternative extension of a candidate, after the extension

int main() {
  /* get input from file
  int M[81] = {0};
  for (int i = 0; i < 81; i++) {
    cin >> M[i];
  }
  */
  int M[] = {
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9 
  };
  int N[81] = {0};
  print(M);
  print(N);
  cout << "Reject: " << reject(M) << endl;
  return 0;
}
