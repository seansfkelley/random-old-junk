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

public class EU_Trade extends PApplet {

final PFont FONT = createFont("GillSans", 12);

final int SIZE_X = 650, SIZE_Y = 725;
final int MAP_OFFSET_X = 25, MAP_OFFSET_Y = 25, BORDER_WIDTH = 2;
final int TOGGLE_WIDTH = 20, TOGGLE_SPACE = 8, TOGGLE_X = 64, TOGGLE_Y = SIZE_Y - TOGGLE_WIDTH * 2 - TOGGLE_SPACE - 16;

final int DEFAULT_TEXT_COLOR = 0xff000000,
            BORDER_COLOR = 0xff888888,
            BACKGROUND_COLOR = 0xffFFFFFF,
            SORT_TOGGLE_COLOR = 0xff1100CC;

final int[] TYPE_COLORS = {0xffDB0000, 0xffFE5C5C, 0xff11772D, 0xff3ED715};

boolean togglesOn = true, sliding = false;
int displayYear = 0;

PImage mapBackground, units, source;
Country[] countries;
int highlightedIndex = -1, numYears;
ToggleBox[] toggles;
ToggleBox sortToggle;
HorizontalSlider slider;

public void setup(){
  size(650, 725);
  textFont(FONT);
  mapBackground = loadImage("EU Map.png");
  loadData();
  smooth();
}

public void loadData(){
  FloatTable[] datasets = new FloatTable[4];
  datasets[EU + IMPORT] = new FloatTable("EU to EU Imports.tsv");
  datasets[EU + EXPORT] = new FloatTable("EU to EU Exports.tsv");
  datasets[WORLD + IMPORT] = new FloatTable("World to EU Imports.tsv");
  datasets[WORLD + EXPORT] = new FloatTable("EU to World Exports.tsv");
  
  FloatTable locations = new FloatTable("EU Country Locations in Pixels.tsv");
  
  String[] countryNames = locations.getRowNames();
  countries = new Country[countryNames.length];
  
  numYears = datasets[0].getNumColumns();
  
  float absoluteMax = 0;
  for (int i = 0; i < numYears; ++i){
    for (int j = 0; j < 4; ++j){
      absoluteMax = max(absoluteMax, max(datasets[j].getColumn(i)));
    }
  }
  
  for (int i = 0; i < countries.length; ++i){
    Country c = new Country(numYears);
    
    c.name = countryNames[i];
    c.x = (int) (locations.getValue(c.name, 0) + MAP_OFFSET_X);
    c.y = (int) (locations.getValue(c.name, 1) + MAP_OFFSET_Y);
    
    for (int j = 0; j < numYears; ++j){
      c.data[j][EU + IMPORT] = datasets[EU + IMPORT].getValue(c.name, j);
      c.data[j][EU + EXPORT] = datasets[EU + EXPORT].getValue(c.name, j);
      c.data[j][WORLD + IMPORT] = datasets[WORLD + IMPORT].getValue(c.name, j);
      c.data[j][WORLD + EXPORT] = datasets[WORLD + EXPORT].getValue(c.name, j);
    }
    c.computeAppearance(absoluteMax);
    
    countries[i] = c;
  }
  
  toggles = new ToggleBox[4];
  toggles[EU + IMPORT] =    new ToggleBox(TOGGLE_X, TOGGLE_Y, 
                                          TOGGLE_WIDTH, TYPE_COLORS[EU + IMPORT]);
  toggles[EU + EXPORT] =    new ToggleBox(TOGGLE_X, TOGGLE_Y + TOGGLE_WIDTH + TOGGLE_SPACE, 
                                          TOGGLE_WIDTH, TYPE_COLORS[EU + EXPORT]);
  toggles[WORLD + IMPORT] = new ToggleBox(TOGGLE_X + TOGGLE_WIDTH + TOGGLE_SPACE, TOGGLE_Y, 
                                          TOGGLE_WIDTH, TYPE_COLORS[WORLD + IMPORT]);
  toggles[WORLD + EXPORT] = new ToggleBox(TOGGLE_X + TOGGLE_WIDTH + TOGGLE_SPACE, TOGGLE_Y + TOGGLE_WIDTH + TOGGLE_SPACE, 
                                          TOGGLE_WIDTH, TYPE_COLORS[WORLD + EXPORT]);
  
  int sortTitleWidth = (int) textWidth("Sort Values?");
  
  sortToggle = new ToggleBox(SIZE_X - MAP_OFFSET_X - TOGGLE_WIDTH - sortTitleWidth / 2, TOGGLE_Y + TOGGLE_WIDTH / 2 + TOGGLE_SPACE / 2,
                             TOGGLE_WIDTH, SORT_TOGGLE_COLOR);
  
  slider = new HorizontalSlider(TOGGLE_X + 3 * TOGGLE_WIDTH + 2 * TOGGLE_SPACE, SIZE_X - MAP_OFFSET_X - sortTitleWidth - TOGGLE_WIDTH - TOGGLE_SPACE,
                                18, 32, TOGGLE_Y + TOGGLE_WIDTH + TOGGLE_SPACE / 2, datasets[0].getColumnNames(), "Year");
}

public void draw(){
  background(BACKGROUND_COLOR);
  stroke(BORDER_COLOR);
  fill(BORDER_COLOR);
  rectMode(CORNERS);
  rect(MAP_OFFSET_X - BORDER_WIDTH, MAP_OFFSET_Y - BORDER_WIDTH, 599 + MAP_OFFSET_X + BORDER_WIDTH, 599 + MAP_OFFSET_Y + BORDER_WIDTH);
  image(mapBackground, MAP_OFFSET_X, MAP_OFFSET_Y);
  
  for (int i = 0; i < countries.length; ++i){
    if (i != highlightedIndex){
      countries[i].draw_circle(displayYear);
    }
  }
  if (highlightedIndex != -1){
    countries[highlightedIndex].draw_circle(displayYear);
    countries[highlightedIndex].draw_text(displayYear);
  }
  
  textFont(FONT);
  fill(DEFAULT_TEXT_COLOR);
  textAlign(RIGHT, CENTER);
  text("Import  ", TOGGLE_X, TOGGLE_Y + TOGGLE_WIDTH / 2);
  text("Export  ", TOGGLE_X, TOGGLE_Y + 3 * (TOGGLE_WIDTH / 2) + TOGGLE_SPACE);
  textAlign(LEFT, BOTTOM);
  text("EU", TOGGLE_X, TOGGLE_Y - 2);
  text("Non-EU", TOGGLE_X + TOGGLE_WIDTH + TOGGLE_SPACE, TOGGLE_Y - 2);
  textAlign(CENTER, BOTTOM);
  text("Sort Values?", sortToggle.toggle.x + sortToggle.toggle.width / 2, sortToggle.toggle.y - 2);
  
  for (int i = 0; i < 4; ++i){
    toggles[i].draw();
  }
  
  sortToggle.draw();
  
  slider.draw();
}

public void mouseMoved(){
  if (!togglesOn){
    return;
  }
  if (highlightedIndex != -1 && countries[highlightedIndex].collide(displayYear)){
    return;
  }
  highlightedIndex = -1;
  for (int i = 0; i < countries.length; ++i){
    if (countries[i].collide(displayYear)){
      highlightedIndex = i;
      return;
    }
  }
}

public void mousePressed(){
  if (mouseButton != LEFT){
    return;
  }
   
  sliding = false;
  if (slider.collide()){
    sliding = true;
    return;
  }
  
  sortToggle.collide();
   
  togglesOn = false;
  for (int i = 0; i < 4; ++i){
    toggles[i].collide();
    if (toggles[i].on){
      togglesOn = true;
    }
  }
}

public void mouseDragged(){
  if (sliding){
    slider.move();
    displayYear = slider.getValue();
  }
}
static final int EU = 0, WORLD = 1, IMPORT = 0, EXPORT = 2,
                 TEXT_BIAS_X = 2, TEXT_BIAS_Y = 2,
                 TEXT_BOX_BORDER = 4;
static final float MAX_AREA = 1024,
                   MIN_COLLIDE_DIST = 10;

int BOX_EDGE_COLOR = 0xff000000,
      BOX_FILL_COLOR = 0xffFFFFFF,
      COUNTRY_TEXT_COLOR = 0xff000000;

public class Country{
  String name;
  int x, y;
  // Year, region + type.
  float[][] data;
  Rectangle[][] rectangles;
  int[][] ranking;
  
  public Country(int numYears){
    data = new float[numYears][4];
  }
  
  public void computeAppearance(float maxValue){
    rectangles = new Rectangle[data.length][4];
    ranking = new int[data.length][4];
    
    for (int yr = 0; yr < data.length; ++yr){
      float[] yearSorted = reverse(sort(data[yr]));
      for (int i = 0; i < 4; ++i){
        for (int j = 0; j < 4; ++j){
          if (yearSorted[i] == data[yr][j]){
            ranking[yr][i] = j;
            break;
          }
        }
      }
      
      // center = bottom right
      int len = round(sqrt(MAX_AREA * (data[yr][EU + IMPORT] / maxValue)));
      rectangles[yr][EU + IMPORT] = new Rectangle(x - len, y - len, len, len);
      
      // center = top right
      len = round(sqrt(MAX_AREA * (data[yr][EU + EXPORT] / maxValue)));
      rectangles[yr][EU + EXPORT] = new Rectangle(x - len, y + 1, len, len);
      
      // center = bottom left
      len = round(sqrt(MAX_AREA * (data[yr][WORLD + IMPORT] / maxValue)));
      rectangles[yr][WORLD + IMPORT] = new Rectangle(x + 1, y - len, len, len);
      
      // center = top left
      len = round(sqrt(MAX_AREA * (data[yr][WORLD + EXPORT] / maxValue)));
      rectangles[yr][WORLD + EXPORT] = new Rectangle(x + 1, y + 1, len, len);
    }
  }
  
  public void draw_circle(int yr){
    for (int i = 0; i < 4; ++i){
      int index = sortToggle.on ? ranking[yr][i] : i;
      if (!toggles[index].on){
        continue;
      }
      
      stroke(TYPE_COLORS[index]);
      strokeWeight(1);
      fill(TYPE_COLORS[index]);
      rectMode(CORNER);
      Rectangle r = rectangles[yr][index];
      rect(r.x, r.y, r.width, r.height);
    }
  }
  
  public void draw_text(int yr){
    strokeWeight(1);
    
    float offsetX = 0;
    if (toggles[EU + IMPORT].on){
      offsetX = rectangles[yr][EU + IMPORT].width;
    }
    if (toggles[EU + EXPORT].on){
      offsetX = max(offsetX, rectangles[yr][EU + EXPORT].width);
    }
    
    stroke(BOX_EDGE_COLOR);
    fill(BOX_FILL_COLOR);
    float w = textWidth(name);
    rectMode(CORNER);
    rect(x - offsetX - TEXT_BIAS_X - w - 2 * TEXT_BOX_BORDER, y - TEXT_BIAS_Y - 4 - TEXT_BOX_BORDER, 
         w + 2 * TEXT_BOX_BORDER, 12 + 2 * TEXT_BOX_BORDER);
    
    textAlign(RIGHT, CENTER);
    fill(COUNTRY_TEXT_COLOR);
    text(name, x - offsetX - TEXT_BIAS_X - TEXT_BOX_BORDER, y - TEXT_BIAS_Y);
    
    ArrayList toDraw = new ArrayList();
    for (int i = 0; i < 4; ++i){
      int index = sortToggle.on ? ranking[yr][i] : i;
      if (!toggles[index].on){
        continue;
      }
      toDraw.add(index);
    }
    
    offsetX = 0;
    if (toggles[WORLD + IMPORT].on){
      offsetX = rectangles[yr][WORLD + IMPORT].width;
    }
    if (toggles[WORLD + EXPORT].on){
      offsetX = max(offsetX, rectangles[yr][WORLD + EXPORT].width);
    }
    
    stroke(BOX_EDGE_COLOR);
    fill(BOX_FILL_COLOR);
    w = 0;
    for (int i = 0; i < toDraw.size(); ++i){
      w = max(w, textWidth(Float.toString(data[yr][(Integer) toDraw.get(i)])));
    }
    float xLocation = x + offsetX + TEXT_BIAS_X + 1,
          yLocation = y - (12 * (toDraw.size() - 1)) / 2 - TEXT_BIAS_Y - TEXT_BOX_BORDER;
    rect(xLocation, yLocation - 5, w + 2 * TEXT_BOX_BORDER, 12 * toDraw.size() + 2 * TEXT_BOX_BORDER);
    
    xLocation += TEXT_BOX_BORDER + 1;
    yLocation += TEXT_BOX_BORDER;
    
    textAlign(LEFT, CENTER);
    for (int i = 0; i < toDraw.size(); ++i){
      int index = (Integer) toDraw.get(i);
      fill(TYPE_COLORS[index]);
      text(Float.toString(data[yr][index]), xLocation, yLocation);
      yLocation += 12;
    }
  }
  
  public boolean collide(int yr){
    if (dist(mouseX, mouseY, x, y) < MIN_COLLIDE_DIST){
      return true;
    }
    else{
      for (int i = 0; i < 4; ++i){
        // No need to go in size order.
        if (toggles[i].on && rectangles[yr][i].contains(mouseX, mouseY)){
          return true;
        }
      }
    }
    
    return false;
  }
}
class FloatTable{
  HashMap data;
  String[] rows, cols;
  
  public FloatTable(String tsvFilename){
    data = new HashMap();
    
    String[] data_rows = loadStrings(tsvFilename);
    
    cols = subset(split(data_rows[0], TAB), 1);
    rows = new String[data_rows.length - 1];
    
    for (int i = 0; i < rows.length; ++i){
      String[] current_row = split(data_rows[i + 1], TAB);
      rows[i] = current_row[0];
      
      float[] row_data = new float[cols.length];
      for (int j = 0; j < cols.length; ++j){
        row_data[j] = Float.valueOf(current_row[j + 1]);
      }
      
      data.put(rows[i], row_data);
    }
    
    rows = sort(rows);
  }
  
  public String[] getRowNames(){
    return rows;
  }
  
  public String[] getColumnNames(){
    return cols;
  }
  
  public int getNumRows(){
    return rows.length;
  }
  
  public int getNumColumns(){
    return cols.length;
  }
  
  public float[] getRow(String row){
    return (float[]) data.get(row);
  }
  
  // Slow!
  public float[] getColumn(int col){
    float[] values = new float[rows.length];
    for (int i = 0; i < rows.length; ++i){
      values[i] = getValue(rows[i], col);
    }
    return values;
  }
  
  public float getValue(String row, int col){
    return ((float[]) data.get(row))[col];
  }
}
int SLIDER_BORDER_COLOR = 0xff000000,
      SLIDER_FILL_COLOR = 0xffFFFFFF,
      SLIDER_LINE_COLOR = 0xff000000,
      SLIDER_TEXT_COLOR = 0xff000000;

public class HorizontalSlider{
  int left, right, h, w, y, divisions, currentDivision, divisionWidth;
  String[] labels;
  String title;
  
  public HorizontalSlider(int left, int right, int h, int w, int y, String[] labels, String title){
    this.left = left;
    this.right = right;
    this.h = h;
    this.w = w;
    this.y = y;
    this.divisions = labels.length;
    this.labels = labels;
    this.title = title;
    currentDivision = 0;
    divisionWidth = (right - left) / divisions;
  }
  
  public void draw(){
    fill(DEFAULT_TEXT_COLOR);
    textAlign(CENTER, BOTTOM);
    text(title, left + (right - left) / 2, y - h);
    
    stroke(SLIDER_LINE_COLOR);
    strokeWeight(1.5f);
    line(left, y, right, y);
    
    stroke(SLIDER_BORDER_COLOR);
    strokeWeight(1);
    fill(SLIDER_FILL_COLOR);
    rectMode(CORNER);
    float rectLeft = map(currentDivision, 0, divisions - 1, left, right - w); 
    rect(rectLeft, y - h / 2, w, h);
    
    fill(SLIDER_TEXT_COLOR);
    textAlign(CENTER, CENTER);
    text(labels[currentDivision], rectLeft + w / 2, y);
  }
  
  public boolean collide(){
    float currentLeft = map(currentDivision, 0, divisions - 1, left, right - w),
          currentTop = y - h / 2;
    return mouseX >= currentLeft && mouseX <= currentLeft + w && mouseY >= currentTop && mouseY <= currentTop + h;
  }
  
  public void move(){
    currentDivision = round(constrain(map(mouseX, left, right, 0, divisions - 1), 0, divisions - 1));
  }
  
  public int getValue(){
    return currentDivision;
  }
}

int DEFAULT_OFF_COLOR = 0xff777777;

public class ToggleBox{
  int offColor, onColor;
  Rectangle toggle;
  boolean on;
  
  public ToggleBox(int x, int y, int sideLength, int onColor){
    toggle = new Rectangle(x, y, sideLength, sideLength);
    this.offColor = DEFAULT_OFF_COLOR;
    this.onColor = onColor;
    on = true;
  }
  
  public void collide(){
    if (toggle.contains(mouseX, mouseY)){
      on = !on;
    }
  }
  
  public void draw(){
    textFont(FONT);
    rectMode(CORNER);
    stroke(DEFAULT_OFF_COLOR);
    strokeWeight(1.5f);
    fill(on ? onColor : offColor);
    rect(toggle.x, toggle.y, toggle.width, toggle.height);
  }
}

  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#FFFFFF", "EU_Trade" });
  }
}
