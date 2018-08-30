// Tufts COMP 150-04, Spring 2010
// Assignment 4 Starter Code

// This sketch is adapted from the graph demo in "Visualizing Data", by Ben Fry. 
// Fry's code is available at http://benfry.com/writing/graphlayout/ch08-graphlayout.zip


class Edge {
  Node from;
  Node to;
  float len, weight;
  int count;


  Edge(Node from, Node to) {
    this.from = from;
    this.to = to;
    this.len = 80;
    weight = EDGE_STROKE_WT_MIN;
  }
  
  
  void increment() {
    count++;
    highestEdgeDegree = max(count, highestEdgeDegree);
  }
  
  // See the relax() method in the Node class.
  void relax() {
    float vx = to.x - from.x;
    float vy = to.y - from.y;
    float d = mag(vx, vy);
    if (d > 0) {
      float f = (len - d) / (d * 3);
      float dx = f * vx;
      float dy = f * vy;
      to.dx += dx;
      to.dy += dy;
      from.dx -= dx;
      from.dy -= dy;
    }
  }


  void draw() {
    if (nodesFixed > 0 && !to.fixed && !from.fixed){
      stroke(COLOR_EDGE_FADED);
    }
    else{
      stroke(COLOR_EDGE);
    }
      
    strokeWeight(weight);
    line(from.x, from.y, to.x, to.y);
    
    if (to.fixed || from.fixed){
      textFont(FONT_LARGE);
      fill(COLOR_TEXT);
      text("" + count, (from.x + to.x) / 2, (from.y + to.y) / 2);
      to.drawLight = true;
      from.drawLight = true;
    }
  }
}
