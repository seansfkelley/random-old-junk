#include "driver.h"

map<string, int> atomic_numbers;
map<int, int> max_bonds;
bool *available;

int main(int argc, char* argv[]){
    if(argc<3){
        cout << "Requires molecule and fgroup files." << endl;
        exit(0);
    }
    
    init_atomic_numbers();
    init_max_bonds();
    
    MolData pd=parse_molfile(string(argv[1]));
    
    long t=time(NULL);
    cout << "energy for " << argv[1] << "=" << process_molecule(pd, string(argv[2]));
    //prints zero if these are one statement; calculated right to left
    cout << " calculated in " << time(NULL)-t << " seconds" << endl;
}  
