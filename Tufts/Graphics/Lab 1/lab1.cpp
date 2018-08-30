/*******************************************************
 *  Comp175 Fundamentals of Computer Graphics
 *  Name: Sean Kelley
 *  ID: 4120
 *  HW: 1
 *  Note: I changed the math3d import path.
 ********************************************************/

#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <Glut/glut.h>
#include "math3d.h"
#include <cstdlib>
#include <ctime>
#include <cmath>

GLint WIDTH = 640, HEIGHT = 480, mouse_x, mouse_y;
GLfloat *image, *small_image;
bool draw_small_image;

inline GLfloat random0_1(){
    return (1.0 * rand()) / RAND_MAX;
}

inline GLfloat dist_to_center(int x, int y){
    return sqrt(pow(WIDTH / 2 - x, 2) + pow(HEIGHT / 2 - y, 2));
}

/*******************************************************
 *  void display(void)
 *
 *  GLUT window-repainting callback. Put all code in here
 *  that you need to paint your image.
 *******************************************************/
void display (void)
{
	//----Tell openGL that the pixels are sequential (ie
	//----they were not aligned on certain boundaries when
	//----written to memory)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

	//-----Clear the background
	glClear(GL_COLOR_BUFFER_BIT);

	//----Draw the pixels to our window, startin at location
	//----(0,0).
	glRasterPos2i(0, 0);

	glDrawPixels(WIDTH, HEIGHT, GL_RGB, GL_FLOAT, image);

    if (draw_small_image){
        glRasterPos2i(mouse_x - 10, HEIGHT - mouse_y - 10);
        glDrawPixels(20, 20, GL_RGB, GL_FLOAT, small_image);
    }

	//----Draw any information left in the buffer
	glFlush();
}


/*******************************************************
 *  motion
 *
 *  Callback function called by GLUT when the mouse is moved
 *  inside the window.
 *
 *  Parameters:
 *  x, y - Mouse position
 *******************************************************/
void motion ( int x, int y )
{
    mouse_x = x;
    mouse_y = y;

    // Set the small image as an inverse of whatever it's drawn above.
    for (int small_image_x = 0; small_image_x < 20; ++small_image_x){
        for (int small_image_y = 0; small_image_y < 20; ++small_image_y){
            int first = 3 * (small_image_y * 20 + small_image_x);
            int image_x = x - 10 + small_image_x, image_y = HEIGHT - y - 10 + small_image_y;
            int image_first = 3 * (image_y * WIDTH + image_x);

            small_image[first] = 1.0f - image[image_first];
            small_image[first + 1] = 1.0f - image[image_first + 1];
            small_image[first + 2] = 1.0f - image[image_first + 2];
        }
    }

	//----display animation
	glutPostRedisplay();
}

/********************************************************************
 *  keyboard
 *
 * Callback function called by GLUT when a key is pressed.
 *
 *  Parameters:
 *  key - The key pressed.
 *  x, y - Mouse position when the key is pressed.
 *******************************************************/
void keyboard (unsigned char key, int x, int y)
{

	//----disable mouse callback function
	glutPassiveMotionFunc(NULL);
    draw_small_image = false;

	switch (key)
	{
	//----Close the window
	case 'q':
	case 'Q':
	case 'x':
	case 'X':
		exit(0);

	//----Fill the image with a single color
	case '1':
        {
            GLfloat r = random0_1(), g = random0_1(), b = random0_1();
            int px_components = WIDTH * HEIGHT * 3;

            for (int i = 0; i < px_components; i += 3){
                image[i] = r;
                image[i + 1] = g;
                image[i + 2] = b;
            }

            break;
        }


	//----Fill the image with a left-to-right color gradient
	case '2':
        {
            GLfloat r = random0_1(), g = random0_1(), b = random0_1(),
                    dr = (random0_1() - r) / WIDTH, dg = (random0_1() - g) / WIDTH, db = (random0_1() - b) / WIDTH;

            for (int x = 0; x < WIDTH; ++x){
                for (int y = 0; y < HEIGHT; ++y){
                    int first = 3 * (y * WIDTH + x);
                    image[first] = r;
                    image[first + 1] = g;
                    image[first + 2] = b;
                }
                r += dr;
                g += dg;
                b += db;
            }

            break;
        }

	//----Fill the image with a function
	case '3':
        {
            GLfloat max_dist = sqrt(WIDTH * WIDTH / 4.0 + HEIGHT * HEIGHT / 4.0);

            GLfloat cr = random0_1(), cg = random0_1(), cb = random0_1(),
                    dr = (random0_1() - cr) / max_dist, dg = (random0_1() - cg) / max_dist, db = (random0_1() - cb) / max_dist;

            for (int x = 0; x < WIDTH; ++x){
                for (int y = 0; y < HEIGHT; ++y){
                    int first = 3 * (y * WIDTH + x);
                    GLfloat dist = dist_to_center(x, y);
                    image[first] = cr + dr * dist;
                    image[first + 1] = cg + dg * dist;
                    image[first + 2] = cb + db * dist;
                }
            }

            break;
        }


	//----Create animation.
	case '4':
        draw_small_image = true;

		glutPassiveMotionFunc(motion);
		motion(x,y);
		break;

	}

	glutPostRedisplay();
}



/*******************************************************
 *  main
 *
 *  Main entry point for this program.
 *  main will
 *   1. Initialize your GLUT window and data
 *   2. Set up callbacks
 *   3. Enter the main event loop.
 *******************************************************/
int main (int argc, char* argv[])
{
 	glutInit(&argc, argv);
	//----Tell GLUT to use a single buffer with three color channels
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

	glutInitWindowSize(WIDTH, HEIGHT);
    glutInitWindowPosition(-1, -1); // Doesn't really matter...
    glutCreateWindow("COLARS");

	//----Set background color
	glClearColor(0.0f, 0.0f, 0.0f, 1.f);

	//----Set viewing window
	glViewport(0, 0, (GLsizei) WIDTH, (GLsizei) HEIGHT);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho (0.0, WIDTH, 0.0, HEIGHT, -1.0, 1.0);
	glMatrixMode(GL_MODELVIEW);

    // For random color picking!
    srand(time(NULL));
    image = new GLfloat[WIDTH * HEIGHT * 3];
    small_image = new GLfloat[20 * 20 * 3];

	//----Tell GLUT about the display callback functions --
	//----this let's GLUT know what function to call in order
	//----to redraw (we are passing a pointer to the function
	//----display().)
	glutDisplayFunc (display);
	glutKeyboardFunc (keyboard);

	//----Enter the GLUT event loop.
	glutMainLoop();


	//----Exit
	return 0;
}

