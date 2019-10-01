/*
 * This program finds the optimal solution to the
 * 8 out of 10 cats does countdown numbergame.
 * In other words, given 6 numbers, 4 operations (+,-,*,/)
 * and a goal, finds the series of operations that will 
 * yeild the closest possible result
 * Notes: / only works when it yeilds a whole number
 * Not all numbers have to be used
 * This is represented with < and > symbols
 * Where a>b means that all the a value is not used (all previous)
 * and a<b meansthat the b value is not used
 */
#include <iostream>
#include <algorithm>
using namespace std;

/* 
 * Takes 2 ints, and an integer representing an opreation
 * And returns the result
 * 0 = +
 * 1 = -
 * 2 = *
 * 3 = /, only valid if we get a hole number
 * 4 = ignore b value
 * 5 = ignore a value
 */
int op(int a, int b, int op) {
  if (op == 0) {
    return a + b;
  } else if (op == 1) {
    return a - b;
  } else if (op == 2) {
    return a * b;
  } else if (op == 3 && a%b == 0) {
    return a / b;
  } else if (op == 4) {
    return a;
  } else if (op == 5) {
    return b;
  } else {
    return -1000000;
  }
}

// Simply prints our array
void print_array(int A[], int size) {
  for (int i = 0; i < size; i++) {
    cout << A[i];
  }
  cout << endl;
}

/*
 * Given an array of integers, increments as if we are in base 5
 * Returns true if we are able to increment, and false if we have overflow
 * I use this function to get all possible combinations of operations
 */
bool inc_ops(int Ops[]) {
  int base = 5;
  if (Ops[4] < base){
    Ops[4]++;
    return true;
  } else if (Ops[3] < base) {
    Ops[3]++;
    Ops[4] = 0;
    return true;
  } else if (Ops[2] < base) {
    Ops[2]++;
    Ops[3] = 0;
    Ops[4] = 0;
    return true;
  } else if (Ops[1] < base) {
    Ops[1]++;
    Ops[2] = 0;
    Ops[3] = 0;
    Ops[4] = 0;
    return true;
  } else if (Ops[0] < base) {
    Ops[0]++;
    Ops[1] = 0;
    Ops[2] = 0;
    Ops[3] = 0;
    Ops[4] = 0;
    return true;
  } else {
    return false;
  }
}

// Convert my representation for operations into symbosl
char to_symbol(int x) {
  if (x == 0) {
    return '+';
  } else if (x == 1) {
    return '-';
  } else if (x == 2) {
    return '*';
  } else if (x == 3) {
    return '/';
  } else if(x == 4) {
    return '<';
  } else {
    return '>';
  }
}

// Given the numbers and operations array, print the operations
// including < and > symbols
void print_calculation1(int N[], int Ops[]) {
  for (int i = 0; i < 5; i++) {
    cout << N[i];
    cout << to_symbol(Ops[i]);
  }
  cout << N[5];
  cout << '=' << endl;
}

// Given the numbers and operations array, print the operations
void print_calculation(int N[], int Ops[]) {
  int first = 0;
  for (int i = 0; i < 5; i++) {
    if (Ops[i] == 5) {
      first = i+1;
    }
  }
  cout << N[first];
  for (int i = first+1; i < 6; i++) {
    if (Ops[i-1] != 4) {
      cout << to_symbol(Ops[i-1]);
      cout << N[i];
    }
  }
  cout << '=';
}

// Return the absolute difference between two numbers
int distance(int x, int y) {
  if (x-y > 0) {
    return x - y;
  } else {
    return y - x;
  }
}

// Save our numbers and operations into seperate arrays
void save(int N[], int Ops[], int Sn[], int Sops[]) {
  for (int i = 0; i < 5; i++) {
    Sn[i] = N[i];
    Sops[i] = Ops[i];
  }
  Sn[5] = N[5];
}

// Given an array of numbers and an array of operations
// return the value when applied in order
int calculate_value(int N[], int Ops[]) {
  return op(op(op(op(op(N[0],N[1],Ops[0]),N[2],Ops[1]),N[3],Ops[2]),N[4],Ops[3]),N[5],Ops[4]);
}

int main()
{
  int goal;
  int N[6];
  cout << "Target: ";
  cin >> goal;
  cout << "6 values: ";
  for (int i = 0; i < 6; i++){
    cin >> N[i];
  }
  cout << "Print all results?: [0,1]";
  bool show;
  cin >> show;

  /*
  for manually checking
  bool show = 1;
  int N[6] = { 50, 100, 7, 6, 1, 10 };
  int goal = 941;
  */

  int Sn[6];
  int Sops[5];
  int x;
  int closest = 1000000;
  int Ops[5] = { 0,0,0,0,0 }; 

  while (next_permutation(N, N+6)) {
    while (inc_ops(Ops)) {
      x = calculate_value(N, Ops);
      if (distance(x, goal) < distance(closest, goal)) {
        closest = x;
        save(N, Ops, Sn, Sops);
      }
      if (x > 0 && show) {
        print_calculation(N, Ops);
        cout << x << endl;
      }
    }
  }
  cout << "Closest: " << closest << endl;
  print_calculation(Sn, Sops);
  cout << closest << endl;

  return 0;
}
