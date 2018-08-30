#include "matrix.h"
#include <math.h>

#define PI 3.14159265

const float DEG_TO_RAD = PI / 180;



/*******************************************************
 *  Load the identity matrix
 *******************************************************/
void mtxIdentity(Matrix3D T) {
    for (int i = 0; i < 16; ++i){
        T[i] = 0;
    }
    T[0] = T[5] = T[10] = T[15] = 1;
}


/*******************************************************
 *  Multiply A times B.  Leave the result in B.
 *******************************************************/
void mtxMultiplyMM (Matrix3D A, Matrix3D B) {
    Matrix3D tmp;
    for (int i = 0; i < 4; ++i){
        for (int j = 0; j < 4; ++j){
            float total = 0;
            for (int k = 0; k < 4; ++k){
                total += A[i * 4 + k] * B[k * 4 + j];
            }
            tmp[i * 4 + j] = total;
        }
    }
    for (int i = 0; i < 16; ++i){
        B[i] = tmp[i];
    }
}


/*******************************************************
 *  Rotate the current matrix T about the given axis
 *  by the specified number of degrees
 *
 *  AXIS CODES
 *    0: x-axis
 *    1: y-axis
 *    2: z-axis
 *******************************************************/
void mtxRotate (Matrix3D T, int axis, float deg) {
    Matrix3D rotate;
    mtxIdentity(rotate);
    deg *= DEG_TO_RAD;
    switch(axis){
    case 0:
        rotate[5] = cos(deg); rotate[6] = -sin(deg);
        rotate[9] = sin(deg); rotate[10] = cos(deg);
        break;

    case 1:
        rotate[0] = cos(deg); rotate[2] = sin(deg);
        rotate[8] = -sin(deg); rotate[10] = cos(deg);
        break;

    case 2:
        rotate[0] = cos(deg); rotate[1] = -sin(deg);
        rotate[4] = sin(deg); rotate[5] = cos(deg);
        break;
    }
    mtxMultiplyMM(rotate, T);
}


/*******************************************************
 *  Translate the current matrix T by the given amount
 *  in each direction
 *******************************************************/
void mtxTranslate (Matrix3D T, float x, float y, float z) {
    Matrix3D translate;
    mtxIdentity(translate);
    translate[3] = x; translate[7] = y; translate[11] = z;
    mtxMultiplyMM(translate, T);
}


/*******************************************************
 *  Scale the given matrix M by the specified amount
 *******************************************************/
void mtxScale (Matrix3D M, float xs, float ys, float zs) {
    Matrix3D scale;
    mtxIdentity(scale);
    scale[0] = xs; scale[5] = ys; scale[10] = zs;
    mtxMultiplyMM(scale, M);
}

/*******************************************************
 * Apply orthographic projection from projection
 * space to image space.
 *******************************************************/
void mtxOrthographic (Matrix3D M, float pxmin, float pxmax,
			   float pymin, float pymax, float pzmin, float pzmax) {
   //----Part 2 A
	Matrix3D temp;
	temp[0] = 2 / (pxmax - pxmin);
	temp[1] = 0; temp[2] = 0;
	temp[3] = -(pxmax + pxmin) / (pxmax - pxmin);
	temp[4] = 0;
	temp[5] = 2 / (pymax - pymin);
	temp[6] = 0;
	temp[7] = -(pymax + pymin) / (pymax - pymin);
	temp[8] = 0; temp[9] = 0;
	temp[10] = 2 / (pzmax - pzmin);
	temp[11] = -(pzmax + pzmin) / (pzmax - pzmin);
	temp[12] = 0; temp[13] = 0; temp[14] = 0; temp[15] = 1;
	mtxMultiplyMM(temp, M);

}


/*******************************************************
 *  Transform the given point by the specified matrix
 *******************************************************/
void mtxTransformPoint (Matrix3D T, float p[3])
{
    float q[3];

    q[0] = T[0] * p[0] + T[1]  * p[1] + T[2]  * p[2]  + T[3] * 1.f;
    q[1] = T[4] * p[0] + T[5]  * p[1] + T[6]  * p[2]  + T[7] * 1.f;
    q[2] = T[8] * p[0] + T[9]  * p[1] + T[10] * p[2]  + T[11] * 1.f;

    //----Set return point
    p[0] = q[0];
    p[1] = q[1];
    p[2] = q[2];
}


/*******************************************************
 *  Transform the given point by the specified matrix
 *******************************************************/
Vector3D mtxTransformPoint (Matrix3D T, Vector3D p)
{
    Vector3D q;

    q.x = T[0]  * p.x + T[1]  * p.y + T[2]  * p.z  + T[3]  * 1.f;
    q.y = T[4]  * p.x + T[5]  * p.y + T[6]  * p.z  + T[7]  * 1.f;
    q.z = T[8]  * p.x + T[9]  * p.y + T[10] * p.z  + T[11] * 1.f;

    return q;
}
