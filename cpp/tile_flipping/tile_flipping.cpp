#include <iostream>
#include <math.h>
#include <queue>
#include <vector>
#include <stack>
#include <bitset>
#include <ios>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <chrono>
#include <time.h>
#include <bitset>
#include <boost/dynamic_bitset.hpp>
using namespace std;
using namespace boost;
struct Dim {
  int x;
  int y;
};

class File_Array {
  public:
    string file_name;
    unsigned long long int file_size;
    fstream file;
  File_Array(string name, unsigned long long int size) {
    file_name = name;
    file_size = size;
    file.open(file_name, ios::in | ios::out);
    if (!file) {
      file.open(name, ios::out);
      file.close();
      file.open(name, ios::in | ios::out);
    } else {
      reset(1024);
    }
  }
  ~File_Array() {
    file.close();
  }
  void reset(unsigned int block_size) {
    file.seekp(0);
    char temp[block_size] = {0};
    for (unsigned long long int i = 0; i < file_size; i += block_size) {
      file.write(temp, block_size);
    }
  }
  bool get(unsigned long long int index) {
    if (index < 0 or file_size <= index) {
      throw invalid_argument("Index not in range");
    }
    file.seekg(index);
    char temp = 0;
    file.read(&temp, 1);
    return temp;
  }
  void set(unsigned long long int index, bool val) {
    if (index < 0 or file_size <= index) {
      throw invalid_argument("Index not in range");
    }
    char x = (char) val;
    file.seekp(index);
    file.write(&x, 1);
    return;
  }
};

template <typename T>
void print_board(int dim, T board) {
  int its = dim*dim;
  int *bits = new int[its];
  // Init to 0
  for (int i = 0; i < its; i++) {
    bits[i] = 0;
  }
  // Assign 1's properly
  for (int i = its-1; i >= 0; i--) {
    bits[i] = board % 2;
    board /= 2;
  }
  // Print out
  for (int i = 0; i < its; i++) {
    if (i % dim == 0) {
      cout << endl;
    }
    cout << bits[i];
  }
  cout << endl;
  delete[] bits;
}
template <typename T>
void print_board_2(Dim dim, T board) {
  int its = dim.x*dim.y;
  int *bits = new int[its];
  // Init to 0
  for (int i = 0; i < its; i++) {
    bits[i] = 0;
  }
  // Assign 1's properly
  for (int i = its-1; i >= 0; i--) {
    bits[i] = board % 2;
    board /= 2;
  }
  // Print out
  for (int i = 0; i < its; i++) {
    if (i % dim.x == 0) {
      cout << endl;
    }
    cout << bits[i];
  }
  cout << endl;
  delete[] bits;
}


template <typename T>
int* bit_to_list(int dim, T board) {
  int its = dim * dim;
  int *bits = new int[its];
  for (int i = 0; i < its; i++) {
    bits[i] = 0;
  }
  for (int i = its-1; i >= 0; i--) {
    bits[i] = board % 2;
    board /= 2;
  }
  return bits;
}

template <typename T>
T list_to_bit(int dim, T* bits) {
  //cout << "list_to_bit";
  T board = 0;
  int power = 1;
  int its = dim * dim;
  for (int i = its-1; i >= 0; i--) {
    board += bits[i] * power;
    power *= 2;
  }
  return board;
}

template <typename T>
T flip_tile(int x, int y, int dim, T board) {
  // Flip a single tile on our board, not including the adjacent ones
  if (x < 0 or y < 0 or x >= dim or y >= dim) {
    return board;
  } else {
    int *bits = bit_to_list(dim, board);
    int bit = bits[x + dim*y];
    if (bit) {
      bits[x + dim*y] = 0;
    } else {
      bits[x + dim*y] = 1;
    }
    T result = list_to_bit(dim, bits);
    delete[] bits;
    return result;
  }
}

//TODO use xor masks to more efficiently flip these
template <typename T>
T flip_tile_set(int x, int y, int dim, T board) {
  board = flip_tile(x, y, dim, board);
  board = flip_tile(x+1, y, dim, board);
  board = flip_tile(x-1, y, dim, board);
  board = flip_tile(x, y+1, dim, board);
  board = flip_tile(x, y-1, dim, board);
  return board;
}

template <typename T>
T flip_tile_2(int x, int y, Dim dim, T board) {
  // Flip a single tile on our board, not including the adjacent ones
  if (x < 0 or y < 0 or x >= dim.x or y >= dim.y) {
    return board;
  } else {
    //cout << x << " " << y << endl;
    //cout << (dim.x - x - 1) + (dim.y - y - 1)*dim.y << endl;
    dynamic_bitset<> temp {dim.x * dim.y, board};
    temp.flip((dim.x - x - 1)+ (dim.y - y - 1)*dim.x);
    return temp.to_ulong();
  }
}

template <typename T>
T flip_tile_set_2(int x, int y, Dim dim, T board) {
  board = flip_tile_2(x, y, dim, board);
  board = flip_tile_2(x+1, y, dim, board);
  board = flip_tile_2(x-1, y, dim, board);
  board = flip_tile_2(x, y+1, dim, board);
  board = flip_tile_2(x, y-1, dim, board);
  return board;
}

template <typename T>
vector<T> solve(unsigned int dim, T board) {
    bool *seen = new bool[(int) pow(2, dim*dim)];
    queue<vector<T>> frontier;
    vector<T> path; path.push_back(board);
    frontier.push(path);
    while (!frontier.empty()) {
      //cout << frontier.size() << endl;
      path = frontier.front();
      frontier.pop();
      print_board(dim, path.back());
      T board = path.back();
      if (board == 0) {
        cout << "Solvable" << endl;
        delete[] seen;
        return path;
      }
      //if board in solvable:
      //    return True, path, seen
      //if board in unsolvable:
      //    return False, None, seen
      for (unsigned int i = 0; i < dim; i++) {
        for (unsigned int j = 0; j < dim; j++) {
          //T newBoard = flip_tile_set(i, j, dim, board);
          vector<T> newPath; newPath = path;
          T newBoard = flip_tile_set(i, j, dim, newPath.back());
          newPath.push_back(newBoard);

          if (!seen[newBoard]) {
            frontier.push(newPath);
            seen[newBoard] = 1;
          }
        }
      }
    }

    cout << "Unsolvable" << endl;
    //for (int i = 0; i < pow(2,dim*dim); i++) {
    //  cout << seen[i];
    //}
    //cout << endl;
    delete[] seen;
    return path;
}

void all_solvable_path(int dim) {
  typedef unsigned int T;
  bool *solvable = new bool[(int) pow(2, dim*dim)];
  bool *unsolvable = new bool[(int) pow(2, dim*dim)];
  //bool *unsolved_boards = new bool[(int) pow(2, dim*dim)];
  //bool *solved_boards = new bool[(int) pow(2, dim*dim)];
  T max = (T) pow(2, dim*dim);
  for (T board = 0; board < max; board++) {
    bool *seen = new bool[(int) pow(2, dim*dim)];
    queue<vector<T>> frontier;
    vector<T> path; path.push_back(board);
    seen[board] = 1;
    frontier.push(path);
    while (!frontier.empty()) {
      path = frontier.front();
      frontier.pop();
      //print_board(dim, path.back());
      T board = path.back();
      if (board == 0) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            solvable[i] = 1;
          }
        }
        break;
      }
      if (solvable[board]) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            solvable[i] = 1;
          }
        }
        solvable[board] = 1;
        break;
      }
      if (unsolvable[board]) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            unsolvable[i] = 1;
          }
        }
        unsolvable[board] = 1;
        break;
      }
      for (T i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
          //T newBoard = flip_tile_set(i, j, dim, board);
          vector<T> newPath; newPath = path;
          T newBoard = flip_tile_set(i, j, dim, newPath.back());
          newPath.push_back(newBoard);
          if (!seen[newBoard]) {
            frontier.push(newPath);
            seen[newBoard] = 1;
          }
        }
      }
    }
  }
  int num_solvable = 0;
  int num_unsolvable = 0;
  /*
  cout << "Solvable" << endl;
  for (T i = 0; i < max; i++) {
    if (solvable[i]) {
      print_board(dim, i);
    }
  }
  cout << "Unsolvable" << endl;
  for (T i = 0; i < max; i++) {
    if (unsolvable[i]) {
      print_board(dim, i);
    }
  }
  */
  for (T i = 0; i < max; i++) {
    num_solvable += solvable[i];
    num_unsolvable += unsolvable[i];
  }
  cout << "Solvable: " << num_solvable << " Unsolvable: " << num_unsolvable << endl;
  delete[] solvable;
  delete[] unsolvable;
  return;
}

void all_solvable(int dim) {
  typedef unsigned long long T;
  bool *solvable = new bool[(int) pow(2, dim*dim)];
  bool *unsolvable = new bool[(int) pow(2, dim*dim)];
  //bool *unsolved_boards = new bool[(int) pow(2, dim*dim)];
  //bool *solved_boards = new bool[(int) pow(2, dim*dim)];
  T max = (T) pow(2, dim*dim);
  T board;
  T visited = 0;
  for (T iter = 0; iter < max; iter++) {
    queue<T> frontier;
    //seen[iter] = 1;
    frontier.push(iter);
    bool *seen = new bool[(int) pow(2, dim*dim)]();
    seen[iter] = 1;
    while (!frontier.empty()) {
      // TODO reorganize this, check everything before adding to queue
      visited++;
      if(visited % 1000000 == 0) { cout << visited << endl; }
      //
      board = frontier.front();
      frontier.pop();
      if (board == 0) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            solvable[i] = 1;
          }
        }
        break;
      }
      if (solvable[board]) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            solvable[i] = 1;
          }
        }
        //solvable[board] = 1;
        break;
      }
      if (unsolvable[board]) {
        for (T i = 0; i < max; i++) {
          if (seen[i]) {
            unsolvable[i] = 1;
          }
        }
        //unsolvable[board] = 1;
        break;
      }
      for (T i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
          T newBoard = flip_tile_set(i, j, dim, board);
          if (!seen[newBoard]) {
            frontier.push(newBoard);
            seen[newBoard] = 1;
          }
        }
      }
    }
    if (frontier.empty() and board != 0 and !solvable[board]) {
      for (T i = 0; i < max; i++) {
        if (seen[i]) {
          unsolvable[i] = 1;
        }
      }
    }

  delete[] seen;
  }
  int num_solvable = 0;
  int num_unsolvable = 0;
  /*
  cout << "Solvable" << endl;
  for (T i = 0; i < max; i++) {
    if (solvable[i]) {
      print_board(dim, i);
    }
  }
  cout << "Unsolvable" << endl;
  for (T i = 0; i < max; i++) {
    if (unsolvable[i]) {
      print_board(dim, i);
    }
  }
  */
  for (T i = 0; i < max; i++) {
    num_solvable += solvable[i];
    num_unsolvable += unsolvable[i];
  }
  cout << "Solvable: " << num_solvable << " Unsolvable: " << num_unsolvable << endl;
  delete[] solvable;
  delete[] unsolvable;
  return;
}

void dfs_fa_all_solvable(int dim, string name) {
  typedef unsigned long long int T;
  T max = (T) pow(2, dim*dim);
  File_Array visited("4_by_4_result.bin", pow(2, dim*dim));
  stack<T> frontier;
  frontier.push(0);
  //visited[0] = 1;
  visited.set(0, 1);
  int counter = 0;
  while(!frontier.empty()){
    counter++;
    if (counter % 100000 == 0) {
      cout << ((double) counter / (double) max) << endl;
      cout << counter << "/" << max << endl;
    }
    T board = frontier.top();
    //print_board(dim, board);
    frontier.pop();
    for (T i = 0; i < dim; i++) {
      for (int j = 0; j < dim; j++) {
          //T newBoard = flip_tile_set(i, j, dim, board);
        T newBoard = flip_tile_set(i, j, dim, board);
        if (!visited.get(newBoard)) {
          frontier.push(newBoard);
          visited.set(newBoard, 1);
        }
      }
    }
  }
  int num_solvable = 0;
  for (T i = 0; i < max; i++) {
    num_solvable += visited.get(i);
    //cout << visited[i];
  }
  //cout << endl;
  cout << "Solvable: " << num_solvable << " Unsolvable: " << max - num_solvable <<  endl;
  //delete[] visited;
  return;
}
void dfs_all_solvable(Dim dim, bool progress, bool verbose) {
  typedef unsigned long long int T;
  T max = (T) pow(2, dim.x*dim.y);
  bool *visited = new bool[(int) pow(2, dim.x*dim.y)];
  stack<T> frontier;
  frontier.push(0);
  visited[0] = 1;
  int counter = 0;
  while(!frontier.empty()){
    if (progress) {
      counter++;
      if (counter % (max / 100) == 0) {
        cout << ((double) counter / (double) max) << endl;
        cout << counter << "/" << max << endl;
      }
    }
    T board = frontier.top();
    //print_board(dim, board);
    frontier.pop();
    for (int i = 0; i < dim.x; i++) {
      for (int j = 0; j < dim.y; j++) {
        //T newBoard = flip_tile_set(i, j, dim, board);
        T newBoard = flip_tile_set_2(i, j, dim, board);
        if (!visited[newBoard]) {
          frontier.push(newBoard);
          visited[newBoard] =  1;
        }
      }
    }
  }
  int num_solvable = 0;
  for (T i = 0; i < max; i++) {
    num_solvable += visited[i];
    if (visited[i] and verbose) {
      print_board_2(dim, i);
    }

    //cout << visited[i];
  }
  //cout << endl;
  cout << "Solvable: " << num_solvable << " Unsolvable: " << max - num_solvable <<  endl;
  delete[] visited;
  return;
}
// rand only has 30-31 decimal places, only use for 5x5, not 6x6
void random_solve(int dim) {
  typedef unsigned long long int T;
  T max = (T) pow(2, dim*dim);
  srand(time(NULL));

  T board = rand() % max;
  print_board(dim, board);
  unsigned long long int steps = 0;
  while (board != 0) {
    board = flip_tile_set(rand()%dim, rand()%dim, dim, board);
    //print_board(dim, board);
    steps++;
  }
  cout << "Takes " << steps << " steps to solve the puzzle" << endl;
  return;
}
void time_random_solve(int dim, int trials) {
  typedef unsigned long long int T;
  srand(time(NULL));
  auto start = chrono::high_resolution_clock::now();
  unsigned long long int ave_steps = 0;
  for (int i = 0; i < trials; i++) {
    T max = (T) pow(2, dim*dim);
    T board = rand() % max;
    unsigned long long int steps = 0;
    while (board != 0) {
      board = flip_tile_set(rand()%dim, rand()%dim, dim, board);
      steps++;
    }
    ave_steps += steps;
  }
  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
  cout << "Average time (microseconds): " << duration.count() / trials << endl; 
  cout << "Average steps: " << ave_steps / trials << endl;
  return;
}

/*
 * 2x2 Solvable: 16 Unsolvable: 0 =  1
 * 3x3 Solvable: 512 Unsolvable: 0 = 1
   * Average time (microseconds): 118
   * Average steps: 599
 * 4x4 Solvable: 4096 Unsolvable: 61440 =  0.06666666667
 * 5x5: Solvable: 8388608 Unsolvable: 25165824 = 0.33333333333
 */

int main(int argc, char *argv) {
  // -a = solve all
  // next arg is dimension, either (4, 5) or (4). 2 numbers = differnet
  // dimensions

  cout << "Simple Tile Flipping Solver" << endl;
  //Dim dim;
  //dim.x = 2;
  //dim.y = 4;
  //dfs_all_solvable(dim, false, true);
  //return 0;
  //TODO
  //Make input for custom board make sense
  //Make all of this more modular with classes and whatnot
  //Make functions work with different dimension
  //Implement this as an arbitrary graph, then make a conversion tool from grid
  //N dimensional tile flipping

  int mode = 0;
  while (true) {
    cout << "[1] Solve all boards\n[2] Check if a specific board is solvable\nPick a mode:";
    cin >> mode;
    if (mode == 1 or mode == 2) {
      break;
    }
  }
  if (mode == 1) {
    cout << "What dimension do you want to solve (x y):";
    Dim dim;
    cin >> dim.x;
    cin >> dim.y;
    cout << endl;
    cout << "Would you like to view all the solvable boards (0=no, 1=yes):";
    bool verbose;
    cin >> verbose;
    cout << "Would you like an approximate progress bar (0=no, 1=yes):";
    bool progress;
    cin >> progress;
    dfs_all_solvable(dim, progress, verbose);
  } else if (mode == 2) {
    cout << "What dimension do you want to solve (x y):";
    Dim dim;
    cin >> dim.x;
    cin >> dim.y;
    cout << "Input your board as an integer" << endl;
    int board;
    cin >> board;
    solve(dim.x, board);
    //cout << "Input your board as\n1101\n0001\n0000\nfor a 4 by 3 example" << endl;
  }

  //dynamic_bitset<> board{dim*dim, 32};
  //board.flip(15);
  //cout << board << endl;
  //b_print_board(dim, board);
  //board = b_flip_tile(x, y, dim, board);
  //b_print_board(dim, board);
  //bitset<dim*dim> board(string("1000110011101111"));
  //print_board(dim, board.to_ulong());
  //print_board_bits(dim, board.to_ulong());

  //unsigned int dim = 6;
  //dfs_fa_all_solvable(dim, "7_by_7_result.bin");

  //string name = "5_by_5_result.bin";
  //string name = "4_by_4_result.bin";
  //random_solve(dim);
  //time_random_solve(dim, 1);
  //auto start = chrono::high_resolution_clock::now();
  //dfs_all_solvable(dim);
  //auto stop = chrono::high_resolution_clock::now();
  //auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
  //cout << duration.count() << " microseconds" << endl; 

  return 0;
}

