#include "isomorphism.h"

//produces a vector of indices (the ones implied from the main molfile listing) of all matching atoms
//any wildcards are ignored, by checking with the node properties of the graph
vector<int> matches_as_indices_main(Matrix m, Graph& g){
    vector<int> v;
    for(int col=0; col<m.Ncols(); ++col){
        for(int row=0; row<m.Nrows(); ++row){
            if(m[row][col]==1 && g[row].type!=WILDCARD_VALUE){
                v.push_back(col);
                break;
            }
        }
    }
    return v;
}

//produces a different order than the other by using rows as outer loop. _main
//returns them in sorted order, this version is unsorted. the index at position
//n is the index of the main graph's atom that matches the nth atom in the fgroup
//does NOT strip the wildcards, they have to match for configuration too
vector<int> matches_as_indices_fgroup(Matrix m){
    vector<int> v;
    for(int row=0; row<m.Nrows(); ++row){
        for(int col=0; col<m.Ncols(); ++col){
            if(m[row][col]==1){
                v.push_back(col);
                break;
            }
        }
    }
    return v;
}

bool comp_match(Match one, Match two){
    if(one.priority==two.priority){
        if(one.indices.size()==two.indices.size()){
            if(equal(one.indices.begin(), one.indices.end(), two.indices.begin())){
                vector<int> orig1(one.original_indices), orig2(two.original_indices);
                if(orig1.size()!=orig2.size())
                    return orig1.size()>orig2.size();
                sort(orig1.begin(), orig1.end());
                sort(orig2.begin(), orig2.end());
                return lexicographical_compare(orig1.begin(), orig1.end(), orig2.begin(), orig2.end());
            }
            return lexicographical_compare(one.indices.begin(), one.indices.end(),
                                           two.indices.begin(), two.indices.end());
        }
        return one.indices.size()>two.indices.size();
    }
    return one.priority<two.priority;
}

/*
for both these sort functions:
energies are not required, they are extra information
the given matches might different by which wildcards they have been assigned,
    so if the main indices are equal then the unsorted original_indices must be
    compared, but CANNOT BE MODIFIED, hence the copies of them
*/

//by descending size
bool comp_matchset(MatchSet one, MatchSet two){
    if(one.indices.size()==two.indices.size()){
        if(equal(one.indices.begin(), one.indices.end(), two.indices.begin())){
            vector<int> orig1(one.original_indices), orig2(two.original_indices);
            if(orig1.size()!=orig2.size())
                return orig1.size()>orig2.size();
            sort(orig1.begin(), orig1.end());
            sort(orig2.begin(), orig2.end());
            return lexicographical_compare(orig1.begin(), orig1.end(), orig2.begin(), orig2.end());
        }
        return lexicographical_compare(one.indices.begin(), one.indices.end(),
                                       two.indices.begin(), two.indices.end());
    }
    return one.indices.size()>two.indices.size();
}

bool equal_matchset(MatchSet one, MatchSet two){
    //energies is not required for equality
    if(one.indices.size()==two.indices.size() && 
       equal(one.indices.begin(), one.indices.end(), two.indices.begin())){
        vector<int> orig1(one.original_indices), orig2(two.original_indices);
        sort(orig1.begin(), orig1.end());
        sort(orig2.begin(), orig2.end());
        return orig1.size()==orig2.size() && equal(orig1.begin(), orig1.end(), orig2.begin());
    }
    return false;
}

bool comp_emap_keys(string one, string two){
    return atoi(one.substr(one.find_last_of(':')+1))<atoi(two.substr(two.find_last_of(':')+1)); 
}

//match a list of exceptions, as taken from a modconfig, and make sure it has
//no overlap with the given tags for the atom in question
bool exception_match(vector<string> ex, map<string, int> tags){
    vector<string> one(ex), two, inter;
    for(map<string, int>::iterator i=tags.begin(); i!=tags.end(); ++i){
        if((*i).second>0)
            two.push_back((*i).first);
    }
    sort(one.begin(), one.end());
    sort(two.begin(), two.end());
    cout << "checking for ";
    print(one);
    cout << " in ";
    print(two);
    cout << endl;
    inter.reserve(max(one.size(), two.size()));
    set_intersection(one.begin(), one.end(), two.begin(), two.end(),
                     insert_iterator<vector<string> >(inter, inter.begin()));
    if(inter.size()>0){
        cout << "exception with: ";
        print(inter);
        cout << endl;
    }
    return inter.size()>0;
}

//the heart of the program
double process_molecule(MolData molecule_data, string filename){
    Graph molecule=moldata_to_graph(molecule_data);
    //atoms/bonds are never referenced again so adding hydrogens won't create inconsistencies
    molecule=add_hydrogen(molecule);
    Matrix beta=graph_to_mat(molecule);
    ifstream f;
    f.open(filename.c_str());
    
    if(!f.is_open()){
        cout << "Error opening file \'" << filename << "\'" << endl;
        exit(0);
    }
    
    print(beta);
    
    //declared this early to allow corrective groups to be added
    double total_energy=correction_factors(molecule);
    
    //parse and store all the f-group files as graphs
    string s, fg_name, directory="";
    vector<string> tokens;
    vector<MolData> all_data;
    while(!f.eof()){
        getline(f, s);
        if(s=="")
            continue;
        
        tokens=split(s, ' ');
        
        if(tokens[0]==KW_CHANGE_DIR){
            directory=tokens[1];
            continue;
        }
        
        MolData fgroup_data=parse_molfile(directory+tokens[0]);
        //this is not an essential step, but may be a useful piece of information to have later
        fgroup_data.name=tokens[0];
        Graph fg=moldata_to_graph(fgroup_data);
        
        //if the molfile is a modifier, don't add it to the fgroup list
        //if it isnt covered, calculate it now. these two arent mututally exclusive
        if(fgroup_data.modifier!="" || fgroup_data.correction){
            if(fgroup_data.modifier!="")
                cout << "modifier ";
            if(fgroup_data.correction)
                cout << "correction ";
            cout << s << endl;
            //tag the atoms now for use in energy assignment later
            vector<MatchSet> temp_matches=find_matches(fgroup_data, molecule, beta, false, false);
            sort(temp_matches.begin(), temp_matches.end(), comp_matchset);
            cout << "all matches:" << endl;
            for(vector<MatchSet>::iterator match=temp_matches.begin(); match<temp_matches.end(); ++match)
                print(*match);
            //remove duplicates to avoid artificially inflating the numbers in the map
            temp_matches=remove_duplicates(temp_matches);
            cout << "processed matches:" << endl;
            for(vector<MatchSet>::iterator match=temp_matches.begin(); match<temp_matches.end(); ++match){
                print(*match);
                if(fgroup_data.correction){
                    cout << "applying " << fgroup_data.energies[KW_DEFAULT_ENERGY].energy << " correction" << endl;
                    total_energy+=fgroup_data.energies[KW_DEFAULT_ENERGY].energy;
                }
                if(fgroup_data.modifier!=""){
                    for(vector<int>::iterator index=(*match).original_indices.begin(); index<(*match).original_indices.end(); ++index)
                        //the tag map stores TYPE:#_OCCURENCES pairs
                        molecule[*index].tags[fgroup_data.modifier]+=1;
                }
            }
            continue;
        }
        
        all_data.push_back(fgroup_data);
    }
    
    f.close();
    
    //this is the global
    available=new bool[num_vertices(molecule)];
    for(int i=0; i<num_vertices(molecule); ++i)
        available[i]=true;
    
    cout << "tags:" << endl;
    for(int i=0; i<num_vertices(molecule); ++i){
        cout << i << ":" << endl;
        print(molecule[i].tags);
    }
    
    vector<Match> global_matches, covers;
    vector<Match>::iterator m_iter;
    vector<MatchSet>::iterator ms_iter;
    for(vector<MolData>::iterator data=all_data.begin(); data!=all_data.end(); ++data){
        vector<MatchSet> matches=find_matches(*data, molecule, beta);
        
        cout << "matches:" << endl;
        for(ms_iter=matches.begin(); ms_iter<matches.end(); ++ms_iter)
            print(*ms_iter);
        cout << endl;
        
        matches=remove_duplicates(matches);
        cout << "unique matches:" << endl;
        for(ms_iter=matches.begin(); ms_iter<matches.end(); ++ms_iter)
            print(*ms_iter);
        cout << endl;
        
        vector<Match> all_matches=expand_matches(matches, molecule);
        
        cout << "expanded matches:" << endl;
        for(m_iter=all_matches.begin(); m_iter!=all_matches.end(); ++m_iter){
            print(*m_iter);
            global_matches.push_back(*m_iter);
        }
        cout << endl << endl;
    }
    
    sort(global_matches.begin(), global_matches.end(), comp_match);
    
    cout << "all possible matches: " << endl;
    
    bool match_valid;
    for(m_iter=global_matches.begin(); m_iter!=global_matches.end(); ++m_iter){
        print(*m_iter);
        
        match_valid=true;
        for(vector<int>::iterator index=(*m_iter).indices.begin(); index!=(*m_iter).indices.end(); ++index){
            if(!available[*index]){
                match_valid=false;
                break;
            }
        }
        if(!match_valid)
            continue;
        covers.push_back(*m_iter);
        for(vector<int>::iterator index=(*m_iter).indices.begin(); index!=(*m_iter).indices.end(); ++index)
            available[*index]=false;
    }

    cout << "covers: " << endl;
    for(m_iter=covers.begin(); m_iter<covers.end(); ++m_iter){
        print(*m_iter);
        total_energy+=(*m_iter).energy;
    }

    return total_energy;
}

double correction_factors(Graph& g){
    double energy=ORIGIN;
    
    //hydrocarbon
    VertexIter vi, vi_end;
    tie(vi, vi_end)=vertices(g);
    bool hydrocarbon=true;
    for(; vi!=vi_end; ++vi){
        if(g[*vi].type!=atomic_numbers["C"] &&
           g[*vi].type!=atomic_numbers["H"]){
            hydrocarbon=false;
            break;
        }
    }
    energy+=hydrocarbon?MOD_HYDROCARBON:0;
    
    cout << "applying initial correction factors:" << endl;
    cout << "origin is " << ORIGIN << endl;
    if(hydrocarbon)
        cout << "hydrocarbon: " << MOD_HYDROCARBON << endl;
    
    return energy+find_rings(g);
}

vector<MatchSet> find_matches(MolData fgroup, Graph& molecule, Matrix& beta, bool check_availability, bool check_ions){
    vector<MatchSet> matches;
    Graph fg_graph=moldata_to_graph(fgroup);
    Matrix alpha=graph_to_mat(fg_graph), M0=gen_M0(alpha, beta, fg_graph, molecule, check_availability, check_ions), current;
    cout << "M0 for " << fgroup.name << ":" << endl;
    print(M0);
    
    MatGen mg(M0);
    if(!fgroup.bond_match)
        one_matrix(alpha);
    
    while(mg.has_next()){
        current=mg.get();
        mg.next();
        Matrix C=current*beta;
        C=current*(C.t());
        if(!fgroup.bond_match)
            one_matrix(C);
        if(SP(C, alpha)==SP(alpha, alpha)){
            //test for coverage, SP=elementwise product
            //alpha is multipled with itself to account for any values greater than
            //one matching and thus being squared
            MatchSet ms;
            ms.indices=matches_as_indices_main(current, fg_graph);
            ms.original_indices=matches_as_indices_fgroup(current);
            ms.energies=fgroup.energies;
            matches.push_back(ms);
        }
    }
    
    cout << mg.num_generated << " primes tested" << endl;
    return matches;
}

//takes a SORTED list and returns a new one without any duplicates
vector<MatchSet> remove_duplicates(vector<MatchSet> v){
    //removing from the middle of a vector is clunky and slow, using a new vector
    //is probably superior
    if(v.size()==0)
        return vector<MatchSet>(v);
    sort(v.begin(), v.end(), comp_matchset);
    vector<MatchSet> v_unique;
    v_unique.push_back(v.front());
    for(vector<MatchSet>::iterator i=v.begin()+1; i<v.end(); ++i){
        if(!equal_matchset(*i, v_unique.back()))
            v_unique.push_back(*i);
    }
    return v_unique;
}

vector<Match> expand_matches(vector<MatchSet> sets, Graph g){
    vector<Match> matches;
    MatchSet ms;
    
    for(vector<MatchSet>::iterator ms_iter=sets.begin(); ms_iter!=sets.end(); ++ms_iter){
        ms=(*ms_iter);
        cout << "expanding ";
        print(ms);
        
        Match m;
        m.priority=ms.energies[KW_DEFAULT_ENERGY].priority;
        m.energy=ms.energies[KW_DEFAULT_ENERGY].energy==DBL_MAX?NA_ENERGY_VALUE:ms.energies[KW_DEFAULT_ENERGY].energy;
        m.indices=ms.indices;
        m.original_indices=ms.original_indices;
        matches.push_back(m);
        
        bool match;
        string emap_key, graph_tag_key;
        int i, config_value, graph_value;
        ModConfig mc;
        for(EnergyMap::iterator emi=ms.energies.begin(); emi!=ms.energies.end(); ++emi){
            if((*emi).first==KW_DEFAULT_ENERGY)
                continue;
            
            emap_key=(*emi).first;
            mc=(*emi).second;
            
            match=true;
            //chop off the differentiating integer, it doesn't exist in the nodes' tags map
            graph_tag_key=emap_key.substr(0, emap_key.find_last_of(':'));
            cout << "trying " << emap_key << " (" << graph_tag_key << ")" << endl;
            print(mc, ms.original_indices.size());
            i=0;
            //original indices includes the wildcards and original ordering so it has a 1:1
            //correspondence: original_indices[i] is the index in the main graph that the
            //ith atom in the fgroup got matched to
            //as a side effect this prioritizes better defined fgroups over those with
            //more wildcards even if they match the same atoms because indices is longer
            for(vector<int>::iterator index=ms.original_indices.begin(); index<ms.original_indices.end(); ++index, ++i){
                cout << "graph index " << *index << " -> " << g[*index].tags[graph_tag_key] << endl;
                //accessing an element that doesnt exist makes a new one, which is good for this
                //as it is initialized to zero as not having it there at all would imply
                config_value=mc.config[i];
                graph_value=g[*index].tags[graph_tag_key];
                
                //broken up for readability
                if(graph_value>0){
                    if(config_value!=MOD_ZERO_MORE_VALUE && config_value!=MOD_ONE_MORE_VALUE){
                        if(config_value==graph_value){
                            if(exception_match(mc.exceptions, g[*index].tags)){
                                match=false;
                                break;
                            }
                        }
                        else{
                            match=false;
                            break;
                        }
                    }
                }
                else if(config_value!=MOD_ZERO_MORE_VALUE && config_value!=0){
                    match=false;
                    break;
                }
            }
            if(match){
                cout << "valid configuration!" << endl << endl;
                Match m;
                m.priority=mc.priority;
                m.energy=mc.energy;
                m.indices=ms.indices;
                m.original_indices=ms.original_indices;
                matches.push_back(m);
            }
            else
                cout << "not valid" << endl << endl;
        }
    }
    return matches;
}

//replace all nonzero elements by one (equivalent to elementwise division with self)
void one_matrix(Matrix& m){
    for(int row=0; row<m.Nrows(); ++row){
        for(int col=0; col<m.Ncols(); ++col)
            m[row][col]=m[row][col]==0?0:1;
    }
}
