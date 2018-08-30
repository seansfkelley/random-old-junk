/*
This file deals with creating and modifying the graphs.
*/
#ifndef GRAPH_MODS_H
#define GRAPH_MODS_H

//circular includes are not a problem because of the ifndef
#include "definitions.h"
#include "isomorphism.h"

Matrix graph_to_mat(Graph& g);
Graph moldata_to_graph(MolData md);

vector<Vertex> nitrogen_specials(Graph& g);
bool contains_vertex(vector<Vertex> vertices, Vertex v);
Graph add_hydrogen(Graph& g);

#endif
