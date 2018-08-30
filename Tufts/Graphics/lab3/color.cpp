#define GLUT_BUILDING_LIB
#include "color.h"

/*******************************************************
* Multiply two colors
*******************************************************/
Color Color::mul(Color c1, Color c2)
{
	Color c;
	c.r=c1.r*c2.r;
	c.g=c1.g*c2.g;
	c.b=c1.b*c2.b;
	return c;
}
/*******************************************************
* Scale a color by a constant
*******************************************************/
Color Color::mul(Color c1, float s)
{
	Color c;
	c.r = c1.r*s;
	c.g = c1.g*s;
	c.b = c1.b*s;
	return c;
}

/*******************************************************
* Add two colors
*******************************************************/
Color Color::sum(Color c1, Color c2)
{
	Color c;
	c.r = c1.r+c2.r;
	c.g = c1.g+c2.g;
	c.b = c2.b+c2.b;
	return c;
}