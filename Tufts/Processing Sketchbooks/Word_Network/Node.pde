// Tufts COMP 150-04, Spring 2010
// Assignment 4 Starter Code

// This sketch is adapted from the graph demo in "Visualizing Data", by Ben Fry. 
// Fry's code is available at http://benfry.com/writing/graphlayout/ch08-graphlayout.zip

import java.util.ArrayDeque;

class Node {
  float x, y;
  float dx, dy;
  float diameter;
  boolean fixed = false, drawLight = false;
  String label;
  int count;
  ArrayDeque move_history_x, move_history_y;

  Node(String label) {
    this.label = label;
    
    x = random(width);
    y = random(height);
    
    move_history_x = new ArrayDeque(MOVEMENT_NODE_HISTORY_LENGTH);
    move_history_y = new ArrayDeque(MOVEMENT_NODE_HISTORY_LENGTH);
    for (int i = 0; i < MOVEMENT_NODE_HISTORY_LENGTH; ++i){
      move_history_x.addFirst(x);
      move_history_y.addFirst(y);
    }
  }
    
  void increment() {
    count++;
    highestNodeDegree = max(count, highestNodeDegree);
  }
  
  // Calculate the placement of each node and lengths for each edge.
  // This is handled as a force-directed layout, a "toy physics" 
  // simulation in which edges act like springs which have a "rest 
  // length".  Relaxation is the process of applying push and pull
  // forces on the springs to allow them to settle to a stable layout.
  void relax() {
    float ddx = 0;
    float ddy = 0;

    for (int j = 0; j < nodeCount; j++) {
      Node n = nodes[j];
      if (n != this) {
        float vx = x - n.x, vy = y - n.y;
        float lensq = vx * vx + vy * vy;
        if (lensq == 0) {
          ddx += random(1);
          ddy += random(1);
        } 
        // The physics appear to perform better when this is larger than the edge lengths.
        else if (lensq < 100 * 100) {
          ddx += vx / lensq;
          ddy += vy / lensq;
        }
      }
    }
    float dlen = mag(ddx, ddy) / 2;
    if (dlen > 0) {
      dx += ddx / dlen;
      dy += ddy / dlen;
    }
  }
  
  boolean update() {
    drawLight = nodesFixed == 0;
    
    float old_x, old_y, new_x, new_y;
    boolean moved = false;
    
    old_x = (Float) move_history_x.removeLast();
    old_y = (Float) move_history_y.removeLast();
    
    if (!fixed && dx != 0 && dy != 0) {
      new_x = x + constrain(dx, -MOVEMENT_MAX_SPEED, MOVEMENT_MAX_SPEED);
      new_y = y + constrain(dy, -MOVEMENT_MAX_SPEED, MOVEMENT_MAX_SPEED);
      
      new_x = constrain(new_x, 0, width);
      new_y = constrain(new_y, 0, height);

      if (dist(new_x, new_y, old_x, old_y) > MOVEMENT_NODE_JIGGLE_THRESHOLD){
        x = new_x;
        y = new_y;
        moved = true;
      }
      else{
        dx = 0;
        dy = 0;
      }
    }
    
    move_history_x.addFirst(x);
    move_history_y.addFirst(y);
    
    dx /= 2;
    dy /= 2;
    
    return moved;
  }


  void draw() {
    textFont(FONT);
    strokeWeight(1.5);
    if (fixed){
      stroke(COLOR_NODE_FIXED);
      fill(COLOR_NODE_INSIDE);
      ellipse(x, y, diameter, diameter);

      fill(COLOR_TEXT);
      text(label + " (" + count + ")", x, y);
    }
    else if (drawLight){
      stroke(COLOR_NODE_LOOSE);
      fill(COLOR_NODE_INSIDE);
      ellipse(x, y, diameter, diameter);

      fill(COLOR_TEXT);
      text(label, x, y);
    }
    else{
      stroke(COLOR_NODE_LOOSE_FADED);
      fill(COLOR_NODE_INSIDE_FADED);
      ellipse(x, y, diameter, diameter);

      fill(COLOR_TEXT_FADED);
      text(label, x, y);
    }
  }

}

