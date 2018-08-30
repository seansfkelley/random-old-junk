#ifndef SPHERE_H
#define SPHERE_H

#include "object.h"

class Sphere : public Object{
public:
    Sphere();
    Sphere(Vec cen, double rad, Pixel col);
    bool collide(Ray ray);
    Pixel color();

private:
    Vec center;
    double radius;
};

#endif
