color SLIDER_BORDER_COLOR = #000000,
      SLIDER_FILL_COLOR = #FFFFFF,
      SLIDER_LINE_COLOR = #000000,
      SLIDER_TEXT_COLOR = #000000;

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
    strokeWeight(1.5);
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

