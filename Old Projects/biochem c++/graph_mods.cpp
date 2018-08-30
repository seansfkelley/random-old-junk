#include "graph_mods.h"

//there has got to be a builtin way to get the matrix from an adjacency_matrix
//either way this is clunky

//convert a boost graph into a newmat matrix
Matrix graph_to_mat(Graph& g){
    Matrix graph_mat(num_vertices(g), num_vertices(g));
    graph_mat=0.0;
    
    VertexIter vi, vi_end;
    OutEdgeIter oei, oei_end;
    
    //tie() saves effort by using assignable tuples
    tie(vi, vi_end)=vertices(g);
    for(; vi!=vi_end; ++vi){
    
        tie(oei, oei_end)=out_edges(*vi, g);
        for(; oei!=oei_end; ++oei)
            graph_mat[*vi][target(*oei, g)]=g[*oei].strength;
    }
    return graph_mat;
}

//convert a pair of vectors into a boost graph
Graph moldata_to_graph(MolData md){
    Graph g(md.atoms.size());
    //add edges (vertices _implicitly_) and set their bond strength
    for(vector<int*>::iterator i=md.bonds.begin(); i<md.bonds.end(); ++i)
        g[add_edge((*i)[0]-1, (*i)[1]-1, g).first].strength=(*i)[2];
    
    //set the atomic numbers of all the atoms
    for(int i=0; i<md.atoms.size(); ++i){
        g[i].type=md.atoms[i];
        g[i].charge=md.charges[i];
        g[i].tags=map<string, int>();
    }
    cout << endl;
    return g;
}

//the copy constructor for Graphs doesn't work/is inadequate
void copy_graph(Graph& from, Graph& to){
    EdgeIter ei, ei_end;
    tie(ei, ei_end)=edges(from);
    for(; ei!=ei_end; ++ei)
        add_edge(target(*ei, from), source(*ei, from), from[*ei], to);
    
    VertexIter vi, vi_end;
    tie(vi, vi_end)=vertices(from);
    for(; vi!=vi_end; ++vi)
        to[*vi]=from[*vi];
}

//this function offends me personally. such are the costs of hard coding.
vector<Vertex> nitrogen_specials(Graph& g){
    vector<int> atoms;
    atoms.push_back(atomic_numbers["N"]);
    atoms.push_back(atomic_numbers["C"]);
    atoms.push_back(atomic_numbers["C"]);
    atoms.push_back(atomic_numbers["O"]);
    atoms.push_back(atomic_numbers["O"]);
    
    vector<int> atoms_no_wildcards=vector<int>(atoms);
    
    vector<int> charges;
    for(int i=0; i<5; ++i)
        charges.push_back(0);
    
    vector<int*> bonds;
    int bond1[]={1,2,1};
    int bond2[]={2,3,1};
    int bond3[]={3,4,1};
    int bond4[]={3,5,2};
    bonds.push_back(bond1);
    bonds.push_back(bond2);
    bonds.push_back(bond3);
    bonds.push_back(bond4);
    
    MolData nitrogen_search;
    nitrogen_search.atoms=atoms;
    nitrogen_search.atoms_no_wildcards=atoms_no_wildcards;
    nitrogen_search.charges=charges;
    nitrogen_search.bonds=bonds;
    nitrogen_search.bond_match=true;
    
    Matrix beta=graph_to_mat(g);
    vector<MatchSet> matches=find_matches(nitrogen_search, g, beta, false, false);
    
    cout << "finding indices for +1 nitrogens: [";
    vector<Vertex> vertices;
    for(vector<MatchSet>::iterator mii=matches.begin(); mii!=matches.end(); ++mii){
        for(vector<int>::iterator i=(*mii).indices.begin(); i!=(*mii).indices.end(); ++i){
            if(g[*i].type==atomic_numbers["N"]){
                cout << *i << ", ";
                vertices.push_back(vertex(*i, g));
                break;
            }
        }
    }
    cout << "]" << endl;
    return vertices;
}

//find in <algorithm> didn't work in this case
bool contains_vertex(vector<Vertex> vertices, Vertex v){
    for(vector<Vertex>::iterator vi=vertices.begin(); vi!=vertices.end(); ++vi){
        if(*vi==v)
            return true;
    }
}

//this function's essentially copy-pasted structures offends me even more. is there
//no way to calculate the additional size needed and add it? graphs can't be expanded,
//they must be initialized with a constant size
//does NOT handle invalid input, i.e. zero/too many/too strong bonds
Graph add_hydrogen(Graph& g){
    vector<Vertex> N_plus1_vertices=nitrogen_specials(g);
    
    OutEdgeIter oei, oei_end;
    VertexIter vi, vi_end;
    map<Vertex, int> num_to_add;
    int temp_h, size_increase=0;
    
    cout << "adding hydrogens to:" << endl;
    tie(vi, vi_end)=vertices(g);
    for(; vi!=vi_end; ++vi){
        temp_h=0;
        cout << (*vi) << " (type " << g[*vi].type << "): ";
        temp_h=max_bonds[g[*vi].type]+g[*vi].charge;
        tie(oei, oei_end)=out_edges(*vi, g);
        for(; oei!=oei_end; ++oei)
            temp_h-=g[*oei].strength;
        /*
        if(g[*vi].type==atomic_numbers["C"]){
            //add as many hydrogen as necessary to fill up all available slots (4 total)
            temp_h=4;
            tie(oei, oei_end)=out_edges(*vi, g);
            for(; oei!=oei_end; ++oei)
                temp_h-=g[*oei].strength;
            
        }
        else if(g[*vi].type==atomic_numbers["N"]){
            //add as many hydrogen as necessary to fill up 3 slots, 1 more if it's bonded
            //to a C that is in turn bonded to a carboxyl (COO/COOH)
            temp_h=0;
            tie(oei, oei_end)=out_edges(*vi, g);
            for(; oei!=oei_end; ++oei)
                temp_h+=g[*oei].strength;
            if(temp_h==4)
                //handle the case that the user specified four bonds, but its not the carboxyl special case
                temp_h=0;
            else{
                temp_h=3-temp_h;
                temp_h+=contains_vertex(N_plus1_vertices, *vi)?1:0;
            }
        }
        else if(g[*vi].type==atomic_numbers["O"])
            //add if there is exactly 1 bond of strength 1
            temp_h=out_degree(*vi, g)==1 && g[*(out_edges(*vi, g).first)].strength==1?1:0;
        else if(g[*vi].type==atomic_numbers["S"])
            //add if there is exactly 1 bond of strength 1
            temp_h=out_degree(*vi, g)==1 && g[*(out_edges(*vi, g).first)].strength==1?1:0;
        */
        num_to_add[*vi]=temp_h;
        if(temp_h>0)
            size_increase+=temp_h;
        cout << temp_h << endl;
    }
    
//    EdgeIter ei, ei_end;
//    
//     cout << "old graph:" << endl;
//     
//     cout << "edges" << endl;
//     tie(ei, ei_end)=edges(g);
//     for(; ei!=ei_end; ++ei)
//         cout << g[*ei].strength << endl;
//         
//     cout << "vertices" << endl;
//     tie(vi, vi_end)=vertices(g);
//     for(; vi!=vi_end; ++vi)
//         cout << g[*vi].type << endl;
    
    cout << size_increase << " hydrogens to be added" << endl;
    
    if(size_increase==0)
        return g;
    
    Graph new_g(num_vertices(g)+size_increase);
    copy_graph(g, new_g);
    
    //initialize the hydrogens' atom traits (only type matters)
    tie(vi, vi_end)=vertices(new_g);
    for(vi=vi+num_vertices(g); vi!=vi_end; ++vi){
        new_g[*vi].type=atomic_numbers["H"];
        new_g[*vi].charge=0;
    }
        
    int current_index=num_vertices(g);
    for(map<Vertex, int>::iterator iter=num_to_add.begin(); iter!=num_to_add.end(); ++iter){
        for(int i=0; i<(*iter).second; ++i)
            new_g[add_edge((*iter).first, vertex(current_index++, new_g), new_g).first].strength=1;
    }
    
    return new_g;
}
