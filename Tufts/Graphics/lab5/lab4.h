#include <OpenGl/GL.h>
#include <glut/glut.h>
#include <stdlib.h>
#include "math3d.h"

#define PI 3.14159265

static GLfloat 	x=0.0f,y=10.75f,z=100.0f,
				lx=0.0f,ly=0.0f,lz=-1.0f, 
				angle=0.0f;

enum { RED, GREEN, BLUE, BLACK, WHITE, YELLOW, CYAN };
static M3DVector4f colors[7] = {{1.0,   0,   0, 1},    // R		 0
								{  0, 1.0,   0, 1},    // G		 1
								{  0,	0, 1.0, 1},    // B		 2
								{ .1,  .1,  .1, 1},    // Black	 3
								{1.0, 1.0, 1.0, 1},    // White  4
								{1.0, .937,   0, 1},   // Yellow 5
								{  0, .718, .662, 1}}; // Cyan	 6
static GLfloat	matGroundA[] = { 0.25f, 0.25f, 0.25f, 1.0f };
								
static GLfloat	light0Ambient[]  = {  1.0f,  1.0f,  1.0f, 0.5f},
	 		 	light0Diffuse[]  = {  0.5f,  0.5f,  0.5f, 0.5f},
 		 		light0Specular[] = {  1.0f,  1.0f,  1.0f, 0.5f };

static GLfloat shapeRotate = 0.0f;
static GLfloat xLightRot = 0.0f;
static GLfloat yLightRot = 0.0f;
static GLfloat zoomFactor = 45;
static GLfloat fAspect;

bool grid = true;

GLfloat left_rotate = 0.0f, right_rotate = 0.0f, leg_rotate = 0.0f;
GLfloat left_rot_amount = 2.5f, right_rot_amount = 2.5f, leg_rot_amount = 3.5f;
GLfloat MAX_LEG_ANGLE = 80.f;

GLUquadricObj* quadratic_cyl;
GLUquadricObj* quadratic_cyl2;


//=============================================================================
// Drawing Functions //
//==================//
void drawGround();
void drawSphere();
void drawCylinder();
void drawBox();
void drawTriangle();
void drawBounce();
void renderScene();

void drawChar();
void animation();

//=============================================================================
// Camera & Projection //
//====================//
void setProjection(int w, int h);
void cameraRotate(float angle);
void cameraWalk(int direction);
void cameraZoom (bool zoomIn);

//=============================================================================
// Standard Functions //
//===================//
void keyboard(unsigned char key, int x, int y);
void keyboard(int key, int x, int y);
void setup();
