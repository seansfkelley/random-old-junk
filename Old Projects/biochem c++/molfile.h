/*
This file parses molfiles into vectors and is home to various auxiliary functions
used by other files.
*/

#ifndef MOLFILE_H
#define MOLFILE_H

#include "definitions.h"

void init_atomic_numbers();
void init_max_bonds();

void print(int *integers, int how_many);
void print(vector<string> v);
void print(vector<int> v);
void print(vector<int*> v);
void print(Matrix m);
void print(Match m);
void print(MatchSet mi);
void print(ModConfig mc, int num_atoms);
void print(MolData md);
void print(Ring r);
void print(map<string, int> tags);

vector<string> split(string s, char delim);
int atoi(string s);
double atof(string s);

MolData parse_molfile(string filename);

#endif
