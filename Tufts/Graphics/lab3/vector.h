
#ifndef VECTOR_H
#define VECTOR_H


/*******************************************************
 *  Structure for three dimensional vector
 *******************************************************/
struct Vector3D {
    float x;
    float y;
    float z;
};

struct Vector2D {
	float x;
	float y;
};


/*******************************************************
 *  Compute the length of the given vector
 *******************************************************/
float vecMag (Vector3D v);


/*******************************************************
 *  Compute the dot product of two vectors
 *******************************************************/
float vecDot (Vector3D v1, Vector3D v2);


/*******************************************************
 *  Subtract the second vector from the first
 *******************************************************/
Vector3D vecSub (Vector3D v1, Vector3D v2);


/*******************************************************
 *  Add the given vectors together
 *******************************************************/
Vector3D vecAdd (Vector3D v1, Vector3D v2);


/*******************************************************
 *  Normalize the given vector
 *******************************************************/
Vector3D vecNorm (Vector3D v);


/*******************************************************
 *  Multiply the given vector by the given scalar
 *******************************************************/
Vector3D vecScale (Vector3D v, float s);


/*******************************************************
 *  Compute the cross product of the given vectors
 *******************************************************/
Vector3D vecCross (Vector3D u, Vector3D v);

/*******************************************************
 *  Print the vector to the terminal window
 *  This function can be used for debug purposes
 *******************************************************/
void printVec3D(Vector3D v);
/*******************************************************
 *  End of #include _VECTOR_H
 *******************************************************/
#endif 
