#ifndef RINGS_H
#define RINGS_H

#include "definitions.h"
#include "molfile.h"

double find_rings(Graph& molecule);
void ring_search_rec(Graph& g, int origin, int current, Ring cur_ring, vector<Ring> &all_rings, int depth);
bool ring_comp(Ring first, Ring second);
bool equal_rings(Ring one, Ring two);

#endif
