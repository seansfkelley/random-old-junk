#ifndef RASTER_H
#define RASTER_H

/*******************************************************
 * Define a Color as a R,G,B triplet
 *******************************************************/
typedef struct {
    float r;
    float g;
    float b;
} Color;


/*******************************************************
 * Set up some basic colors
 *******************************************************/
const Color BLACK   = { 0.0, 0.0, 0.0 };
const Color WHITE   = { 1.0, 1.0, 1.0 };
const Color RED     = { 1.0, 0.0, 0.0 };
const Color GREEN   = { 0.0, 1.0, 0.0 };
const Color BLUE    = { 0.0, 0.0, 1.0 };
const Color CYAN    = { 0.0, 1.0, 1.0 };
const Color MAGENTA = { 1.0, 0.0, 1.0 };
const Color YELLOW  = { 1.0, 1.0, 0.0 };
const Color GRAY    = { 0.5, 0.5, 0.5 };


/*******************************************************
 * class Raster
 * 
 * Encapsulates an array of pixel data.  Provides
 * methods for reading and writing pixels as well as
 * rendering basic 2D primitives. 
 *******************************************************/
class Raster {

   
protected:
   
   // Image dimensions
   int width;
   int height;
   int left;
   int right;
   int top;
   int bottom;

   // Pixel data
   float * pixels;

   // Current foreground and background colors
   Color foreground;
   Color background;

   
public:

    Raster(int width, int height, int left, int bottom);
    ~Raster();

   
    int     getWidth()  { return this->width; }
    int     getHeight() { return this->height; }
    int     getLeft()   { return this->left; }
    int     getBottom() { return this->bottom; }
    int     getRight()  { return this->right; }
    int     getTop()    { return this->top; }
    float * getPixels() { return this->pixels; }
    void    setBackground(Color bg) { this->background = bg; }
    void    setForeground(Color fg) { this->foreground = fg; }
    Color   getBackground() { return this->background; }
    Color   getForeground() { return this->foreground; }

    void    clear();
    void    setPixel(int x, int y, Color c);
    Color   getPixel(int x, int y);

	void drawLine(float x0, float y0,
			  float x1, float y1);

    Color getBoxSample(int x, int y);

	Color averageColor(float x0, float y0,float x1, float y1,
                       float x2, float y2, float x3, float y3);
};

#endif
