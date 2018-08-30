final PFont FONT = createFont("GillSans", 12);

final int SIZE_X = 650, SIZE_Y = 725;
final int MAP_OFFSET_X = 25, MAP_OFFSET_Y = 25, BORDER_WIDTH = 2;
final int TOGGLE_WIDTH = 20, TOGGLE_SPACE = 8, TOGGLE_X = 64, TOGGLE_Y = SIZE_Y - TOGGLE_WIDTH * 2 - TOGGLE_SPACE - 16;

final color DEFAULT_TEXT_COLOR = #000000,
            BORDER_COLOR = #888888,
            BACKGROUND_COLOR = #FFFFFF,
            SORT_TOGGLE_COLOR = #1100CC;

final color[] TYPE_COLORS = {#DB0000, #FE5C5C, #11772D, #3ED715};

boolean togglesOn = true, sliding = false;
int displayYear = 0;

PImage mapBackground, units, source;
Country[] countries;
int highlightedIndex = -1, numYears;
ToggleBox[] toggles;
ToggleBox sortToggle;
HorizontalSlider slider;

void setup(){
  size(650, 725);
  textFont(FONT);
  mapBackground = loadImage("EU Map.png");
  loadData();
  smooth();
}

void loadData(){
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

void draw(){
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

void mouseMoved(){
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

void mousePressed(){
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

void mouseDragged(){
  if (sliding){
    slider.move();
    displayYear = slider.getValue();
  }
}
