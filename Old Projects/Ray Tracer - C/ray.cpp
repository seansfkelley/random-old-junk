#include "ray.h"

Ray::Ray(){
    org=Vec();
    dir=Vec();
}

Ray::Ray(Vec origin, Vec direction){
    org=Vec(origin);
    dir=Vec(direction);
    dir.norm();
}

ostream& operator<<(ostream &os, Ray ray){
    os << "<." << ray.org << " ->" << ray.dir << ">";
    return os;
}
