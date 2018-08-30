#ifndef MATRIX_H
#define MATRIX_H

#include "vector.h"

#define X    0   // X-Axis
#define Y    1   // Y-Axis
#define Z    2   // Z-Axis


/*******************************************************
 * Define a 3D matrix as an array of 16 floats.
 *
 *    |  0  1  2  3  |
 *    |  4  5  6  7  |
 *    |  8  9  10 11 |
 *    |  12 13 14 15 |
 *
 *******************************************************/
typedef float Matrix3D[16];  // 4x4 row-major matrix



/*******************************************************
 * mtxLoadIdentity()
 *
 * Resets the given matrix to the identity matrix
 *
 * T  -  Matrix to reset
 *******************************************************/
void mtxIdentity (Matrix3D T);



/*******************************************************
 * mtxMultiplyMM()
 * 
 * Multiply matrix A times matrix B.  The result
 * will be left in matrix B.
 *******************************************************/ 
void mtxMultiplyMM(Matrix3D A, Matrix3D B);



/*******************************************************
 *  Rotate the matrix about the given axis by the
 *  specified number of degrees
 *
 *  AXIS CODES
 *    0: x-axis
 *    1: y-axis
 *    2: z-axis
 *
 *******************************************************/
void mtxRotate (Matrix3D T, int axis, float deg);



/*******************************************************
 *  Translate the current matrix by the given amount
 *  in each direction
 *******************************************************/
void mtxTranslate (Matrix3D T, float x, float y, float z);



/*******************************************************
 *  Scale the given matrix by the specified amount  
 *******************************************************/
void mtxScale (Matrix3D M, float xs, float ys, float zs);



////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// You shouldn't have to touch functions below this point.

/*******************************************************
 * Apply orthographic projection from projection 
 * space to image space.
 *******************************************************/
void mtxOrthographic (Matrix3D M, float pxmin, float pxmax, 
			   float pymin, float pymax, float pzmin, float pzmax);

    
    
/*******************************************************
 *  Transform the given point by the specified matrix
 *******************************************************/
Vector3D mtxTransformPoint (Matrix3D T, Vector3D p);


/*******************************************************
 *  Transform the given point by the specified matrix
 *******************************************************/
void mtxTransformPoint (Matrix3D T, float p[3]);

#endif
