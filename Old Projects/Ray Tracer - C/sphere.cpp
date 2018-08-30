#include "sphere.h"

Sphere::Sphere(){
    center=Vec();
    radius=0;
    obj_color=Pixel();
}

Sphere::Sphere(Vec cen, double rad, Pixel col){
    center=Vec(cen);
    radius=rad;
    obj_color=Pixel(col);
}

bool Sphere::collide(Ray ray){
    Vec dist=ray.org-center;
    double b=2*ray.dir.dot(dist), c=dist.dot(dist)-radius*radius, d=b*b-4*c;
    if(d<0)
        return false;
    double t0=(-b-sqrt(d))/2;
    if(t0>0){
        collision_dist=t0;
        return true;
    }
    double t1=(-b+sqrt(d))/2;
    if(t1>0){
        collision_dist=t1;
        return true;
    }
    return false;
}

Pixel Sphere::color(){
    return Pixel(obj_color);
}
