#include "vec.h"

Vec Vec::operator-(){
    return Vec(-x, -y, -z);
}

Vec Vec::operator-(Vec other){
    return Vec(x-other.x, y-other.y, z-other.z);
}

void Vec::operator-=(Vec other){
    x-=other.x; y-=other.y; z-=other.z;
}

Vec Vec::operator+(Vec other){
    return Vec(x+other.x, y+other.y, z+other.z);
}

void Vec::operator+=(Vec other){
    x+=other.x; y+=other.y; z+=other.z;
}

Vec Vec::operator*(double scalar){
    return Vec(x*scalar, y*scalar, z*scalar);
}

void Vec::operator*=(double scalar){
    x*=scalar; y*=scalar; z*=scalar;
}

Vec Vec::operator/(double scalar){
    return Vec(x/scalar, y/scalar, z/scalar);
}

void Vec::operator/=(double scalar){
    x/=scalar; y/=scalar; z/=scalar;
}

double& Vec::operator[](int index){
    switch(index){
        case 0:
            return x;
        case 1:
            return y;
        case 2:
            return z;
        default:
            cerr << "index " << index << " out of bounds" << endl;
            exit(0);
    }
}

double Vec::mag(){
    return sqrt(x*x+y*y+z*z);
}

void Vec::norm(){
    (*this)/=mag();
}

double Vec::dot(Vec other){
    return x*other.x+y*other.y+z*other.z;
}

Vec Vec::cross(Vec other){
    return Vec(y*other.z-z*other.y,
               z*other.x-x*other.z,
               x*other.y-y*other.x);
}

ostream& operator<<(ostream &os, Vec v){
    os << "<" << v.x << "," << v.y << "," << v.z << ">";
    return  os;
}
