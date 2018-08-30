#include "mat_gen.h"

MatGen::MatGen(){
    done=true;
    num_generated=0;
}

MatGen::MatGen(Matrix m){
    original=m;
    done=false;
    num_generated=0;
    
    rows=m.Nrows();
    cols=m.Ncols();
    prime=Matrix(rows, cols);
    
    firsts=new int[rows];
    bool all_zero;
    for(int i=0; i<rows; ++i){
        all_zero=true;
        for(int j=0; j<cols; ++j){
            if(original[i][j]!=0){
                firsts[i]=j;
                all_zero=false;
                break;
            }
        }
        if(all_zero){
            done=true;
            break;
        }
    }
    
    if(done){
        lasts=currents=NULL;
        masks=NULL;
        return;
    }
    
    lasts=new int[rows];
    for(int i=0; i<rows; ++i){
        lasts[i]=0;
        for(int j=cols-1; j>=0; --j){
            if(original[i][j]!=0){
                lasts[i]=j;
                break;
            }
        }
    }
    
    currents=new int[rows];
    for(int i=0; i<rows; ++i)
        currents[i]=0;
    
    masks=new int*[rows];
    for(int i=0; i<rows; ++i){
        masks[i]=new int[cols];
        for(int j=0; j<cols; ++j)
            masks[i][j]=0;
    }
    
    prime=0;
    next(true);
}

MatGen::~MatGen(){
    delete firsts;
    if(lasts!=NULL)
        delete lasts;
    if(currents!=NULL)
        delete currents;
    if(masks!=NULL){
        for(int i=0; i<rows; ++i)
            delete masks[i];
        delete masks;
    }
}

Matrix MatGen::get(){
    return prime;
}

void MatGen::next(bool first_time){
    int lowest_chg_row=-1, next_spot;
    
    if(first_time){
        lowest_chg_row=0;
        next_spot=firsts[0];
    }
    else{
        //figure out bottommost row that has a possiblity after the current, accounting
        //for the masks of the previous rows
        for(int i=rows-1; i>=0 && lowest_chg_row==-1; --i){
            if(currents[i]>=lasts[i])
                continue;
            for(int j=currents[i]+1; j<=lasts[i]; ++j){
                if(masks[i][j]==0 && original[i][j]!=0){
                    next_spot=j;
                    lowest_chg_row=i;
                    break;
                }
            }
        }
        
        if(lowest_chg_row==-1){
            done=true;
            return;
        }
    }
    
    //set the row in question as appropriate, masks too (important!)
    masks[lowest_chg_row][currents[lowest_chg_row]]=0;
    prime[lowest_chg_row][currents[lowest_chg_row]]=0;
    
    currents[lowest_chg_row]=next_spot;
    
    masks[lowest_chg_row][currents[lowest_chg_row]]=1;
    prime[lowest_chg_row][currents[lowest_chg_row]]=1;
    
    //modify the following rows according to the availibility and masks
    //if the row cant have a one set, set all following rows to their lasts
    //and call it again for the next permutation
    
    bool upper_row_failed=false, this_row_failed;
    
    //outermost: iterate through the rows to be changed
    for(int i=lowest_chg_row+1; i<rows; ++i){
        //inner loop: reset this level's masks (essentially a 'bitwise' or)
        for(int j=0; j<cols; ++j)
            masks[i][j]=masks[i-1][j];
        masks[i][currents[i-1]]=1;
        
        prime[i][currents[i]]=0;
        
        if(!upper_row_failed){
            this_row_failed=true;
            for(int j=firsts[i]; j<=lasts[i]; ++j){
                if(masks[i][j]==0 && original[i][j]!=0){
                    masks[i][j]=1;
                    prime[i][j]=1;
                    currents[i]=j;
                    this_row_failed=false;
                    break;
                }
            }
        }
        
        if(this_row_failed || upper_row_failed){
            upper_row_failed=true;
            masks[i][lasts[i]]=1;
            prime[i][lasts[i]]=1;
            currents[i]=lasts[i];
        }
    }
    if(upper_row_failed)
        next();
    else
        num_generated++;
}

bool MatGen::has_next(){
    return !done;
}

//see if two given atoms are a possible match
bool correspond(Graph& alpha, Graph& beta, int alpha_index, int beta_index, bool check_availability, bool check_ions){
    //this is where the magic happens - enforce strictest possible matching
    //conditions to minimize the number of permutations that will be generated
    
    //check if it's already been covered
    if(check_availability &&
       alpha[alpha_index].type!=WILDCARD_VALUE &&
       !available[beta_index])
        return false;
    
    //type (atomic number)
    if(alpha[alpha_index].type!=WILDCARD_VALUE &&
       alpha[alpha_index].type!=beta[beta_index].type)
        return false;
     
    //charge (ionic)
    if(check_ions && alpha[alpha_index].type!=WILDCARD_VALUE && 
       alpha[alpha_index].charge!=beta[beta_index].charge)
        return false;

    //degree (number of bonds)
    if(out_degree(alpha_index, alpha)>out_degree(beta_index, beta))
        return false;
    
    int num_bonds=0;
    OutEdgeIter oei, oei_end;
    tie(oei, oei_end)=out_edges(alpha_index, alpha);
    for(; oei!=oei_end; ++oei)
        num_bonds+=alpha[*oei].strength;
    if(num_bonds>max_bonds[alpha[alpha_index].type])
        return false;
    
    //check neighborhood using set intersection of the two neighborhoods
    vector<int> alpha_neighbors, beta_neighbors, intersect;
    
    AdjVertexIter avi, avi_end;
    tie(avi, avi_end)=adjacent_vertices(alpha_index, alpha);
    for(; avi!=avi_end; ++avi){
        if(alpha[*avi].type!=WILDCARD_VALUE)
            alpha_neighbors.push_back(alpha[*avi].type);
    }
    
    tie(avi, avi_end)=adjacent_vertices(beta_index, beta);
    for(; avi!=avi_end; ++avi)
        beta_neighbors.push_back(beta[*avi].type);
    
    sort(alpha_neighbors.begin(), alpha_neighbors.end());
    sort(beta_neighbors.begin(), beta_neighbors.end());
    
    set_intersection(alpha_neighbors.begin(), alpha_neighbors.end(),
                     beta_neighbors.begin(), beta_neighbors.end(),
                     insert_iterator<vector<int> >(intersect, intersect.begin()));
    
    //what a hack - if it didn't get 'initialized' (by the intersection being empty)
    //this fixes it; would crash equal() otherwise
    intersect.push_back(0);
    intersect.pop_back();
    
    if(!equal(alpha_neighbors.begin(), alpha_neighbors.end(), intersect.begin()))
        return false;
    
    return true;
}

//generate M0 using correspond, once for each space in the matrix
Matrix gen_M0(Matrix& m_alpha, Matrix& m_beta, Graph& g_alpha, Graph& g_beta, bool check_availability, bool check_ions){
    Matrix M0(m_alpha.Nrows(), m_beta.Ncols());
    for(int row=0; row<M0.Nrows(); ++row){
        for(int col=0; col<M0.Ncols(); ++col)
            M0[row][col]=correspond(g_alpha, g_beta, row, col, check_availability, check_ions)?1:0;
    }
    return M0;
}
