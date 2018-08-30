#include "raster.h"
#include <math.h>


/*******************************************************
 * Constructor
 *
 * Initialize an image with its width, height, and
 * bottom-left pixel position.
 *******************************************************/
Raster::Raster(int width, int height, int left, int bottom)
{
    this->width = width;
    this->height = height;
    this->left = left;
    this->right = width + left;
    this->bottom = bottom;
    this->top = height + bottom;
    this->pixels = new float[width * height * 3];
    this->foreground.r = 0.0f;
    this->foreground.g = 0.0f;
    this->foreground.b = 0.0f;
    this->background.r = 1.0f;
    this->background.g = 1.0f;
    this->background.b = 1.0f;
}

Raster::~Raster()
{
    delete this->pixels;
}


/*******************************************************
 * clear()
 *
 * Clear image with current background color
 *******************************************************/
void Raster::clear()
{
    int p = 0;
    int len = width * height * 3;
    while (p < len) {
        pixels[p++] = background.r;
        pixels[p++] = background.g;
        pixels[p++] = background.b;
    }
}


/*******************************************************
 * setPixel
 *
 * Sets a pixel in the raster to the given color.  Clips
 * any out-of-bounds coordinates.
 *
 * x,y	- Pixel Location
 * c	- Color to apply to pixel
 *******************************************************/
void Raster::setPixel(int x, int y, Color c)
{
    int p;
    if (x >= left && x < right && y >= bottom && y < top) {
        p = ((x-left) + (y-bottom) * width) * 3;
        pixels[p] = c.r;
        pixels[p+1] = c.g;
        pixels[p+2] = c.b;
    }
}


/*******************************************************
 * getPixel
 *
 * Returns the color of the pixel at coordinate (x, y)
 *******************************************************/
Color Raster::getPixel(int x, int y)
{
    Color result;
    int p;
    if (x >= left && x < right && y >= bottom && y < top) {
        p = ((x-left) + (y-bottom) * width) * 3;
        result.r = pixels[p];
        result.g = pixels[p+1];
        result.b = pixels[p+2];
    }
	else
	{
		result.r=0;
		result.g=0;
		result.b=0;
	}
    return result;
}

/*******************************************************
 * drawLine
 *
 * Draws a one-pixel wide line from (x0,y0) to (x1,y1)
 * using the midpoint line algorithm.
 *******************************************************/
void Raster::drawLine(float x0, float y0,
                      float x1, float y1)
{
   //----Always draw from left to right
   float t;
   if (x0 > x1) {
      t = x0; x0 = x1; x1 = t;
      t = y0; y0 = y1; y1 = t;
   }

   float dx = x1 - x0;
   float dy = y1 - y0;

   char ltype;

   //----Decide which case we're drawing and adjust
   //----coordinates accordingly

   //----CASE A: Slope between 0 and 1
   if (dy >= 0 && dx >= dy) {
      ltype = 'A';
   }

   //----CASE B: Slope greater than 1 (swap x and y coords)
   else if (dy >= 0 && dy > dx) {
      ltype = 'B';
      t = x0; x0 = y0; y0 = t;
      t = x1; x1 = y1; y1 = t;
      dx = x1 - x0;
      dy = y1 - y0;
   }

   //----CASE C: Slope between 0 and -1 (reflect y coord)
   else if (dy < 0 && dx >= -dy) {
      ltype = 'C';
      dy = -dy;
   }

   //----CASE D: Slope less than -1 (swap x,y and reflect y)
   else {
      ltype = 'D';
      t = x0; x0 = y1; y1 = t;
      t = x1; x1 = y0; y0 = t;
      dx = x1 - x0;
      dy = y0 - y1;
   }

   float d = 2 * dy - dx;
   float incrE = 2 * dy;
   float incrNE = 2 * (dy - dx);
   int sx = (int)(x0 + 0.5);
   int sy = (int)(y0 + 0.5);
   int x = sx;
   int y = sy;

   //----Render line
   while (x <= x1) {

      switch (ltype) {
      case 'A':   setPixel(x, y, foreground); break;
      case 'B':   setPixel(y, x, foreground); break;
      case 'C':   setPixel(x, 2 * sy - y, foreground); break;
      case 'D':   setPixel(2 * sy - y, x, foreground); break;
      }

      if (d <= 0) {
         d += incrE;
         x++;
      } else {
         d += incrNE;
         x++;
         y++;
      }
   }
}

/*******************************************************
 * averageColor
 *
 * Average the color in a rectangle in the image
 *
 * x0,y0  -  First rectangle vertex
 * x1,y1  -  Second rectangle vertex
 * x2,y2  -  Third rectangle vertex
 * x3,y3  -  Fourth rectangle vertex
 *******************************************************/
Color Raster::averageColor(float x0, float y0,float x1, float y1,
                           float x2, float y2, float x3, float y3)
{
//----You should have a working version of this function from homework 3 or 4
return BLACK;
}


/*******************************************************
 * getBoxSample
 *
 * Computes a 5x5 average of the pixels surrounding x,y
 *
 * x,y  -  Point to sample around
 *******************************************************/
Color Raster::getBoxSample(int x, int y) {
//----You should have a working version of this function from homework 3 or 4
return BLACK;
}