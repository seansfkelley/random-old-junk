#include "rings.h"

double find_rings(Graph& molecule){
    vector<Ring> all_rings, unique_rings, valid_rings;
    VertexIter vi, vi_end;
    Ring r;
    tie(vi, vi_end)=vertices(molecule);
    for(; vi!=vi_end; ++vi)
        ring_search_rec(molecule, (int)(*vi), -1, r, all_rings, 1);
    
    if(all_rings.size()==0)
        return 0;
    
    sort(all_rings.begin(), all_rings.end(), ring_comp);
    
    unique_rings.push_back(all_rings[0]);
    for(int i=1; i<all_rings.size(); ++i){
        //cout << "checking " << i << endl;
        if(!equal_rings(unique_rings.back(), all_rings[i]))
            unique_rings.push_back(all_rings[i]);
    }
    
    cout << endl << "all rings:" << endl;
    for(vector<Ring>::iterator i=all_rings.begin(); i!=all_rings.end(); ++i){
        print(*i);
        cout << endl;
    }
    
    cout << endl << "unique rings:" << endl;
    for(vector<Ring>::iterator i=unique_rings.begin(); i!=unique_rings.end(); ++i){
        print(*i);
        cout << endl;
    }
    
    //to eliminate small rings contained in large ones
    bool valid;
    vector<int> intersect;
    for(int test=unique_rings.size()-1; test>0; --test){
        cout << "testing ";
        print(unique_rings[test]);
        cout << endl;
        valid=true;
        for(int i=0; i<test; ++i){
            cout << "against ";
            print(unique_rings[i]);
            intersect.clear();
            set_intersection(unique_rings[test].indices.begin(), unique_rings[test].indices.end(),
                             unique_rings[i].indices.begin(), unique_rings[i].indices.end(),
                             insert_iterator<vector<int> >(intersect, intersect.begin()));
            cout << " -> intersection is ";
            print(intersect);
            cout << endl;
            if(intersect.size()==unique_rings[i].indices.size() &&
               equal(intersect.begin(), intersect.end(), unique_rings[i].indices.begin())){
                valid=false;
                break;
            }
        }
        if(valid){
            valid_rings.push_back(unique_rings[test]);
            cout << "accepted" << endl;
        }
        else
            cout << "rejected" << endl;
    }
    
    //first is unique and smallest, so it must be valid and is never tested
    valid_rings.push_back(unique_rings[0]);
    
    double ring_energies=0;
    bool hetero;
    int double_bonds, previous;
    
    cout << endl << "valid (tagged) rings:" << endl;
    for(vector<Ring>::iterator ring=valid_rings.begin(); ring!=valid_rings.end(); ++ring){
        hetero=false;
        double_bonds=0;
        previous=(*ring).indices.back(); //compare the first to the last the first time around
        for(vector<int>::iterator index=(*ring).indices.begin(); index!=(*ring).indices.end(); ++index){
            molecule[*index].tags[RING_MODIFIER]+=1;
            if(molecule[*index].type==atomic_numbers["N"] ||
               molecule[*index].type==atomic_numbers["O"] ||
               molecule[*index].type==atomic_numbers["S"])
                hetero=true;
            if(molecule[edge(*index, previous, molecule).first].strength==2)
                double_bonds++;
            previous=*index;
        }
        if((double_bonds*2-2)%4==0)//huckel's rule
            (*ring).aromatic=true;
        print(*ring);
        cout << endl;
        if((*ring).aromatic){
            for(vector<int>::iterator index=(*ring).indices.begin(); index!=(*ring).indices.end(); ++index)
                molecule[*index].tags[AROMATIC_MODIFIER]+=1;
            ring_energies+=MOD_AROMATIC;
            cout << "aromatic: " << MOD_AROMATIC << endl;
            if(hetero){
                ring_energies+=MOD_HETEROAROMATIC;
                cout << "heteroaromatic: " << MOD_HETEROAROMATIC << endl;
            }
        }
        cout << endl;
    }
    
    return ring_energies;
}

//casting vertices to ints may be dangerous, but the alternative - iterating through
//the number of vertices until a match of v=Vertex(index) is found - is bulky
//ints are faster, and Vertex== doesn't seem to work consistently
void ring_search_rec(Graph& g, int origin, int current, Ring cur_ring, vector<Ring> &all_rings, int depth){
    if(depth>RING_MAX_SIZE)
        return;
    if(current==-1)
        current=origin;
    cur_ring.indices.push_back(current);
    
    int aro_strength;
    bool aromatic;
    
    AdjVertexIter avi, avi_end;
    tie(avi, avi_end)=adjacent_vertices(current, g);
    for(; avi!=avi_end; ++avi){
        if(find(cur_ring.indices.begin(), cur_ring.indices.end(), (int)(*avi))==cur_ring.indices.end()){//current not in cur_ring
            //cout << (*avi) << " not in ";
            //print(cur_ring);
            //cout << endl;
            Ring new_current;
            new_current.indices=vector<int>(cur_ring.indices);
            ring_search_rec(g, origin, (int)(*avi), new_current, all_rings, depth+1);
        }
        else if((int)(*avi)==origin && depth>2){
            Ring match;
            match.indices=vector<int>(cur_ring.indices);
            //check for aromaticy BEFORE it's sorted
            aro_strength=g[edge(cur_ring.indices[0], cur_ring.indices[1], g).first].strength;
            match.aromatic=true;
            for(int i=1; i<cur_ring.indices.size()-1; ++i){
                //2-1-2-1... alternator
                aro_strength=3-aro_strength;
                if(g[edge(cur_ring.indices[i], cur_ring.indices[i+1], g).first].strength!=aro_strength){
                    match.aromatic=false;
                    break;
                }
            }
            if(g[edge(cur_ring.indices[0], cur_ring.indices[cur_ring.indices.size()-1], g).first].strength!=3-aro_strength)
                match.aromatic=false;
            sort(match.indices.begin(), match.indices.end());
            all_rings.push_back(match);
        }
    }
}

bool ring_comp(Ring first, Ring second){
    if(first.indices.size()!=second.indices.size())
        return first.indices.size()<second.indices.size();
    return lexicographical_compare(first.indices.begin(), first.indices.end(),
                                   second.indices.begin(), second.indices.end());
}

bool equal_rings(Ring one, Ring two){
    return one.indices.size()==two.indices.size() && equal(one.indices.begin(), one.indices.end(),
                                                           two.indices.begin());
}
