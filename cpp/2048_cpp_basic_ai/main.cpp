#include <iostream>
#include <iomanip>
#include <time.h>
#include <cstdlib>
#include <unistd.h>

using namespace std;

// Display the board
void print_board(int board[])
{
  cout << "-----------------------" << endl;
  for(int i = 0; i < 4; i++) {
    for(int j = 0; j < 4; j++) {
      cout << setw(5) << board[i*4+j] << " ";
    }
    cout << endl;
  }
  cout << "-----------------------" << endl;
  return;
}

// Spawn a 2 or 4 ontu an empty tile
void spawn(int board[])
{
  int index = (rand() % 4) * 4 + rand() % 4;
  int value = rand() % 8;
  if (value > 0) {
    value = 2;
  } else {
    value = 4;
  }
  while (board[index]) {
    index = (index + 1) % 16;
  }
  board[index] = value;
  return;
}

int shift(int row[])
{
  int score = 0;
  // Do this for each item
  // Take the first item to the right that isn't zero
  // If they are equal, double the first item, and make the right item 0
  // Of course switch this for right, left, up, down
  int x;
  int y;

  for(int x = 0; x < 4; x++) {
    y = x + 1;
    while (!row[y]) {
      y += 1;
    }
  // y = index of first non-zero
    if (row[x] == row[y]) {
      row[x] *= 2;
      row[y] = 0;
      score += row[x];
    }
  }
  // This code right here sucks
  for(int x = 0; x < 4; x++) {
    if (!row[x]) {
      for(int y = x; y < 4-1; y++) {
        row[y] = row[y+1];
        row[y+1] = 0;
      }
    }
  }
  for(int x = 0; x < 4; x++) {
    if (!row[x]) {
      for(int y = x; y < 4-1; y++) {
        row[y] = row[y+1];
        row[y+1] = 0;
      }
    }
  }


  return score;
}

int left(int board[])
{
  int score = 0;
  for (int x = 0; x < 16; x += 4) {
    int row[4] = {board[x], board[x+1], board[x+2], board[x+3]};
    score += shift(row);
    for (int i = 0; i < 4; i++) {
      board[x+i] = row[i];
    }
  }
  return score;
}
  

int right(int board[])
{
  int score = 0;
  for (int x = 0; x < 16; x += 4) {
    int row[4] = {board[x+3], board[x+2], board[x+1], board[x]};
    score += shift(row);
    for (int i = 0; i < 4; i++) {
      board[x+i] = row[3-i];
    }
  }
  return score;
}

int up(int board[])
{
  int score = 0;
  for (int x = 0; x < 4; x++) {
    int row[4] = {board[x], board[4+x], board[8+x], board[12+x]};
    score += shift(row);
    for (int i = 0; i < 4; i++) {
      board[4*i+x] = row[i];
    }
  }
  return score;
}

int down(int board[])
{
  int score = 0;
  for (int x = 0; x < 4; x++) {
    int row[4] = {board[12+x], board[8+x], board[4+x], board[x]};
    score += shift(row);
    for (int i = 0; i < 4; i++) {
      board[4*i+x] = row[3-i];
    }
  }
  return score;
}

void copy_board(int new_board[], int board[])
{
  for(int i = 0; i < 16; i++) {
    new_board[i] = board[i];
  }
  return;
}

void init_board(int board[])
{
  for(int i = 0; i < 4; i++) {
    for(int j = 0; j < 4; j++) {
      board[i*4+j] = 0;
    }
  }
}

bool equal(int board1[], int board2[])
{
  for(int i = 0; i < 16; i++) {
    if (board1[i] != board2[i]) {
      return false;
    }
  }
  return true;
}

bool game_over(int board[])
{
  bool result = true;
  for (int i = 0; i < 16; i++) {
    if (!board[i]) {
      return false;
    }
  }
  for (int i = 1; i < 15; i++) {
    // If not on left edge
    if ((i%4) != 0) {
      if (board[i] == board[i-1]) {
        return false;
      }
    }
    // If not on right edge
    if (((i+1)%4) != 0) {
      if (board[i] == board[i+1]) {
        return false;
      }
    }
    // If not on top edge
    if (i > 3) {
      if (board[i] == board[i-4]) {
        return false;
      }
    }
    // If not on bottem edge
    if (i < 12) {
      if (board[i] == board[i+4]) {
        return false;
      }
    }
  }
  return true;
}


// Performs moves in this priority: right, up, down, left
int one_game_1()
{
  int board[16];
  init_board(board);
  spawn(board);
  spawn(board);
  int old_board[16];
  copy_board(old_board, board);
  int score = 0;
  while (1) {
    print_board(board);
    score += right(board);
    if (equal(old_board, board)) {
        score += up(board);
    }
    if (equal(old_board, board)) {
        score += down(board);
    }
    if (equal(old_board, board)) {
        score += left(board);
    }
    if (equal(old_board, board)) {
      return score;
    }
    spawn(board);
    copy_board(old_board, board);
  }
}

// Performs moves in priority right, up, down, left, but if it hits a "bad"
// move, it immediatly reverse the direction
int one_game_2()
{
  int board[16];
  init_board(board);
  spawn(board);
  spawn(board);
  int old_board[16];
  copy_board(old_board, board);
  int score = 0;
  bool no_change = false;
  while (1) {
    no_change = false;
    score += right(board);
    no_change = equal(old_board, board);
    if (no_change) {
      score += up(board);
      no_change = equal(old_board, board);
    }
    if (no_change) {
      score += down(board);
      no_change = equal(old_board, board);
      score += up(board);
    }
    if (no_change) {
      score += left(board);
      no_change = equal(old_board, board);
      score += right(board);
    }
    if (no_change) {
      return score;
    }
    spawn(board);
    copy_board(old_board, board);
  }
}

// Alternating up, right, with priority added at the end
int one_game_3()
{
  int board[16];
  init_board(board);
  spawn(board);
  spawn(board);
  int old_board[16];
  copy_board(old_board, board);
  int score = 0;

  bool no_change;
  while (1) {
    no_change = false;
    score += right(board);
    score += up(board);
    no_change = equal(old_board, board);
    if (no_change) {
      score += up(board);
      no_change = equal(old_board, board);
    }
    if (no_change) {
      score += down(board);
      no_change = equal(old_board, board);
      score += up(board);
    }
    if (no_change) {
      score += left(board);
      no_change = equal(old_board, board);
      score += right(board);
    }
    if (no_change) {
      return score;
    }
    spawn(board);
    copy_board(old_board, board);
  }
}

int one_game_best_move()
{
  int board[16];
  init_board(board);
  spawn(board);
  spawn(board);
  int old_board[16];
  copy_board(old_board, board);
  int new_board[16];
  copy_board(new_board, board);
  int score = 0;
  int best_move;
  int score_increase;

  while (1) {
    print_board(board);
    best_move = 1;
    score_increase = right(new_board);
    copy_board(new_board, board);
    if (score_increase < up(new_board)) {
      copy_board(new_board, board);
      score_increase = up(new_board);
      best_move = 2;
    }
    if (score_increase < down(new_board)) {
      copy_board(new_board, board);
      score_increase = down(new_board);
      best_move = 3;
    }
    if (score_increase < left(new_board)) {
      copy_board(new_board, board);
      score_increase = left(new_board);
      best_move = 4;
    }
    copy_board(new_board, board);
    // Perform move
    if (best_move == 1) {
      score += right(board);
    } else if (best_move == 2) {
      score += up(board);
    } else if (best_move == 3) {
      score += down(board);
    } else if (best_move == 4) {
      score += left(board);
    }
    if (equal(new_board, board)) {
      return score;
    }
  }
}

// To Add:
// Random Moves
// Recursive search tree
// Neural network
// Add game over function to other ai

// Test the ai with a specific mode
float test_ai(int mode, int iterations) {
  int total = 0; 
  float average = 0.0;
  for (int i = 0; i < iterations; i++) {
    if (mode == 1) { 
      total += one_game_1();
    } else if (mode == 2) {
      total += one_game_2();
    } else if (mode == 3) {
      total += one_game_3();
    } else {
      total += 0;
    }
  }
  return total / (float) iterations;
}


int main()
{
  int mode = 1;
  // MAIN GAME
  if (mode == 0) {
    int board[16];
    init_board(board);
    spawn(board);
    spawn(board);
    char input = ' ';
    int score = 0;
    cout << "Use wasd to shift board, and q to quit" << endl;
    cout << "Press any key to start" << endl;
    while (!game_over(board)) {
      print_board(board);
      cout << "Score: " << score << endl;
      cin >> input;
      switch (input) {
        case 'w':
          score += up(board);
          break;
        case 'a':
          score += left(board);
          break;
        case 's':
          score += down(board);
          break;
        case 'd':
          score += right(board);
          break;
        default:
          cout << "Invalid key" << endl;
      }
      spawn(board);
    }
  }

  // Without correction = 2023
  // With correction = 1417
  // With alternating = 1821
  // AI GAME
  //cout << test_ai(1, 1000) << endl;
  //cout << one_game_best_move() << endl;
  one_game_1();

  return 0;
}
