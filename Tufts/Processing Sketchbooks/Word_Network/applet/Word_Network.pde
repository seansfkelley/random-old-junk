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

static final color COLOR_BACKGROUND =        #000000,
                   COLOR_NODE_LOOSE =        #7B7B7B,
                   COLOR_NODE_LOOSE_FADED =  #303030,
                   COLOR_NODE_FIXED =        #CE0606,
                   COLOR_NODE_INSIDE =       #5B5B5B,
                   COLOR_NODE_INSIDE_FADED = #202020,
                   COLOR_EDGE =              #9C00F4,
                   COLOR_EDGE_FADED =        #3A005B,
                   COLOR_TEXT =              #D0D0D0,
                   COLOR_TEXT_FADED =        #707070;

static final int TEXT_SIZE_SMALL = 8,
                 TEXT_SIZE_LARGE = 24;

static final float MOVEMENT_MAX_SPEED = 7,
                   MOVEMENT_NUM_NODES_THRESHOLD = 0.05; // Percentage.

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
void setup() {
  size(600, 600);
  background(COLOR_BACKGROUND);
  loadData();
  println(nodeCount + " nodes connected by " + edgeCount + " edges");
  smooth();
  
  for (int i = 0; i < nodeCount; ++i){
    nodes[i].diameter = 2 * sqrt(map(nodes[i].count, 1, highestNodeDegree, CIRCLE_AREA_MIN, CIRCLE_AREA_MAX) / PI);
  }
  
  for (int i = 0; i < edgeCount; ++i){
    edges[i].weight = map((float) edges[i].count, 1.0, (float) highestEdgeDegree, EDGE_STROKE_WT_MIN, EDGE_STROKE_WT_MAX);
  }

  textAlign(CENTER, CENTER);
  ellipseMode(CENTER);
}


void loadData() {
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
void addEdge(String fromLabel, String toLabel) {
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

boolean ignoreWord(String what) {
  for (int i = 0; i < ignore.length; i++) {
    if (what.equals(ignore[i])) {
      return true;
    }
  }
  return false;
}


// Find a node using a HashMap to efficiently look up a 
// node based on its label.  If it is not found, add a node.
Node findNode(String label) {
  label = label.toLowerCase();
  Node n = (Node) nodeTable.get(label);
  if (n == null) {
    return addNode(label);
  }
  return n;
}


// Put a new node into the nodeTable so that it can be 
// retrieved by name.
Node addNode(String label) {
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
void draw() {
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

void mousePressed() {
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
void mouseDragged() {
  if (selection != null) {
    selection.x = mouseX;
    selection.y = mouseY;
  }
  
  loop();
}


void mouseReleased() {
  selection = null;
}
