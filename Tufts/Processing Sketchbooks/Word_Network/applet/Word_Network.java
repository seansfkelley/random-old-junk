import processing.core.*; 
import processing.xml.*; 

import java.util.ArrayDeque; 

import java.applet.*; 
import java.awt.*; 
import java.awt.image.*; 
import java.awt.event.*; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class Word_Network extends PApplet {

// Tufts COMP 150-04, Spring 2010
// Assignment 4 Starter Code

// This sketch is adapted from the graph demo in "Visualizing Data", by Ben Fry. 
// Fry's code is available at http://benfry.com/writing/graphlayout/ch08-graphlayout.zip

static final String FILENAME = "paulsimon.txt";

int nodeCount, highestNodeDegree = 0;
Node[] nodes = new Node[100];
HashMap nodeTable = new HashMap();
Node selection;
int nodesFixed = 0;

int edgeCount, highestEdgeDegree = 0;
Edge[] edges = new Edge[500];

static final int COLOR_BACKGROUND =        0xff000000,
                   COLOR_NODE_LOOSE =        0xff7B7B7B,
                   COLOR_NODE_LOOSE_FADED =  0xff303030,
                   COLOR_NODE_FIXED =        0xffCE0606,
                   COLOR_NODE_INSIDE =       0xff5B5B5B,
                   COLOR_NODE_INSIDE_FADED = 0xff202020,
                   COLOR_EDGE =              0xff9C00F4,
                   COLOR_EDGE_FADED =        0xff3A005B,
                   COLOR_TEXT =              0xffD0D0D0,
                   COLOR_TEXT_FADED =        0xff707070;

static final int TEXT_SIZE_SMALL = 8,
                 TEXT_SIZE_LARGE = 24;

static final float MOVEMENT_MAX_SPEED = 7,
                   MOVEMENT_NUM_NODES_THRESHOLD = 0.05f; // Percentage.

static final int MOVEMENT_NODE_HISTORY_LENGTH =   30,
                 MOVEMENT_NODE_JIGGLE_THRESHOLD =  5;

static final float EDGE_STROKE_WT_MIN =   1,
                   EDGE_STROKE_WT_MAX =   5;
//                   EDGE_LENGTH_MIN =     75,
//                   EDGE_LENGTH_MAX =    150;

static final float CIRCLE_AREA_MIN = 100,
                   CIRCLE_AREA_MAX = 900;

PFont FONT = createFont("SansSerif", 10);
PFont FONT_LARGE = createFont("SansSerif", 14);

// Create the structure that will be used later for drawing, 
// but don't yet do anything related to the node layout; 
// that is handled by draw().
public void setup() {
  size(600, 600);
  background(COLOR_BACKGROUND);
  loadData();
  println(nodeCount + " nodes connected by " + edgeCount + " edges");
  smooth();
  
  for (int i = 0; i < nodeCount; ++i){
    nodes[i].diameter = 2 * sqrt(map(nodes[i].count, 1, highestNodeDegree, CIRCLE_AREA_MIN, CIRCLE_AREA_MAX) / PI);
  }
  
  for (int i = 0; i < edgeCount; ++i){
    edges[i].weight = map((float) edges[i].count, 1.0f, (float) highestEdgeDegree, EDGE_STROKE_WT_MIN, EDGE_STROKE_WT_MAX);
  }

  textAlign(CENTER, CENTER);
  ellipseMode(CENTER);
}


public void loadData() {
  String[] lines = loadStrings(FILENAME);
  
  // Make the text into a single String object
  String line = join(lines, " ");
  
  // Replace -- with an actual em dash
  line = line.replaceAll("--", "\u2014");
  
  // Split into phrases using any of the provided tokens
  String[] phrases = splitTokens(line, ".,;:?!\u2014\"");
  //println(phrases);

  for (int i = 0; i < phrases.length; i++) {
    // Make this phrase lowercase
    String phrase = phrases[i].toLowerCase();
    // Split each phrase into individual words at one or more spaces
    String[] words = splitTokens(phrase, " ");
    for (int w = 0; w < words.length-1; w++) {
      addEdge(words[w], words[w+1]);
    }
  }
}


// Adding an Edge object involves first finding two nodes 
// by name, creating a node if it doesn't exist.
public void addEdge(String fromLabel, String toLabel) {
  // Filter out unnecessary words
  if (ignoreWord(fromLabel) || ignoreWord(toLabel)) return;

  Node from = findNode(fromLabel);
  Node to = findNode(toLabel);
  from.increment();
  to.increment();
  
  for (int i = 0; i < edgeCount; i++) {
    if (edges[i].from == from && edges[i].to == to) {
      edges[i].increment();
      return;
    }
  } 
  
  Edge e = new Edge(from, to);
  e.increment();
  if (edgeCount == edges.length) {
    edges = (Edge[]) expand(edges);
  }
  edges[edgeCount++] = e;
}


String[] ignore = { "a", "of", "the", "i", "it", "you", "and", "to", "-", "'" };

public boolean ignoreWord(String what) {
  for (int i = 0; i < ignore.length; i++) {
    if (what.equals(ignore[i])) {
      return true;
    }
  }
  return false;
}


// Find a node using a HashMap to efficiently look up a 
// node based on its label.  If it is not found, add a node.
public Node findNode(String label) {
  label = label.toLowerCase();
  Node n = (Node) nodeTable.get(label);
  if (n == null) {
    return addNode(label);
  }
  return n;
}


// Put a new node into the nodeTable so that it can be 
// retrieved by name.
public Node addNode(String label) {
  Node n = new Node(label);  
  if (nodeCount == nodes.length) {
    nodes = (Node[]) expand(nodes);
  }
  nodeTable.put(label, n);
  nodes[nodeCount++] = n;
  return n;
}


// Relaxation is the process finding the best location
// for each of the edges and nodes.  (See the relax() 
// methods in Edge and Node classes.)  Edges are drawn 
// before nodes so that the lines appear behind the 
// node labels.
public void draw() {
  background(COLOR_BACKGROUND);

  for (int i = 0; i < nodeCount; i++) {
    nodes[i].relax();
  }
  
    for (int i = 0 ; i < edgeCount ; i++) {
    edges[i].relax();
  }
  
  int numMoved = 0;
  for (int i = 0; i < nodeCount; i++) {
    if (nodes[i].update()){
      numMoved++;
    }
  }
  for (int i = 0 ; i < edgeCount ; i++) {
    edges[i].draw();
  }
  for (int i = 0 ; i < nodeCount ; i++) {
    nodes[i].draw();
  }
  
  if (numMoved < nodeCount * MOVEMENT_NUM_NODES_THRESHOLD && selection == null){
    noLoop();
  }
}

public void mousePressed() {
  // Done in reverse order to match up with the user's expectation that nodes sitting
  // on top of other nodes will be the ones selected by a click. Doing it in forward
  // order will always cause the underlying node to be selected.
  for (int i = nodeCount - 1; i >= 0; --i){
    if (dist(mouseX, mouseY, nodes[i].x, nodes[i].y) < nodes[i].diameter){
      selection = nodes[i];
      break;
    }
  }
  if (selection != null) {
    if (mouseButton == LEFT) {
      if (!selection.fixed){
        nodesFixed++;
      }
      selection.fixed = true;
      
    } else if (mouseButton == RIGHT) {
      if (selection.fixed){
        nodesFixed--;
      }
      selection.fixed = false;
    }
  }
  
  loop();
}

// Handle user dragging of a node.
public void mouseDragged() {
  if (selection != null) {
    selection.x = mouseX;
    selection.y = mouseY;
  }
  
  loop();
}


public void mouseReleased() {
  selection = null;
}
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
  
  
  public void increment() {
    count++;
    highestEdgeDegree = max(count, highestEdgeDegree);
  }
  
  // See the relax() method in the Node class.
  public void relax() {
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


  public void draw() {
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
// Tufts COMP 150-04, Spring 2010
// Assignment 4 Starter Code

// This sketch is adapted from the graph demo in "Visualizing Data", by Ben Fry. 
// Fry's code is available at http://benfry.com/writing/graphlayout/ch08-graphlayout.zip



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
    
  public void increment() {
    count++;
    highestNodeDegree = max(count, highestNodeDegree);
  }
  
  // Calculate the placement of each node and lengths for each edge.
  // This is handled as a force-directed layout, a "toy physics" 
  // simulation in which edges act like springs which have a "rest 
  // length".  Relaxation is the process of applying push and pull
  // forces on the springs to allow them to settle to a stable layout.
  public void relax() {
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
  
  public boolean update() {
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


  public void draw() {
    textFont(FONT);
    strokeWeight(1.5f);
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


  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#FFFFFF", "Word_Network" });
  }
}
