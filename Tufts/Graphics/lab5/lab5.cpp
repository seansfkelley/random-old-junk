#include "lab5.h"

static GLfloat 	x=0.0f,y=1.75f,z=200.0f,
		lx=0.0f,ly=0.0f,lz=-1.0f, 
		angle=0.0f, lightAngle=0.0f;

enum { RED, GREEN, BLUE, BLACK, YELLOW, CYAN };
static M3DVector3f colors[7] = {{255,   0,   0},  // R		0
				{  0, 255,   0},  // G		1
				{  0,	0, 255},  // B		2
				{ 25,  25,  25},  // Black	3
				{255, 239,   0},  // Yellow	4
                {  0, 183, 235}}; // Cyan	5

enum {PLASTIC_DIFFUSE, PLASTIC_SPECULAR, METAL_DIFFUSE, METAL_SPECULAR};
static float materials[4][3] = {
    { 1.0f,  0.25f,  0.25f},
    { 1.0f,   1.0f,   1.0f},
    {0.35f,  0.35f,  0.45f},
    { 0.8f,    0.8f,  1.0f}
};
								
static GLfloat	light0Ambient[]  = {  1.0f,  1.0f,  1.0f, 0.25f },

				light1Ambient[]  = {  0.25f,  0.25f,  0.75f, 0.75f},
		 		light1Diffuse[]  = {  0.25f,  0.25f,  0.75f, 0.75f},
		 		light1Specular[] = {  0.25f,  0.25f,  0.75f, 0.25f},
                light1Position[] = {  0.0f,  0.0f, 90.0f, 1.0f },

				light2Ambient[]  = {  0.25f,  0.75f,  0.25f, 0.75f},
                light2Diffuse[]  = {  0.25f,  0.75f,  0.25f, 0.75f},
                light2Specular[] = {  0.25f,  0.75f,  0.25f, 0.25f},
                light2Position[] = {  0.0f,  50.0f, 0.0f, 1.0f },

                light3Ambient[]  = {  0.75f,  0.75f,  0.75f, 0.75f},
                light3Diffuse[]  = {  0.75f,  0.75f,  0.75f, 0.75f},
		 		light3Specular[] = {  0.75f,  0.75f,  0.75f, 0.25f},
                light3Position[] = {     x,     y,     z, 1.0f },
                light3Direction[] = { 0.0f,  0.0f, -1.0f};

static GLfloat shapeRotate = 0.0f;
static GLfloat xLightRot = 0.0f;
static GLfloat yLightRot = 0.0f;
static GLfloat zoomFactor = 45;
static GLfloat fAspect;

static GLfloat left_rotate = 0.0f, right_rotate = 0.0f, leg_rotate = 0.0f;
static GLfloat left_rot_amount = 2.5f, right_rot_amount = 2.5f, leg_rot_amount = 3.5f;
static GLfloat MAX_LEG_ANGLE = 80.f;

static GLfloat  matGroundA[] = { 0.25f, 0.25f, 0.25f, 1.0f };

bool grid = true;

GLUquadricObj* quadratic_cyl;

//=============================================================================

void drawGround () {
	//						R		G	B		A
   	GLfloat matQuadAmb[] = {0.0f, 0.0f, 0.0f, 1.0f};
	//http://www.opengl.org/sdk/docs/man/xhtml/glMaterial.xml
	//			  face,    light kind, material color
	glMaterialfv(GL_FRONT, GL_AMBIENT, matQuadAmb);
	glBegin(GL_QUADS);
	glColor3fv(colors[BLACK]);
        glVertex3f( 600.0f, -100, -600.0f);
        glVertex3f(-600.0f, -100, -600.0f);
        glVertex3f(-600.0f, -100,  600.0f);
        glVertex3f( 600.0f, -100,  600.0f);
    glEnd();
}

void drawSphere () {
	GLfloat matSphereAmb[] = {1.0f, 0.0f, 0.0f, 1.0f},
			matLinesAmb[]  = {0.5f, 0.5f, 0.5f, 1.0f};
	//http://www.opengl.org/sdk/docs/man/xhtml/glMaterial.xml
	//			  face,    light kind, material color
	glMaterialfv(GL_FRONT, GL_AMBIENT, matLinesAmb);
	// Axis lines
	glBegin(GL_LINES);
		glColor3fv(colors[YELLOW]);
		glVertex3f(-60.0f,   0.0f, 0.0f);
		glVertex3f( 60.0f,   0.0f, 0.0f);
	glEnd();glBegin(GL_LINES);
		glColor3fv(colors[YELLOW]);
		glVertex3f(  0.0f, -60.0f, 0.0f);
		glVertex3f(  0.0f,  60.0f, 0.0f);
	glEnd();glBegin(GL_LINES);
		glColor3fv(colors[YELLOW]);
		glVertex3f(  0.0f, 0.0f, -60.0f);
		glVertex3f(  0.0f, 0.0f,  60.0f);
	glEnd();
	
	glMaterialfv(GL_FRONT, GL_AMBIENT, matSphereAmb);
	glutSolidSphere (40.0, 40, 40);
}

void drawChar() {
	glPushMatrix();
    // glScalef(0.5f, 0.5f, 0.5f);
        glTranslatef(0.0f, -50.0f, 0.0f);

        // Get the height of the longest leg, then add 10 to it for the offset of the chest.
        GLfloat height = cos(std::min<GLfloat>(leg_rotate, 80 - leg_rotate) * PI / 180) * 2 * 20.f + 10.f;
        glTranslatef(0.f, height, 0.f);

        glMaterialfv(GL_FRONT, GL_AMBIENT, materials[METAL_DIFFUSE]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, materials[METAL_DIFFUSE]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, materials[METAL_SPECULAR]);
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
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, materials[PLASTIC_DIFFUSE]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, materials[PLASTIC_DIFFUSE]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, materials[PLASTIC_SPECULAR]);
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

void renderScene () {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMaterialfv(GL_FRONT, GL_AMBIENT, colors[BLUE]);
	
	// BEGIN movable lighting
	glPushMatrix();	
        // Rotate coordinate system
        glRotatef(yLightRot, 0.0f, 1.0f, 0.0f);
        glRotatef(xLightRot, 1.0f, 0.0f, 0.0f);
        // Specify new position and direction in rotated coords.
        glLightfv(GL_LIGHT1,GL_POSITION,light1Position);
        glColor3ub(255,0,0);	
        // Translate origin to move the cone out to where the light
        // is positioned.
        glTranslatef(light1Position[0],light1Position[1],light1Position[2]);
        glutSolidCone(4.0f,6.0f,15,15);
        glPushAttrib(GL_LIGHTING_BIT);
        	glDisable(GL_LIGHTING);
        	glColor3ub(255,255,0);
        	glutSolidSphere(3.0f, 15, 15);
        glPopAttrib();
	// Restore rotation settings, etc. before the push
	glPopMatrix();
	// END movable lighting

	glPushMatrix();	
        glLightfv(GL_LIGHT2, GL_POSITION, light2Position);

        glColor3ub(255,0,0);
        glTranslatef(light2Position[0], light2Position[1], light2Position[2]);
        glRotatef(270.0f, 1.0f, 0.0f, 0.0f);
        glutSolidCone(4.0f,6.0f,15,15);

        glPushAttrib(GL_LIGHTING_BIT);
        	glDisable(GL_LIGHTING);
        	glColor3ub(255,255,0);
        	glutSolidSphere(3.0f, 15, 15);
        glPopAttrib();

    glPopMatrix();

	drawGround();
    drawChar();
	glutSwapBuffers();
}

void changeSize (int w, int h) {
	glViewport(0, 0, w, h);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	
	GLfloat fAspect = (GLfloat) w / (GLfloat) h;
	gluPerspective(45.0f, fAspect, 1.0f, 1000.0f);

	gluLookAt(x, y, z, x + lx,y + ly,z + lz, 0.0f,1.0f,0.0f);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
}

void setup () {
	//-------------------------------------------------------------------------
	// Basic Enabling
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glFrontFace(GL_CCW);
    glEnable(GL_NORMALIZE); //normalize transformed normals to be of unit length
	
	//-------------------------------------------------------------------------
	// Lights & Lighting
	
	// Light 0 ----------------------------------------------------------------

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0Ambient);
	
	// Light 1 ----------------------------------------------------------------

	glLightfv(GL_LIGHT1, GL_AMBIENT, light1Ambient);
	glLightfv(GL_LIGHT1, GL_DIFFUSE, light1Diffuse);
	glLightfv(GL_LIGHT1, GL_SPECULAR, light1Specular);
	glLightfv(GL_LIGHT1, GL_POSITION, light1Position);
	glEnable(GL_LIGHT1);

	glLightfv(GL_LIGHT2, GL_AMBIENT, light2Ambient);
	glLightfv(GL_LIGHT2, GL_DIFFUSE, light2Diffuse);
	glLightfv(GL_LIGHT2, GL_SPECULAR, light2Specular);
	glLightfv(GL_LIGHT2, GL_POSITION, light2Position);
	glEnable(GL_LIGHT2);

	glLightfv(GL_LIGHT3, GL_AMBIENT, light3Ambient);
	glLightfv(GL_LIGHT3, GL_DIFFUSE, light3Diffuse);
	glLightfv(GL_LIGHT3, GL_SPECULAR, light3Specular);
	glLightfv(GL_LIGHT3, GL_POSITION, light3Position);
    glLightf (GL_LIGHT3, GL_SPOT_CUTOFF, 5.0f);
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, light3Direction);
	glEnable(GL_LIGHT3);

	// Enable Lighting & Depth
	glEnable(GL_LIGHTING);
	glEnable(GL_DEPTH_TEST);
	
	//-------------------------------------------------------------------------
	// Materials
	glShadeModel(GL_SMOOTH);
	
	//-------------------------------------------------------------------------
	// Misc. Setup Calls
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f );

    quadratic_cyl = gluNewQuadric();
}

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

void cameraZoom(bool zoomIn) {
    zoomFactor += zoomIn ? 0.5f : -0.5f;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
}

void cameraRotate(float ang) {
    GLfloat tmp_x = lx - x, tmp_z = lz - z;
    GLfloat h = sqrt(tmp_x * tmp_x + tmp_z * tmp_z);
    lx = h * cos(ang - PI / 2) + x; lz = h * sin(ang - PI / 2) + z;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
    
    light3Direction[0] = lx - x;
    light3Direction[1] = 0.0f;
    light3Direction[2] = lz - z;

    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, light3Direction);
}

void cameraWalk(int direction) {
    GLfloat tmp_x = x - lx, tmp_z = z - lz;
    GLfloat h = sqrt(tmp_x * tmp_x + tmp_z * tmp_z);
    tmp_x = 4 * direction * (tmp_x / h);
    tmp_z = 4 * direction * (tmp_z / h);
    x -= tmp_x;  z -= tmp_z;
    lx -= tmp_x; lz -= tmp_z;
    setProjection(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT));
    
    light3Position[0] = x;
    light3Position[1] = y;
    light3Position[2] = z;
    
    glLightfv(GL_LIGHT3, GL_POSITION, light3Position);
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

// Had to twiddle with which types of input each keyboard function operates on to
// get them to work as intended. Also flipped the direction of the initial light's
// up/down movement.
void keyboard(unsigned char key, int x, int y) {
	switch (key) {
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

    case '4':
        rotateAppendage(leg_rotate, leg_rot_amount, 0.f, 80.f);
        break;

    case 'i': 
        xLightRot-=5.0f;
        break;
        
    case 'k':
        xLightRot+=5.0f;
        break;
    
    case 'j':
        yLightRot-=5.0f;
        break;

    case 'l':
        yLightRot+=5.0f;
        break;

    case 'w': 
        light2Position[2] -= 5.0f;
        break;
        
    case 'a':
        light2Position[0] -= 5.0f;
        break;
    
    case 's':
        light2Position[2] += 5.0f;
        break;

    case 'd':
        light2Position[0] += 5.0f;
        break;

    case 'q' :
    case 'Q' :
        exit(0);
	}
	glutPostRedisplay();
}

void SpecialKeys(int key, int x, int y) {
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

int main(int argc, char* argv[]) {	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
    glutInitWindowSize(800,600);
	glutCreateWindow("Lab 5");
	
	glutReshapeFunc(changeSize);
	glutDisplayFunc(renderScene);
	glutKeyboardFunc(keyboard);
	glutSpecialFunc(SpecialKeys);
	setup();
	glutMainLoop();
	
	return 0;
}
