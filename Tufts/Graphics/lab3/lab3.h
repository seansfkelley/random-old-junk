/*******************************************************
 *  Comp175 Fundamentals of Computer Graphics
 *  Name: your name here
 *  ID: last 4 digits of your Tufts id
 *  HW: 03
 ********************************************************/

#define _CRT_SECURE_NO_DEPRECATE
#define GLUT_BUILDING_LIB
#include <OpenGL/GL.h>
#include <glut/glut.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <list>
#include <algorithm>
#include <vector>
#include "matrix.h"
#include "raster.h"
#include "bitmapMetadata.h"

#define MAX(a,b) ((a)>(b)?(a):(b))
#define MIN(a,b) ((a)>(b)?(b):(a))

using namespace std;

// Struct to represent a 3D triangle with Texture coordinates
struct Triangle {
	Vector3D v0, v1, v2; // Triangle vertices in 3D
	Vector2D tex0, tex1, tex2; // Triangle texture coordinates for each vertex
};
struct Vertex {
    float x;
    float y;
};

// Structure representing the edge of a polygon.
// Contains the edge's two endpoints.
struct Edge {
    float x0;
    float y0;
    float x1;
    float y1;
};

// Data structure to implement the filling polygons
// algorithm. Structure represents an entry in the tables of
// active and inactive edges.
struct TblEdge {
    float ymax;
    float x; // If this edge is active, this represents the intersection with
			 // the current scan line. If this edge is inactive, it represents
			 // xmin.
    float revSlope;
};

static int gWidth, gHeight;
static int gLeft, gRight, gTop, gBottom;
static char *textureFile1;
static char *textureFile2;
Triangle gTriangle;
Matrix3D M;
FILE* gFp;
Vector3D gXaxis, gYaxis, gZaxis, gOrigin;

static Raster * gImage;
static Raster * gTexture1;
static Raster * gTexture2;

Color   gBackground = { 1.0, 1.0, 1.0 };

typedef list<TblEdge> EdgeList;
typedef EdgeList::iterator EdgeListIt;






/*******************************************************
 * FillTextureTriangle()
 * Fill triangle with the pattern corresponding to a
 * triangle region in the texture image.
 *   x0,y0	  -  First triangle vertex
 *   x1,y1	  -  Second triangle vertex
 *   x2,y2	  -  Third triangle vertex
 *   xt0,yt0  -  First point in texture image
 *   xt1,yt1  -  Second point in texture triangle
 *   xt2,yt2  -  Third point in texture triangle
 *   image 	  - Output image
 *   texImage - Texture to sample from
 ******************************************************/
void FillTextureTriangle(float x0, float y0,
						 float x1, float y1,
                         float x2, float y2,
						 float xt0, float yt0,
						 float xt1, float yt1,
						 float xt2, float yt2,
						 Raster* image, Raster* texImage);

////////////////////////////////////////////////////////////////////////////////
// Premade Functions .///
////////////////////////


/*******************************************************
 * init()
 * This function initializes the texture file name and
 * global triangle to default values.
 *******************************************************/
void init();

/*******************************************************
 * LineEquation()
 *
 * Compute the value of the implicit equation of the line
 * from (x0, y0) to (x1, y1) in point (xi, yi)
 *
 * (x0, y0), (x1, y1)  -  the two points defining the line
 * (xi, yi) - equation value is calculated for this point
 *******************************************************/
float LineEquation( float x0, float y0,
	    			float x1, float y1,
					float xi, float yi);

void FillPolygon(Edge *edgeArr, int nEdges, Color fill, Raster* image);
					
/*******************************************************
 *  getTriangleNormalVector()
 *
 * returns the normal vector of a triangle
 *
 *  Parameters:
 *  t - the triangle to examine
 *******************************************************/	
Vector3D getTriangleNormalVector(Triangle t);

/*******************************************************
 * void draw3D(char doWhat);	
 * Called within keyboard(); responsible for drawing
 * 3D triangle
 *******************************************************/
void draw3D(char doWhat);

void drawPolygon();

// Reads in a .bmp image and makes it readable for OpenGL
Raster *rtReadImage(char *filename);

void ClearImage(float *pixels, Color color);

void keyboard (unsigned char key, int x, int y);
void display (void);
					
////////////////////////////////////////////////////////////////////////////////
// Helper Functions .///
///////////////////////

// Switches order of verticies if needed
void ForceEdgeVertOrient(Edge *edge);

// Converts from edge data type to TblEdge
// Parameters:	edge: edge to be converted
//				newEdge: converted edge
int convertEdgetoTblEdge(Edge edge, TblEdge *newEdge);

// Calculates and sets x intercept
// Parameters:	TblEdge: edge whose x intercept we want
void setXintersect(TblEdge *edge);

// Calls setPixel for a given length
void fillSpan(int start, int stop, int scanline, Color c, Raster* image);

// Finds first stored sscanline with defined geometry
// Parameters:	scan2GEV: the height of GEV index for each scanline
//				height: height of target image
int getFirstScanline(int* scan2GEV, int height);

// Looks at the x (or y) val of each edge and returns true if x val of 1st edge 
// is less than the x (or y) val of the 2nd edge
bool SortByX (TblEdge &edge1, TblEdge &edge2);
bool SortByY (Edge* e1, Edge* e2);
