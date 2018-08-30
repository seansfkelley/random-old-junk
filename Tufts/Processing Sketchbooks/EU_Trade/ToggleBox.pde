color DEFAULT_OFF_COLOR = #777777;

public class ToggleBox{
  color offColor, onColor;
  Rectangle toggle;
  boolean on;
  
  public ToggleBox(int x, int y, int sideLength, color onColor){
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
    strokeWeight(1.5);
    fill(on ? onColor : offColor);
    rect(toggle.x, toggle.y, toggle.width, toggle.height);
  }
}
