#include "tracer.h"

//+z is INTO screen

Pixel raytrace(Ray ray, vector<Object*> all_objects){
    vector<Object*>::iterator o;
    Object *cur=NULL;
    double dist=DBL_MAX;
    for(o=all_objects.begin(); o<all_objects.end(); ++o){
        if((*o)->collide(ray) && (*o)->distance()<dist){
            cur=(*o);
            dist=(*o)->distance();
        }
    }
    if(cur!=NULL)
        return cur->color();
    return Pixel(BKRD_RED, BKRD_GREEN, BKRD_BLUE);
}

int main(int argc, char *argv[]){
    Vec eye(0,0,0), topleft(-50,-50,100), delta_x=Vec(1,0,0), delta_y=Vec(0,1,0);
    Vec top=topleft, current;
    
    vector<Object*> all_objects;
    
    Sphere s(Vec(0,0,300), 100, Pixel(127,127,127));
    
    all_objects.push_back(&s);

    pngwriter image(100, 100, 0, "out.png");
    
    Pixel p;
    for(int i=1; i<=100; ++i){
        current=top;
        for(int j=1; j<=100; ++j){
            p=raytrace(Ray(current, current-eye), all_objects);
            image.plot(i, j, p.r*255, p.g*255, p.b*255);
            current+=delta_y;
        }
        top+=delta_x;
    }
    
    image.close();
    //bounding boxes!
    //anti aliasing
}
