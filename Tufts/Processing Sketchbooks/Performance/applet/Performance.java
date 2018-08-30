import processing.core.*; 
import processing.xml.*; 

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

public class Performance extends PApplet {

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

public void setup() {
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


public void draw() {
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


public void drawTitle() {
  fill(0);
  textSize(20);
  textAlign(LEFT);
  String title = data.getColumnName(currentColumn);
  text(title, plotX1, plotY1 - 10);
}


float[] tabLeft, tabRight;  // Add above setup()
float tabTop, tabBottom;
float tabPad = 10;

public void drawTitleTabs() {
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


public void mousePressed() {
  if (mouseY > tabTop && mouseY < tabBottom) {
    for (int col = 0; col < data.getColumnCount(); col++) {
      if (mouseX > tabLeft[col] && mouseX < tabRight[col]) {
        setCurrent(col);
        redraw();
      }
    }
  }
}

public void mouseMoved(){
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

public String formatSeconds(int seconds){
  return String.valueOf(seconds / 60) + (seconds % 60 < 10 ? ":0" : ":") + String.valueOf(seconds % 60);
}

public void setCurrent(int col) {
  currentColumn = col;
}


public void drawAxisLabels() {
  fill(0);
  textSize(13);
  textLeading(15);
  
  textAlign(CENTER, CENTER);
  text(yLabels[currentColumn], labelX, (plotY1 + plotY2) / 2);
  textAlign(CENTER);
  text("Elapsed Time (minutes)", (plotX1 + plotX2) / 2, labelY);
}


public void drawXLabels() {
  fill(0);
  textSize(10);
  textAlign(CENTER);
  
  for (int sec = secondInterval; sec < secondMax; sec += secondInterval) {
    float x = map(sec, 0, secondMax, plotX1, plotX2);
    text(formatSeconds(sec), x, plotY2 + textAscent() + 16);
  }
}

public void drawMouseLine(){
  if (mouseLine){
    stroke(196);
    strokeWeight(.5f);
    line(mouseX, plotY1, mouseX, plotY2);
  }
}  

public void drawYLabels() {
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


public void drawData(int col) { 
  if (col == 0 || col == 2){
    strokeWeight(1.5f); 
    stroke(0xff5679C1); 
    beginShape(); 
    if (col == 2){
      fill(0xff5679C1);
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
          fill(0xff5679C1);
        else
          fill(0xffCA1D1D);
        noStroke();
        rect(x, (plotY1 + plotY2) / 2, ceil(x + (plotX2 - plotX1) / rowCount), y);
      } 
    } 
  }
} 

public void drawMouseLabel(){
  fill(0);
  textSize(10);
  textAlign(CENTER, BOTTOM);
  text(mouseLabelValue, mouseX, mouseY);
  textAlign(CENTER, TOP);
  text(mouseLabelTime, mouseX, plotY2 + 2);
}
// Tufts COMP 150-04, Spring 2010
// Assignment 3 Starter Code
// Modified from Ben Fry's book "Visualizing Data"

// first line of the file should be the column headers
// first column should be the row titles
// all other values are expected to be floats
// getFloat(0, 0) returns the first data value in the upper lefthand corner
// files should be saved as "text, tab-delimited"
// empty rows are ignored
// extra whitespace is ignored


class FloatTable {
  int rowCount;
  int columnCount;
  float[][] data;
  String[] rowNames;
  String[] columnNames;
  
  
  FloatTable(String filename) {
    String[] rows = loadStrings(filename);
    
    String[] columns = split(rows[0], TAB);
    columnNames = subset(columns, 1); // upper-left corner ignored
    scrubQuotes(columnNames);
    columnCount = columnNames.length;

    rowNames = new String[rows.length-1];
    data = new float[rows.length-1][];

    // start reading at row 1, because the first row was only the column headers
    for (int i = 1; i < rows.length; i++) {
      if (trim(rows[i]).length() == 0) {
        continue; // skip empty rows
      }
      if (rows[i].startsWith("#")) {
        continue;  // skip comment lines
      }

      // split the row on the tabs
      String[] pieces = split(rows[i], TAB);
      scrubQuotes(pieces);
      
      // copy row title
      rowNames[rowCount] = pieces[0];
      // copy data into the table starting at pieces[1]
      data[rowCount] = parseFloat(subset(pieces, 1));

      // increment the number of valid rows found so far
      rowCount++;      
    }
    // resize the 'data' array as necessary
    data = (float[][]) subset(data, 0, rowCount);
  }
  
  
  public void scrubQuotes(String[] array) {
    for (int i = 0; i < array.length; i++) {
      if (array[i].length() > 2) {
        // remove quotes at start and end, if present
        if (array[i].startsWith("\"") && array[i].endsWith("\"")) {
          array[i] = array[i].substring(1, array[i].length() - 1);
        }
      }
      // make double quotes into single quotes
      array[i] = array[i].replaceAll("\"\"", "\"");
    }
  }
  
  
  public int getRowCount() {
    return rowCount;
  }
  
  
  public String getRowName(int rowIndex) {
    return rowNames[rowIndex];
  }
  
  
  public String[] getRowNames() {
    return rowNames;
  }

  
  // Find a row by its name, returns -1 if no row found. 
  // This will return the index of the first row with this name.
  // A more efficient version of this function would put row names
  // into a Hashtable (or HashMap) that would map to an integer for the row.
  public int getRowIndex(String name) {
    for (int i = 0; i < rowCount; i++) {
      if (rowNames[i].equals(name)) {
        return i;
      }
    }
    //println("No row named '" + name + "' was found");
    return -1;
  }
  
  
  // technically, this only returns the number of columns 
  // in the very first row (which will be most accurate)
  public int getColumnCount() {
    return columnCount;
  }
  
  
  public String getColumnName(int colIndex) {
    return columnNames[colIndex];
  }
  
  
  public String[] getColumnNames() {
    return columnNames;
  }


  public float getFloat(int rowIndex, int col) {
    // Remove the 'training wheels' section for greater efficiency
    // It's included here to provide more useful error messages
    
    // begin training wheels
    if ((rowIndex < 0) || (rowIndex >= data.length)) {
      throw new RuntimeException("There is no row " + rowIndex);
    }
    if ((col < 0) || (col >= data[rowIndex].length)) {
      throw new RuntimeException("Row " + rowIndex + " does not have a column " + col);
    }
    // end training wheels
    
    return data[rowIndex][col];
  }
  
  
  public boolean isValid(int row, int col) {
    if (row < 0) return false;
    if (row >= rowCount) return false;
    //if (col >= columnCount) return false;
    if (col >= data[row].length) return false;
    if (col < 0) return false;
    return !Float.isNaN(data[row][col]);
  }


  public float getColumnMin(int col) {
    float m = Float.MAX_VALUE;
    for (int row = 0; row < rowCount; row++) {
      if (isValid(row, col)) {
        if (data[row][col] < m) {
          m = data[row][col];
        }
      }
    }
    return m;
  }


  public float getColumnMax(int col) {
    float m = -Float.MAX_VALUE;
    for (int row = 0; row < rowCount; row++) {
      if (isValid(row, col)) {
        if (data[row][col] > m) {
          m = data[row][col];
        }
      }
    }
    return m;
  }

  
  public float getRowMin(int row) {
    float m = Float.MAX_VALUE;
    for (int col = 0; col < columnCount; col++) {
      if (isValid(row, col)) {
        if (data[row][col] < m) {
          m = data[row][col];
        }
      }
    }
    return m;
  } 


  public float getRowMax(int row) {
    float m = -Float.MAX_VALUE;
    for (int col = 0; col < columnCount; col++) {
      if (isValid(row, col)) {
        if (data[row][col] > m) {
          m = data[row][col];
        }
      }
    }
    return m;
  }


  public float getTableMin() {
    float m = Float.MAX_VALUE;
    for (int row = 0; row < rowCount; row++) {
      for (int col = 0; col < columnCount; col++) {
        if (isValid(row, col)) {
          if (data[row][col] < m) {
            m = data[row][col];
          }
        }
      }
    }
    return m;
  }


  public float getTableMax() {
    float m = -Float.MAX_VALUE;
    for (int row = 0; row < rowCount; row++) {
      for (int col = 0; col < columnCount; col++) {
        if (isValid(row, col)) {
          if (data[row][col] > m) {
            m = data[row][col];
          }
        }
      }
    }
    return m;
  }
}

  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#FFFFFF", "Performance" });
  }
}
