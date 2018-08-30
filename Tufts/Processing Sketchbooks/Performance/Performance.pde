// Tufts COMP 150-04, Spring 2010
// Assignment 3 Starter Code
// Modified from Ben Fry's book "Visualizing Data"

FloatTable data;
  
float[] dataMaxes = new float[] {100, // 100% is the max.
                                 200, // > 100 means the load is too high.
                                 4096 // 4GB
                                 };

float plotX1, plotY1, plotX2, plotY2;
float labelX, labelY;

int currentColumn = 0;

int secondMax;

int secondInterval = 30;

String mouseLabelValue = "", mouseLabelTime = "";
boolean mouseLine = false;

int[] yIntervals = new int[] {20, 20, 1024};
String[] yLabels = new String[] {"%", "%", " MB"};

PFont plotFont; 

void setup() {
  size(1024, 600);
  
  data = new FloatTable("usage.tsv");
  
  secondMax = Integer.parseInt(data.getRowName(data.getRowCount() - 1));

  // Corners of the plotted time series
  plotX1 = 80; 
  plotX2 = width - 80;
  labelX = 30;
  plotY1 = 60;
  plotY2 = height - 70;
  labelY = height - 15;
  
  plotFont = createFont("SansSerif", 20);
  textFont(plotFont);

  smooth();
}


void draw() {
  background(224);
  
  // Show the plot area as a white box  
  fill(255);
  rectMode(CORNERS);
  noStroke();
  rect(plotX1, plotY1, plotX2, plotY2);

  drawTitleTabs();
  drawAxisLabels();
  drawXLabels();
  drawYLabels();
  drawMouseLine();

  drawData(currentColumn); 
  
  drawMouseLabel();
  
  noLoop();
}


void drawTitle() {
  fill(0);
  textSize(20);
  textAlign(LEFT);
  String title = data.getColumnName(currentColumn);
  text(title, plotX1, plotY1 - 10);
}


float[] tabLeft, tabRight;  // Add above setup()
float tabTop, tabBottom;
float tabPad = 10;

void drawTitleTabs() {
  rectMode(CORNERS);
  noStroke();
  textSize(20);
  textAlign(LEFT);

  // On first use of this method, allocate space for an array
  // to store the values for the left and right edges of the tabs
  if (tabLeft == null) {
    tabLeft = new float[data.getColumnCount()];
    tabRight = new float[data.getColumnCount()];
  }
  
  float runningX = plotX1; 
  tabTop = plotY1 - textAscent() - 15;
  tabBottom = plotY1;
  
  for (int col = 0; col < data.getColumnCount(); col++) {
    String title = data.getColumnName(col);
    tabLeft[col] = runningX; 
    float titleWidth = textWidth(title);
    tabRight[col] = tabLeft[col] + tabPad + titleWidth + tabPad;
    
    // If the current tab, set its background white, otherwise use pale gray
    fill(col == currentColumn ? 255 : 224);
    rect(tabLeft[col], tabTop, tabRight[col], tabBottom);
    
    // If the current tab, use black for the text, otherwise use dark gray
    fill(col == currentColumn ? 0 : 64);
    text(title, runningX + tabPad, plotY1 - 10);
    
    runningX = tabRight[col];
  }
}


void mousePressed() {
  if (mouseY > tabTop && mouseY < tabBottom) {
    for (int col = 0; col < data.getColumnCount(); col++) {
      if (mouseX > tabLeft[col] && mouseX < tabRight[col]) {
        setCurrent(col);
        redraw();
      }
    }
  }
}

void mouseMoved(){
  mouseLabelValue = mouseLabelTime = "";
  mouseLine = false;
  if (mouseY < plotY2 && mouseY > plotY1){
    int dataPointX = round(map(mouseX, plotX1, plotX2, 0, secondMax));
    if (dataPointX >= 0 && dataPointX < data.getRowCount()){
      mouseLabelValue = String.valueOf(round(data.getFloat(dataPointX, currentColumn))) + yLabels[currentColumn];
      mouseLabelTime =  formatSeconds(dataPointX);
      mouseLine = true;
    }
  }
  redraw();
}

String formatSeconds(int seconds){
  return String.valueOf(seconds / 60) + (seconds % 60 < 10 ? ":0" : ":") + String.valueOf(seconds % 60);
}

void setCurrent(int col) {
  currentColumn = col;
}


void drawAxisLabels() {
  fill(0);
  textSize(13);
  textLeading(15);
  
  textAlign(CENTER, CENTER);
  text(yLabels[currentColumn], labelX, (plotY1 + plotY2) / 2);
  textAlign(CENTER);
  text("Elapsed Time (minutes)", (plotX1 + plotX2) / 2, labelY);
}


void drawXLabels() {
  fill(0);
  textSize(10);
  textAlign(CENTER);
  
  for (int sec = secondInterval; sec < secondMax; sec += secondInterval) {
    float x = map(sec, 0, secondMax, plotX1, plotX2);
    text(formatSeconds(sec), x, plotY2 + textAscent() + 16);
  }
}

void drawMouseLine(){
  if (mouseLine){
    stroke(196);
    strokeWeight(.5);
    line(mouseX, plotY1, mouseX, plotY2);
  }
}  

void drawYLabels() {
  fill(0);
  textSize(10);
  textAlign(RIGHT);
  
  stroke(128);
  strokeWeight(1);

  for (float v = 0; v <= dataMaxes[currentColumn]; v += yIntervals[currentColumn]) {
    float y = map(v, 0, dataMaxes[currentColumn], plotY2, plotY1);  
    text(floor(v), plotX1 - 10, y + 4);
    line(plotX1 - 4, y, plotX1, y);     // Draw a tick
  }
}


void drawData(int col) { 
  if (col == 0 || col == 2){
    strokeWeight(1.5); 
    stroke(#5679C1); 
    beginShape(); 
    if (col == 2){
      fill(#5679C1);
      vertex(plotX1, plotY2);
    }
    else
      noFill(); 
    int rowCount = data.getRowCount(); 
    for (int row = 0; row < rowCount; row++) { 
      if (data.isValid(row, col)) { 
        float value = data.getFloat(row,col);  
        float x = map(row, 0, secondMax - 1, plotX1, plotX2); 
        float y = map(value, 0, dataMaxes[col], plotY2, plotY1);
        vertex(x, y); 
      } 
    }
    if (col == 2)
      vertex(plotX2, plotY2);
    endShape(); 
  }
  else if (col == 1){
    rectMode(CORNERS);
    int rowCount = data.getRowCount(); 
    for (int row = 0; row < rowCount; row++) { 
      if (data.isValid(row, col)) { 
        float value = data.getFloat(row,col);  
        float x = map(row, 0, secondMax, plotX1, plotX2); 
        float y = map(value, 0, dataMaxes[col], plotY2, plotY1);
        if (value < 100)
          fill(#5679C1);
        else
          fill(#CA1D1D);
        noStroke();
        rect(x, (plotY1 + plotY2) / 2, ceil(x + (plotX2 - plotX1) / rowCount), y);
      } 
    } 
  }
} 

void drawMouseLabel(){
  fill(0);
  textSize(10);
  textAlign(CENTER, BOTTOM);
  text(mouseLabelValue, mouseX, mouseY);
  textAlign(CENTER, TOP);
  text(mouseLabelTime, mouseX, plotY2 + 2);
}
