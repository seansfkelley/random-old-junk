#ifndef RAY_H
#define RAY_H

#include "defs.h"
#include "vec.h"

class Ray{
public:
    Ray();
    Ray(Vec origin, Vec direction);
    
    Vec org, dir;
};

ostream& operator<<(ostream &os, Ray ray);

#endif
