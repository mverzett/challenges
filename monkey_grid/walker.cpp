/*CHALLENGE DESCRIPTION

  There is a monkey which can walk around on a planar grid. The monkey can move one space at a time left, right, up or down. 
  That is, from (x, y) the monkey can go to (x+1, y), (x-1, y), (x, y+1), and (x, y-1). Points where the sum of the digits 
  of the absolute value of the x coordinate plus the sum of the digits of the absolute value of the y coordinate are lesser 
  than or equal to 19 are accessible to the monkey. For example, the point (59, 79) is inaccessible because 5 + 9 + 7 + 9 = 30, 
  which is greater than 19. Another example: the point (-5, -7) is accessible because abs(-5) + abs(-7) = 5 + 7 = 12, which is less than 19. 
  How many points can the monkey access if it starts at (0, 0), including (0, 0) itself?
*/

struct point2D{
  int x,y;
  point2D(int parx, int pary){
    x = parx;
    y = pary;
  }

  bool operator<(const point2D& rhs) const{
    return x < rhs.x || (x == rhs.x && y < rhs.y);
  }

  bool operator==(const point2D& rhs) const{
    return x == rhs.x && y == rhs.y;
  }

  point2D operator+(const point2D& rhs) const{
    return point2D(x + rhs.x, y + rhs.y);
  }
};

/*
//TEST CASES
#include <assert.h> 
point2D p1(1,1); 
point2D p2(2,2); 
point2D p3(1,3); 
point2D p4(1,1); 

p1 < p2
p2 < p1
p1 < p3
p1 == p4
p1+p4 == p2
assert(p1 < p2)

 */

//ROOT bindings for graphics
#include <TGraph.h>
#include <TCanvas.h>

//helper function
static int sum_digits(int number){
  int mod = number % 10;
  int div = number / 10;
  if(div == 0)
    return mod;
  else
    return mod + sum_digits(div);
}


class Walker{
public:
  Walker(int boundary);
  int walk(point2D starting_point);

private:
  int boundary_;
  TGraph graph_; 
  TCanvas canvas_;
};


#include <set>
#include <stack>
#include <iostream>
#include <fstream>

Walker::Walker(int boundary):
  boundary_(boundary),
  canvas_(),
  graph_()
{
  graph_.Draw("AP");
  graph_.SetMarkerStyle(20);
  graph_.SetMarkerSize(0.5);
}

int Walker::walk(point2D starting_point){
  //empty set
  std::set<point2D>   visited_tiles;
  visited_tiles.insert(starting_point);
  std::stack<point2D> stack;
  stack.push(starting_point);
  int iteration = 0;
  point2D allowed_movements[4] = {point2D(-1, 0), point2D(1, 0), point2D(0, -1), point2D(0, 1)}; 
  while( !stack.empty() ){
      iteration++;
      point2D point = stack.top();
      stack.pop();
      graph_.SetPoint(iteration, point.x, point.y);
      if(iteration % 1000 == 0){
	graph_.Draw("AP");
        canvas_.Update();
      }
      //loop over allowed movements
      for(int i = 0; i < 4; i++){
	point2D candidate_point = point + allowed_movements[i];
	int sumx = sum_digits(abs(candidate_point.x));
	int sumy = sum_digits(abs(candidate_point.y));
	//check boundary condition
	if(sumx + sumy > boundary_)
	  continue;
	//check if already covered
	if(visited_tiles.find(candidate_point) != visited_tiles.end())
	  continue;
	visited_tiles.insert(candidate_point);
	stack.push(candidate_point);	
      }
    }

  //dump to txt, to compare
  // std::ofstream myfile;
  // myfile.open("tiles.txt");
  // for(std::set<point2D>::iterator myIterator = visited_tiles.begin();
  //     myIterator != visited_tiles.end();
  //     myIterator++)
  //   myfile << myIterator->x <<" " << myIterator->y << std::endl;
  // myfile.close();
  
  return visited_tiles.size();
  //as from stack walk: 125413
}
