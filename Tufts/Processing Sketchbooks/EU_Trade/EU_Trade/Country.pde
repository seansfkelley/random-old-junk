static final int EU = 0, WORLD = 1, IMPORT = 0, EXPORT = 2,
                 TEXT_BIAS_X = 2, TEXT_BIAS_Y = 2,
                 TEXT_BOX_BORDER = 4;
static final float MAX_AREA = 1024,
                   MIN_COLLIDE_DIST = 10;

color BOX_EDGE_COLOR = #000000,
      BOX_FILL_COLOR = #FFFFFF,
      COUNTRY_TEXT_COLOR = #000000;

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
