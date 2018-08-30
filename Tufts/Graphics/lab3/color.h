#ifndef COLOR_H
#define COLOR_H

#define GLUT_BUILDING_LIB
/*******************************************************
 * Define a Color as a R,G,B triplet
 *******************************************************/
class Color {
public:
    float r;
    float g;
    float b;

	/*******************************************************
	* Multiply two colors
	*******************************************************/
	static Color mul(Color c1, Color c2);
	/*******************************************************
	* Scale a color by a constant
	*******************************************************/
	static Color mul(Color c1, float s);
	/*******************************************************
	* Add two colors
	*******************************************************/
	static Color sum(Color c1, Color c2);
	
};


/*******************************************************
 * Set up some basic colors
 *******************************************************/
//const Color BLACK   = { 0.0, 0.0, 0.0 };
//const Color WHITE   = { 1.0, 1.0, 1.0 };
//const Color RED     = { 1.0, 0.0, 0.0 };
//const Color GREEN   = { 0.0, 1.0, 0.0 };
//const Color BLUE    = { 0.0, 0.0, 1.0 };
//const Color CYAN    = { 0.0, 1.0, 1.0 };
//const Color MAGENTA = { 1.0, 0.0, 1.0 };
//const Color YELLOW  = { 1.0, 1.0, 0.0 };
//const Color GRAY    = { 0.5, 0.5, 0.5 };

#endif