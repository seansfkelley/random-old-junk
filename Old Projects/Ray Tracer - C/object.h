#ifndef OBJECT_H
#define OBJECT_H

#include "defs.h"
#include "ray.h"

class Object{
public:
    virtual bool collide(Ray ray)=0;
    virtual Pixel color()=0;
    double distance(){return collision_dist;}

protected:
    double collision_dist;
    Pixel obj_color;
};

//virtual ostream& operator<<(ostream& os, Object o);

#endif
