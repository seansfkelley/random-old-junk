/*
This file serves as a global repository of all includes etc. to make life easy
and avoid a whole lot of redundancy
*/

#ifndef DEFINITIONS_H
#define DEFINITIONS_H

//keywords in molfiles
#define KW_MODIFIER "MODIFIER"
#define KW_DEFAULT_ENERGY "DEFAULT"
#define KW_ALT_ENERGY "ALTERNATE"
#define KW_NO_BOND_MATCH "NOBOND"
#define KW_CORRECTION "CORRECTION"
#define KW_CHANGE_DIR "DIRECTORY"

//other keyword-type constants
#define MOD_ZERO_MORE_STRING "*"
#define MOD_ZERO_MORE_VALUE -1
#define MOD_ONE_MORE_STRING "+"
#define MOD_ONE_MORE_VALUE -2
#define WILDCARD_STRING "?"
#define WILDCARD_VALUE -1
#define RING_MODIFIER "RING"
#define AROMATIC_MODIFIER "AROMATIC"

//other constants
#define CONCURRENT_COVER true
#define ORIGIN 0
#define MOD_HYDROCARBON 3.68
#define MOD_AROMATIC 0
#define MOD_HETEROAROMATIC -1.95
#define NA_ENERGY_VALUE 0 //value for energy if default is not specified and it must be used
                          //NOT the indicator for no specification, that is DBL_MAX
#define NUM_ELEMENTS 83
#define RING_MAX_SIZE 6

#define WANT_STREAM //for newmat's matrix io

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <algorithm>
#include <vector>
#include <map>
#include <cfloat>
#include <ctime>
#include <boost/utility.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/adjacency_matrix.hpp>
#include <newmat10/newmat.h>
#include <newmat10/newmatap.h>
#include <newmat10/newmatio.h>

using namespace std;
using namespace boost;
using namespace NEWMAT;

struct ModConfig{
    int *config;
    int priority;
    double energy;
    vector<string> exceptions;
};

typedef map<string, ModConfig> EnergyMap;

struct AtomInfo{
    int type, charge;
    map<string, int> tags;
};

struct BondInfo{
    int strength;
};

struct MatchSet{
    vector<int> indices, original_indices;
    EnergyMap energies;
};

struct Match{
    int priority;
    vector<int> indices, original_indices;
    double energy;
};

struct MatNode{
    vector<MatNode*> children;
    RowVector row, mask;
};

struct MolData{
    vector<int> atoms, atoms_no_wildcards, charges;
    vector<int*> bonds;
    EnergyMap energies;
    string name, modifier;
    bool bond_match, correction;
};

struct Ring{
    vector<int> indices;
    bool aromatic;
};

typedef adjacency_matrix<undirectedS, AtomInfo, BondInfo> Graph;

typedef graph_traits<Graph>::vertex_descriptor Vertex;
typedef graph_traits<Graph>::vertex_iterator VertexIter;
typedef graph_traits<Graph>::adjacency_iterator AdjVertexIter;
typedef graph_traits<Graph>::edge_iterator EdgeIter;
typedef graph_traits<Graph>::out_edge_iterator OutEdgeIter;

const string elem_symbols[NUM_ELEMENTS]=
{"H","He","Li","Be", "B", "C", "N", "O", "F","Ne","Na","Mg","Al","Si", "P", "S",
"Cl","Ar", "K","Ca","Sc","Ti", "V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge",
"As","Se","Br","Kr","Rb","Sr", "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
"In","Sn","Sb","Te", "I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd",
"Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta", "W","Re","Os","Ir","Pt","Au","Hg",
"Tl","Pb","Bi"};

//is S=2 chemically accurate?
const int elem_max_bonds[NUM_ELEMENTS]=
{  1,  -1,  -1,  -1,  -1,   4,   4,   2,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   2,
  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
  -1,  -1,  -1};

//declare all globals here, put them in driver.cpp
extern map<string, int> atomic_numbers;
extern map<int, int> max_bonds;
extern bool *available;

#endif
