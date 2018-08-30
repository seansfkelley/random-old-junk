#ifndef DEFS_H
#define DEFS_H

#include <iostream>
#include <cmath>
#include <vector>
#include <cfloat>

#include <pngwriter.h>

using namespace std;

typedef unsigned char byte;

class Pixel{
public:
    Pixel(byte red=255, byte green=255, byte blue=255, byte alpha=0):r(red),g(green),b(blue),a(alpha){;}
    byte r, g, b, a;
};

#endif
