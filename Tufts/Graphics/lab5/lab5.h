#include <OpenGl/GL.h>
#include <glut/glut.h>
#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include "math3d.h"

#define PI 3.14159265

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
void keyboard(unsigned int key, int x, int y);
void SpecialKeys(int key, int x, int y);
void setup();
