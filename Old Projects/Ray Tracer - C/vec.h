#ifndef VEC_H
#define VEC_H

#include "defs.h"

class Vec{
public:
    Vec(double X=0, double Y=0, double Z=0):x(X),y(Y),z(Z){;}
    
    Vec operator-();
    
    Vec operator-(Vec other);
    void operator-=(Vec other);
    
    Vec operator+(Vec other);
    void operator+=(Vec other);
    
    Vec operator*(double scalar);
    void operator*=(double scalar);
    
    Vec operator/(double scalar);
    void operator/=(double scalar);
    
    double& operator[](int index);
    
    double mag();
    void norm();
    double dot(Vec other);
    Vec cross(Vec other);
    
    double x, y, z;
};

ostream& operator<<(ostream &os, Vec v);

#endif
