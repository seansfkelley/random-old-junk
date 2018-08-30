#include "lab4.h"
#include <iostream>
#include <algorithm>

//=============================================================================
// Name: Sean Kelley
// Operating System Used: OS X
// Any other instructions:
// Buttons 1, 2, 3 wave the arms; w makes him dance!
//
//=============================================================================

//=============================================================================
//
// What do you need to implement?
// 1. Your 3D character. A wrapper function has been created for you, though
//       making helper functions may simplify your debugging and is encouraged.
//       The name of the wrapper function is drawChar(). Note that the simple
//       animation is triggered by keypress. Look at keyboard() for information
//       Only one animation is required, but implementing more is encouraged.
// 2. cameraRotate(), cameraWalk() and cameraZoom() with a personal choice of 
//       rotation style, though this must be noted either in the function or in 
//       the header. Be detailed. If you have any questions ask early.
// 
//
//
// Useful and Important Information
// - Fill out the information header of this assignment.
// - If what you provide does not compile it will not be graded. Include any
//      necessary compilation instructions in the header, and be sure to 
//      specify above what operating system you are using.
// - Part of your grade will be based on code tidyness and style. Commenting
//      your code and muting all debug printf/cout statements on your 
//      submission version is essential. Failure to do either one will result 
//      in point deduction.
// - If you want to learn more about OpenGL or have questions, try looking in
//      The Red Book first, or The Super Bible. They are great resources.
//      (http://www.opengl.org/documentation/red_book/)
//
//=============================================================================



//=============================================================================
//
// Functions to be Implemented
//
//=============================================================================

void drawChar() {
    glMaterialfv(GL_FRONT, GL_AMBIENT, colors[CYAN]);
	glPushMatrix();
        glScalef(0.5f, 0.5f, 0.5f);

        // Get the height of the longest leg, then add 10 to it for the offset of the chest.
        GLfloat height = cos(std::min<GLfloat>(leg_rotate, 80 - leg_rotate) * PI / 180) * 2 * 20.f + 10.f;
        glTranslatef(0.f, height, 0.f);

        // Body
        glPushMatrix();
            glScalef(0.75f, 1.f, 0.5f);
		    glutSolidCube(20.f);
        glPopMatrix();

        // Head
        glPushMatrix();
            glTranslatef(0.f, 17.5f, 0.f);
            glutSolidSphere(7.5f, 25, 25);
        glPopMatrix();

        // Left Upper Arm
        glPushMatrix();
            glTranslatef(0.f, -30.f, 0.f);
            glRotatef(90.f, 0.f, 1.f, 0.f);

            glTranslatef(0.f, 35.f, 7.5f);
            glRotatef(left_rotate, 1.f, 0.f, 0.f);

            gluCylinder(quadratic_cyl, 2.5f, 2.5f, 15.0f, 20, 20);

            // Left Forearm
            glPushMatrix();
                glTranslatef(0.f, 0.f, 15.f);
                glRotatef(left_rotate, 1.f, 0.f, 0.f);

                gluCylinder(quadratic_cyl, 2.5f, 2.5f, 15.0f, 20, 20);
            glPopMatrix();
        glPopMatrix();

        // Right Upper Arm
        glPushMatrix();
            glTranslatef(0.f, -30.f, 0.f);
            glRotatef(270.f, 0.f, 1.f, 0.f);

            glTranslatef(0.f, 35.f, 7.5f);
            glRotatef(right_rotate, 1.f, 0.f, 0.f);

            gluCylinder(quadratic_cyl, 2.5f, 2.5f, 15.0f, 20, 20);

            // Right Forearm
            glPushMatrix();
                glTranslatef(0.f, 0.f, 15.f);
                glRotatef(right_rotate, 1.f, 0.f, 0.f);

                gluCylinder(quadratic_cyl, 2.5f, 2.5f, 15.0f, 20, 20);
            glPopMatrix();
        glPopMatrix();

        // Upper Legs
        glPushMatrix();
            glTranslatef(0.f, -30.f, 0.f);
            glRotatef(90.f, 1.f, 0.f, 0.f);

            glPushMatrix();
                // Left Leg
                glTranslatef(-3.75f, 0.f, -20.f);
                glRotatef(-leg_rotate, 1.f, 0.f, 0.f);
                gluCylinder(quadratic_cyl, 2.5f, 2.5f, 20.0f, 20, 20);

                // Lower Leg
                glPushMatrix();
                    glTranslatef(0.f, 0.f, 20.f);
                    glRotatef(2 * leg_rotate, 1.f, 0.f, 0.f);

                    gluCylinder(quadratic_cyl, 2.5f, 2.5f, 20.0f, 20, 20);
                glPopMatrix();
            glPopMatrix();

            glPushMatrix();
                // Right Leg
                glTranslatef(3.75f, 0.f, -20.f);
                glRotatef(leg_rotate - MAX_LEG_ANGLE, 1.f, 0.f, 0.f);
                gluCylinder(quadratic_cyl, 2.5f, 2.5f, 20.0f, 20, 20);

                // Lower Leg
                glPushMatrix();
                    glTranslatef(0.f, 0.f, 20.f);
                    glRotatef(-2 * (leg_rotate - MAX_LEG_ANGLE), 1.f, 0.f, 0.f);

                    gluCylinder(quadratic_cyl, 2.5f, 2.5f, 20.0f, 20, 20);
                glPopMatrix();
            glPopMatrix();
        glPopMatrix();
	glPopMatrix();
}

void animation() {
    // See notes in keyboard()
    ; 
}

// Rotates the camera in-place like a FPS 
void cameraRotate(float ang) {
    GLfloat tmp_x = lx - x, tmp_z = lz - z;
    GLfloat h = sqrt(tmp_x * tmp_x + tmp_z * tmp_z);
    lx = h * cos(ang - PI / 2) + x; lz = h * sin(ang - PI / 2) + z;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
}

void cameraWalk(int direction) {
    GLfloat tmp_x = x - lx, tmp_z = z - lz;
    GLfloat h = sqrt(tmp_x * tmp_x + tmp_z * tmp_z);
    tmp_x = 4 * direction * (tmp_x / h);
    tmp_z = 4 * direction * (tmp_z / h);
    x -= tmp_x;  z -= tmp_z;
    lx -= tmp_x; lz -= tmp_z;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
}


void cameraZoom(bool zoomIn) {
    zoomFactor += zoomIn ? 0.5f : -0.5f;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
}


//=============================================================================
//
// Drawing Functions
//
//=============================================================================


void drawGround () {
	glMaterialfv(GL_FRONT, GL_AMBIENT, matGroundA);
	glBegin(GL_QUADS);
		glColor3fv(colors[BLACK]);
        glVertex3f( 600.0f, -1, -600.0f);
        glVertex3f(-600.0f, -1, -600.0f);
        glVertex3f(-600.0f, -1,  600.0f);
        glVertex3f( 600.0f, -1,  600.0f);
    glEnd();
	if(grid) {
		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLACK]);
		for (int i = -600; i < 600; i+=100) {
			glBegin(GL_LINES);
				glVertex3f(i, 0, -600.f);
				glVertex3f(i, 0,  600.f);
			glEnd();
		}
		for (int i = -600; i < 600; i+=100) {
			glBegin(GL_LINES);
				glVertex3f(-600, 0, i);
				glVertex3f(600, 0, i);
			glEnd();
		}
	}
}

void drawSphere () {
	glPushMatrix();
		glTranslatef(0.0f, 30.0f, 0.0f);
		// Axis lines
		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[WHITE]);
		glBegin(GL_LINES);
			glColor3fv(colors[YELLOW]);
			glVertex3f(-30.0f,   0.0f, 0.0f);
			glVertex3f( 30.0f,   0.0f, 0.0f);
		glEnd();glBegin(GL_LINES);
			glColor3fv(colors[YELLOW]);
			glVertex3f(  0.0f, -30.0f, 0.0f);
			glVertex3f(  0.0f,  30.0f, 0.0f);
		glEnd();glBegin(GL_LINES);
			glColor3fv(colors[YELLOW]);
			glVertex3f(  0.0f, 0.0f, -30.0f);
			glVertex3f(  0.0f, 0.0f,  30.0f);
		glEnd();
	
		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLUE]);
		glutSolidSphere (25.0, 25, 25);
	glPopMatrix();
}

void drawCylinder () {
	glPushMatrix();
		glPushMatrix();
			glTranslatef(50.0f, 25.0f, 0.0f);
			// Axis lines
			glMaterialfv(GL_FRONT, GL_AMBIENT, colors[WHITE]);
			glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(-20.0f,   0.0f, 0.0f);
				glVertex3f( 20.0f,   0.0f, 0.0f);
			glEnd();glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(  0.0f, -20.0f, 0.0f);
				glVertex3f(  0.0f,  20.0f, 0.0f);
			glEnd();glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(  0.0f, 0.0f, -20.0f);
				glVertex3f(  0.0f, 0.0f,  20.0f);
			glEnd();
		glPopMatrix();
	
		glTranslatef(50.0f, 40.0f, 0.0f);
		glRotatef(90, 0.f, 0.f, 0.f);
		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[GREEN]);
		gluCylinder (quadratic_cyl, 10.0f, 10.0f, 30.0f, 20, 20);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(70.0f, 20.0f, 0.0f);
		glRotatef(45, 0.5f, 0.5f, 0.5f);
	
		glPushMatrix();
			// Axis lines
			glTranslatef(0.f, 0.f, 15.0f);
			glMaterialfv(GL_FRONT, GL_AMBIENT, colors[WHITE]);
			glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(-20.0f,   0.0f, 0.0f);
				glVertex3f( 20.0f,   0.0f, 0.0f);
			glEnd();glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(  0.0f, -30.0f, 0.0f);
				glVertex3f(  0.0f,  30.0f, 0.0f);
			glEnd();glBegin(GL_LINES);
				glColor3fv(colors[YELLOW]);
				glVertex3f(  0.0f, 0.0f, -20.0f);
				glVertex3f(  0.0f, 0.0f,  20.0f);
			glEnd();
		glPopMatrix();

		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLACK]);
		gluCylinder (quadratic_cyl, 10.0f, 10.0f, 30.0f, 20, 20);
	glPopMatrix();
}

void drawBox() {
	glMaterialfv(GL_FRONT, GL_AMBIENT, colors[RED]);
	glPushMatrix();
		glTranslatef(-40.f, 10.f, 0.f);
		glutSolidCube(20.f);
	glPopMatrix();
}

void drawTriangle() {
	GLfloat top[]  = { -65.0f, 15.0f, 0.f },
			botl[] = { -75.0f,  5.0f, 0.f },
			botr[] = { -55.0f,  5.0f, 0.f };
	glBegin(GL_TRIANGLES);
		glVertex3fv(top);
		glVertex3fv(botl);
		glVertex3fv(botr);
	glEnd();
}

void drawBounce() {
	glPushMatrix();
		glTranslatef(-100, 50, 0);
		glRotatef(shapeRotate, 1., 0., 0.);
		glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLACK]);
		glutSolidCube(20.f);
	
		glPushMatrix();
			float move = sin(shapeRotate)*15;
			glTranslatef(0, 0, 30+move);
			glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLACK]);
			glutSolidSphere (10.0, 25, 25);
		glPopMatrix();
	glPopMatrix();
}

void renderScene () {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	
    drawGround();

	drawChar();
	
	glutSwapBuffers();
}


//=============================================================================
//
// Camera and Projection Functions
//
//=============================================================================


void setProjection (int w, int h) {
	glViewport(0, 0, w, h);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
	
	fAspect = (GLfloat) w / (GLfloat) h;
	gluPerspective(zoomFactor, fAspect, 1.0f, 10000.0f);

	gluLookAt(x, y, z, lx, ly, lz, 0.0f,1.0f,0.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

//=============================================================================
//
// Keyboard & Setup Functions
//
//=============================================================================


void keyboard(int key, int x, int y) {
	
	switch (key) {
		case GLUT_KEY_LEFT : 
			angle -= 0.10f;
			cameraRotate(angle);break;
		case GLUT_KEY_RIGHT : 
			angle += 0.10f;
			cameraRotate(angle);break;
		case GLUT_KEY_UP : 
			cameraWalk(1);break;
		case GLUT_KEY_DOWN : 
			cameraWalk(-1);break;
	}
	glutPostRedisplay();
}

inline void rotateAppendage(GLfloat &arm_rotate, GLfloat &arm_rot_amount, const float min, const float max){
    arm_rotate += arm_rot_amount;
    if (arm_rotate < min){
        arm_rotate = min;
        arm_rot_amount = -arm_rot_amount;
    }
    else if (arm_rotate > max){
        arm_rotate = max;
        arm_rot_amount = -arm_rot_amount;
    }
}

void keyboard (unsigned char key, int x, int y) {
	switch(key) {
    // Increased the zoom range!
    case 'z': 
        if(zoomFactor<64) {
            cameraZoom(true);	
        } break;
    case 'x': 
        if(zoomFactor>32) {
            cameraZoom(false);
        } break;
		
        // Found it to be easier to map specific changes to each key rather export it
        // to a single-button animation function.
    case '1':
        rotateAppendage(left_rotate, left_rot_amount, -60.f, 45.f);
        break;

    case '2':
        rotateAppendage(left_rotate, left_rot_amount, -60.f, 45.f);
        rotateAppendage(right_rotate, right_rot_amount, -60.f, 45.f);
        break;

    case '3':
        rotateAppendage(right_rotate, right_rot_amount, -60.f, 45.f);
        break;

    case 'w':
        rotateAppendage(leg_rotate, leg_rot_amount, 0.f, 80.f);
        break;

    case 'q' :
    case 'Q' :
        exit(0);
	}
	glutPostRedisplay();
}

void setup () {
	//=========================================================================
	// Basic Setup  //
	//=============//
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glFrontFace(GL_CCW);
	
	//=========================================================================
	// Lights and lighting  //
	//=====================//
	glLightfv(GL_LIGHT0, GL_AMBIENT, light0Ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light0Diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, light0Specular);
	glEnable(GL_LIGHT0);
	
	glEnable(GL_LIGHTING);
	glEnable(GL_DEPTH_TEST);

	
	//=========================================================================
	// Materials //
	//==========//
	glShadeModel(GL_SMOOTH);
	
	//=========================================================================
	// Misc. Calls  //
	//=============//
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f );

	// Create memory for primatives
	quadratic_cyl=gluNewQuadric();
	quadratic_cyl2=gluNewQuadric();
}

int main(int argc, char* argv[]) {	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
    glutInitWindowSize(800,600);
	glutCreateWindow("Lab 4");
	
	glutReshapeFunc(setProjection);
	glutDisplayFunc(renderScene);
	glutKeyboardFunc(keyboard);
	glutSpecialFunc(keyboard);
	setup();
	glutMainLoop();
	
	return 0;
}
