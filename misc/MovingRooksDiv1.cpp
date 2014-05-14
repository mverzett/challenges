/*Problem Statement
In this problem, some test cases have more than one correct output. We are using a special checker to verify that the output of your program is correct. 
This problem is about chessboards with rooks. A rook is a chess piece that moves arbitrarily far, either horizontally or vertically. Both rows and columns of chessboards in our problem are numbered starting from 0. 

An n times n chessboard is called peaceful if it contains exactly n rooks and no two rooks attack each other. In other words, there cannot be two rooks in the same row or in the same column of the chessboard. A peaceful chessboard can be described by a int[] Y with n elements: for each row r, the rook in row r is in column Y[r]. 

You are given two int[]s Y1 and Y2 with n elements each. Each of them represents one peaceful chessboard. 

You want to change the first chessboard into the second one. There is only one type of moves you are allowed to make: On the first chessboard, you can choose two rooks in positions (r1,c1) and (r2,c2) such that r1 < r2 and c1 > c2, and move them to (r1,c2) and (r2,c1). Note that the new chessboard is peaceful again. 

If changing the first chessboard into the second one is impossible, return a int[] with only one element, and that element should be -1. 

Otherwise, find any valid sequence of moves that changes the first board into the second board. Each move is uniquely defined by two integers: the rows with the rooks you want to move. If we write down the two rows for each move, we get a sequence of integers that encodes the solution. If that sequence has at most 2500 integers (i.e., encodes at most 1250 moves), return a int[] with the entire sequence. Otherwise, return a int[] with just the first 2500 integers of your sequence.
 
Definition
    	
Class:	MovingRooksDiv1
Method:	move
Parameters:	int[], int[]
Returns:	int[]
Method signature:	int[] move(int[] Y1, int[] Y2)
(be sure your method is public)
    
 
Notes
-	You are not required to find the solution that uses the smallest possible number of moves.
-	If your return value has 2500 integers, it will be accepted if and only if it is a valid solution or a proper prefix of some valid solution.
-	If your return value has fewer than 2500 integers, it will be accepted if and only if it's a valid solution (not a proper prefix).
 
Constraints
-	Y1 will contain between 1 and 2500 elements, inclusive.
-	Y2 will contain the same number of elements as Y1.
-	Each element of Y1 will be between 0 and n-1, inclusive, where n is the number of elements of Y1.
-	Each element of Y2 will be between 0 and n-1, inclusive, where n is the number of elements of Y2.
-	All elements of Y1 will be distinct.
-	All elements of Y2 will be distinct.
*/

#include <vector>
#include <queue>
#include <iterator>
#include <iostream>

typedef std::vector<int> vint;
typedef std::vector<int>::const_iterator vinter;

int min(vinter start, vinter stop){
  int min = *start;
  for(vinter i = start; i != stop; ++i){
    if(*i < min)
      min = *i;
  }
  return min;
}

int max(vinter start, vinter stop){
  int max = *start;
  for(vinter i = start; i != stop; ++i){
    if(*i > max)
      max = *i;
  }
  return max;
}

bool can_morph(vint test, vint target){
  unsigned int position=0;
  vinter begin = test.begin();
  vinter end   = test.end();
  for(vinter it = begin; it != end; ++it){
    if(min(it, end) > target[position] || target[position] > max(begin, it+1))
      return false;
    position++;
  }
  return true;
}

int ranking(vint test, vint target){
  unsigned int position=0;
  int rank = 0;
  for(vinter it = test.begin(); it != test.end(); ++it){
    if(*it == target[position])
      rank++;
    position++;
  }
  return rank;
}

vint swap(vint l1, int r1, int r2){
  bool isAllowed = (r1 < r2 && l1[r1] > l1[r2]);
  if( !isAllowed ){
    return vint();
  }
  vint ret = l1; //check that it copies and not references!
  int tmp = l1[r1];
  ret[r1] = ret[r2];
  ret[r2] = tmp;
  return ret;
}

/* TO BE TRANSLATED IN C++
t1 = [1,0]
t2 = [0,1]
assert(can_morph(t1, t2) == True)
assert(ranking(t1, t2)   == 0)

t1 = [3,1,2,0]
t2 = [3,2,1,0]
t3 = [0,1,2,3]

print 'testing can_morph and ranking'
assert(can_morph(t1, t2) == True)
assert(ranking(t1, t2)   == -2)

assert(can_morph(t1, t3) == True)
assert(ranking(t1, t2)   == -2)

assert(can_morph(t2, t3) == True)
assert(ranking(t2, t3)   == 0)

assert(can_morph(t2, t1) == True)
assert(can_morph(t3, t2) == False)*/

struct container{
  vint board;
  vint moves;
  int  rank;
  container(vint &board_, vint &moves_, int rank_){
    board = board_;
    moves = moves_;
    rank  = rank_;
  }
  bool operator<(const container &rhs) const{
    return rank < rhs.rank;
  }
};

vint move(vint y1, vint y2){
  int chess_size = y1.size();
  std::priority_queue<container> paths_to_check; // = std::queue<container>();
  vint empty; // = vint();
  container first_element = container(y1, empty, ranking(y1, y2));
  //first_element.board = y1;
  //first_element.moves = vint();
  //first_element.rank  = ranking(y1, y2);

  paths_to_check.push(first_element);
  while( !paths_to_check.empty() ){
    //pop first element
    container element = paths_to_check.top();
    paths_to_check.pop();
    //are we there yet?
    if( element.rank == chess_size )
      return element.moves;
    //loop over possible combinations
    for(int r1 = 0; r1 < (chess_size-1); r1++){
      for(int r2 = r1; r2 < chess_size; r2++){
	//check if swap is allowed
	vint new_candidate = swap(element.board, r1, r2);
	if(new_candidate.size() == 0)
	  continue;
	//check if morphing is allowed
	if(!can_morph(new_candidate, y2))
	  continue;
	//compute ranking
	int new_rank = ranking(new_candidate, y2);
	vint clone = element.moves;
	clone.push_back(r1);
	clone.push_back(r2);
	//put element
	paths_to_check.push(
		   container(new_candidate,
			     clone,
			     new_rank)
		   );
      }
    }
  }
  empty.push_back(-1);
  return empty;
}

vint make_vint(int* array, unsigned int size){
  //helper class
  vint ret;
  for(unsigned int i=0; i < size; i++){
    ret.push_back(array[i]);
  }
  return ret;
}

#include <assert.h> 

int main(){
  //test cases
  std::cout << "testing case 1" << std::endl;
  int a[1] = {0};
  vint c1  = make_vint(a, 1);
  vint c2  = make_vint(a, 1);
  vint ret = move(c1, c2);  
  vint answer;
  assert(ret == answer);

  
  std::cout << "testing case 2" << std::endl;
  int b[2] = {1, 0};
  int c[2] = {0, 1};
  c1  = make_vint(b, 2);
  c2  = make_vint(c, 2);
  ret = move(c1, c2);  
  answer = make_vint(c, 2);
  assert(ret == answer);

  std::cout << "testing case 3" << std::endl;
  int d[3] = {1,2,0};
  int e[3] = {2,0,1};
  int kk[1] = {-1};
  c1  = make_vint(d, 3);
  c2  = make_vint(e, 3);
  ret = move(c1, c2);  
  answer = make_vint(kk, 1);
  assert(ret == answer);

  std::cout << "testing case 4" << std::endl;
  int f[6] = {2,1,0,3,5,4};
  int g[6] = {0,1,2,3,4,5};
  int h[4] = {0, 2, 4, 5};
  c1  = make_vint(f, 6);
  c2  = make_vint(g, 6);
  ret = move(c1, c2);  
  answer = make_vint(h, 4);
  assert(ret == answer);//*/

  std::cout << "testing case 5" << std::endl;
  int i[11] = {10,9,8,7,6,5,4,3,2,1,0};
  int l[11] = {0,1,2,3,4,5,6,7,8,9,10};
  int m[10] = {0, 10, 1, 9, 2, 8, 3, 7, 4, 6};
  c1  = make_vint(i, 11);
  c2  = make_vint(l, 11);
  ret = move(c1, c2);  
  answer = make_vint(m, 10);
  assert(ret == answer);
  std::cout << "DONE!" << std::endl;
  return 0;
}
