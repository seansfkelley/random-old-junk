#include "molfile.h"

//is there a way to init the map without needing to do this type of thing?
void init_atomic_numbers(){
    for(int i=0; i<NUM_ELEMENTS; ++i)
        atomic_numbers[elem_symbols[i]]=i+1;
    atomic_numbers[WILDCARD_STRING]=WILDCARD_VALUE;
}

void init_max_bonds(){
    for(int i=0; i<NUM_ELEMENTS; ++i)
        max_bonds[i+1]=elem_max_bonds[i]==-1?INT_MAX:elem_max_bonds[i];
    max_bonds[WILDCARD_VALUE]=INT_MAX;
}

void print(int *integers, int how_many){
    cout << '[';
    for(int i=0; i<how_many; ++i)
        cout << integers[i] << ", ";
    cout << ']';
}

void print(vector<string> v){
    cout << '[';
    vector<string>::iterator i;
    for(i=v.begin(); i<v.end(); ++i)
        cout << *i << ", ";
    cout << ']';
}

void print(vector<int> v){
    cout << '[';
    vector<int>::iterator i;
    for(i=v.begin(); i<v.end(); ++i)
        cout << *i << ", ";
    cout << ']';
}

void print(vector<int*> v){
    cout << '[';
    vector<int*>::iterator i;
    for(i=v.begin(); i<v.end(); ++i)
        cout << "(" << (*i)[0] << ", " << (*i)[1]<< ", " << (*i)[2] << "), ";
    cout << ']' << endl;
}

void print(Matrix m){
    cout << setw(1) << setprecision(0) << m << setprecision(6);
}

void print(Match m){
    cout << m.priority << " (E=" << m.energy << "): ";
    print(m.indices);
    cout << "/";
    print(m.original_indices);
    cout << endl;
}

void print(MatchSet mi){
    print(mi.indices);
    cout << "/";
    print(mi.original_indices);
    cout << endl;
}

void print(ModConfig mc, int num_atoms){
    cout << "config (" << hex << mc.config << dec <<"): ";
    if(mc.config==NULL)
        cout << "N/A" ;
    else
        print(mc.config, num_atoms);
    cout << " with E=" << mc.energy << "; ";
    print(mc.exceptions);
    cout << endl;
}

void print(MolData md){
    cout << md.name << ": ";
    print(md.atoms);
    cout << " (";
    print(md.atoms_no_wildcards);
    cout << "); +-";
    print(md.charges);
    cout << endl;
}

void print(Ring r){
    cout << "ring[" << (r.aromatic?'Y':'N') << "]: ";
    print(r.indices);
}

void print(map<string, int> tags){
    for(map<string, int>::iterator i=tags.begin(); i!=tags.end(); ++i)
        cout << (*i).first << ": " << (*i).second << endl;
}

//this seriously doesnt exist in the STL? maybe replace with the boost tokenizer
vector<string> split(string s, char delim){
    vector<string> v;
    string temp;
    int index=0, prev_index=0;
    while((index=s.find(delim, index))!=string::npos){
        temp=s.substr(prev_index,index-prev_index);
        prev_index=++index;
        if(temp!="")
            v.push_back(temp);
    }
    v.push_back(s.substr(prev_index, string::npos));
    return v;
}

int atoi(string s){
    return atoi(s.c_str());
}

double atof(string s){
    return atof(s.c_str());
}

//returns empty string normally, modifer name if the molfile is a modifer type
MolData parse_molfile(string filename){
    MolData pd;

    ModConfig temp_mc;
    temp_mc.config=NULL;
    temp_mc.energy=DBL_MAX;
    temp_mc.priority=INT_MAX;
    pd.energies[KW_DEFAULT_ENERGY]=temp_mc;
    
    ifstream f;
    f.open(filename.c_str());
    
    if(!f.is_open()){
        cout << "Error opening file \'" << filename << "\'" << endl;
        exit(0);
    }
    
    //.smol is my new extension for simple molfile, doesnt carry positional info
    //for atoms, hence the change of index
    bool is_smol=filename.length()>5 && filename.substr(filename.length()-5, 5)==".smol";
    int w_index=is_smol?0:3;
    
    string s;
    vector<string> tokens;
    vector<int*> configs;
    int *temp_atom;
    
    getline(f, s);
    tokens=split(s, ' ');
    const int num_atoms=atoi(tokens[0]), num_bonds=atoi(tokens[1]);
    const int variants=is_smol?atoi(tokens[2]):0;
    if(is_smol){
        for(int i=0; i<variants; ++i)
            configs.push_back(new int[num_atoms]);
    }
    
    int temp_number;
    
    //process the atom block
    for(int i=0; i<num_atoms && !f.eof(); ++i){ 
        getline(f,s);
        if(s==""){
            --i;
            continue;
        }
        tokens=split(s, ' ');
        temp_number=atomic_numbers[tokens[w_index]];
        pd.atoms.push_back(temp_number);
        if(temp_number!=WILDCARD_VALUE)
            pd.atoms_no_wildcards.push_back(temp_number);
        if(is_smol){
            pd.charges.push_back(atoi(tokens[1]));
            for(int j=0; j<variants; ++j){
                if(tokens[j+2]==MOD_ZERO_MORE_STRING)
                    configs[j][i]=MOD_ZERO_MORE_VALUE;
                else if(tokens[j+2]==MOD_ONE_MORE_STRING)
                    configs[j][i]=MOD_ONE_MORE_VALUE;
                else
                    configs[j][i]=atoi(tokens[j+2]);
            }
        }
        else
            pd.charges.push_back(0);
    }
    
//     for(vector<int*>::iterator i=configs.begin(); i!=configs.end(); ++i){
//         print(*i, num_atoms);
//         cout << endl;
//     }
    
    //process the bond block
    for(int i=0; i<num_bonds && !f.eof(); ++i){
        getline(f,s);
        if(s==""){
            --i;
            continue;
        }
        tokens=split(s, ' ');
        temp_atom=new int[3];
        temp_atom[0]=atoi(tokens[0]);//first index
        temp_atom[1]=atoi(tokens[1]);//second index
        temp_atom[2]=atoi(tokens[2]);//strength
        pd.bonds.push_back(temp_atom);
    }
    
    //process remaining directives
    pd.modifier="";
    pd.bond_match=true;
    pd.correction=false;
    while(!f.eof()){
        getline(f,s);
        if(s=="") continue;
        tokens=split(s, ' ');
        if(tokens[1]==KW_DEFAULT_ENERGY){
            pd.energies[KW_DEFAULT_ENERGY].energy=atof(tokens[3]);
            pd.energies[KW_DEFAULT_ENERGY].priority=atoi(tokens[2]);
        }
        else if(tokens[1]==KW_ALT_ENERGY){
            ModConfig mc;
            mc.priority=atoi(tokens[2]);
            //indexing starts at one in molfiles
            mc.config=configs[atoi(tokens[4])-1];
            mc.energy=atof(tokens[5]);
            for(int i=6; i<tokens.size(); ++i)
                mc.exceptions.push_back(tokens[i]);
            pd.energies[tokens[3]+":"+tokens[4]]=mc;
            
        }
        else if(tokens[1]==KW_MODIFIER)
            pd.modifier=tokens[2];
        else if(tokens[1]==KW_NO_BOND_MATCH)
            pd.bond_match=false;
        else if(tokens[1]==KW_CORRECTION)
            pd.correction=true;
    }
    
    cout << filename << ":" << endl;
    for(EnergyMap::iterator i=pd.energies.begin(); i!=pd.energies.end(); ++i){
        cout << (*i).first << ": ";
        print((*i).second, num_atoms);
    }
    cout << endl;
    
    f.close();
    
    cout << "MolData:" << endl;
    print(pd);
    
    return pd;
}
