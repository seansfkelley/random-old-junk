#ifndef MAT_GEN_H
#define MAT_GEN_H

#include "definitions.h"

class MatGen{
public:
    MatGen();
    MatGen(Matrix m);
    ~MatGen();
    
    Matrix get();
    void next(bool first_time=false);
    bool has_next();
    
    int num_generated;
    
private:
    Matrix original, prime;
    int rows, cols;
    int *firsts, *lasts, *currents;
    int **masks;
    bool done;
};

bool correspond(Graph& alpha, Graph& beta, int row, int col, bool check_availability, bool check_ions);
Matrix gen_M0(Matrix& m_alpha, Matrix& m_beta, Graph& g_alpha, Graph& g_beta, bool check_availability=true, bool check_ions=true);

#endif
