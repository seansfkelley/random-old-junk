#include "vector.h"
#include <math.h>
#include <cstdio>

/*******************************************************
 *  Compute the length of the given vector
 *******************************************************/
float vecMag (Vector3D v)
{
    return (float)sqrt(vecDot(v, v));
}


/*******************************************************
 *  Compute the dot product of the two vectors
 *******************************************************/
float vecDot (Vector3D v1, Vector3D v2)
{
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z; 
}


/*******************************************************
 *  Subtract the second vector from the first
 *******************************************************/
Vector3D vecSub (Vector3D v1, Vector3D v2)
{
    Vector3D v;
    v.x = v1.x - v2.x;
    v.y = v1.y - v2.y;
    v.z = v1.z - v2.z;
    return (v);
}


/*******************************************************
 *  Add the given vectors together
 *******************************************************/
Vector3D vecAdd (Vector3D v1, Vector3D v2)
{
    Vector3D v;
    v.x = v1.x + v2.x;
    v.y = v1.y + v2.y;
    v.z = v1.z + v2.z;
    return (v);
}


/*******************************************************
 *  Normalize the given vector
 *******************************************************/
Vector3D vecNorm (Vector3D v)
{
    Vector3D vNorm;
    float mag = vecMag(v);
    vNorm.x = v.x / mag;
    vNorm.y = v.y / mag;
    vNorm.z = v.z / mag;
    return (vNorm);
}


/*******************************************************
 *  Multiply the given vector by the given scalar
 *******************************************************/
Vector3D vecScale (Vector3D v, float s)
{
    Vector3D vScale;
    vScale.x = v.x * s;
    vScale.y = v.y * s;
    vScale.z = v.z * s;
    return (vScale);
}


/*******************************************************
 *  Compute the cross product of the given vectors
 *******************************************************/
Vector3D vecCross (Vector3D v, Vector3D w)
{
    Vector3D u;
    u.x = v.y * w.z - w.y * v.z;
    u.y = w.x * v.z - v.x * w.z;
    u.z = v.x * w.y - w.x * v.y;
    return (u);
}

/*******************************************************
 *  Print the vector to the terminal window
 *  This function can be used for debug purposes
 *******************************************************/
void printVec3D(Vector3D v)
{
	printf("(%f,%f,%f)\n",v.x,v.y,v.z);
}