/*
This file generates all matches, covers them on the fly, then assigns modified energies.
*/

#ifndef ISOMORPHISM_H
#define ISOMORPHISM_H

#include "definitions.h"
#include "molfile.h"
#include "graph_mods.h"
#include "rings.h"
#include "mat_gen.h"

vector<int> matches_as_indices_main(Matrix m, Graph& g);
vector<int> matches_as_indices_fgroup(Matrix m);

bool comp_match(Match one, Match two);
bool comp_matchset(MatchSet one, MatchSet two);
bool equal_matchset(MatchSet one, MatchSet two);
bool comp_emap_keys(string one, string two);
bool exception_match(vector<string> ex, map<string, int> tags);

double process_molecule(MolData molecule_data, string filename);
double correction_factors(Graph& g);
vector<MatchSet> find_matches(MolData fgroup, Graph& molecule, Matrix& beta, bool check_availability=true, bool check_ions=true);
vector<MatchSet> remove_duplicates(vector<MatchSet> v);
vector<Match> expand_matches(vector<MatchSet> ms, Graph g);
void one_matrix(Matrix& m);

#endif
