#ifndef BOX_H
#define BOX_H

#include "defs.h"
#include "vec.h"
#include "object.h"

class Box{
public:
    Box();
    Box(vector<Object*> all_objects);
    ~Box();

private:
    vector<Object*> objects;
};

/*
no front/back to box?
test if point of origin is inside box -> must be contained
otherwise do special intersection of plane(s) (for the box sides) and object in question?
*/

#endif
