/* 
 * File:   main.cpp
 * Author: davidmuchene
 *
 * Created on September 19, 2017, 9:04 PM
 */

#include <cstdlib>
#include <unordered_map>
#include <vector>
#include <iostream>

using namespace std;



// a->b a->c a->d | d->c
// {'a': ['b', 'c', 'd'] } 
template <class T>
std::vector<T> topological_sort(unordered_map<T, vector<T>> graph) {
    vector<T> no_indeg;
    vector<T> sorted;
    unordered_map<T, int> indeg;
    for(auto& node : graph){
        int num_nodes = indeg[node.first];
        for(auto& neighbor : node.second) {
            indeg[neighbor] = indeg[neighbor]+1;
        }
    }
    
    for(auto& node: indeg) {
        if(node.second == 0) {
            no_indeg.push_back(node.first);
        }
    }
    
    while(no_indeg.size()) {
        T val = no_indeg.back();
        no_indeg.pop_back();
        sorted.push_back(val);
        for(auto& neighbor: graph[val]) {
            indeg[neighbor] = indeg[neighbor] -1; 
            if(indeg[neighbor] == 0) {
                no_indeg.push_back(neighbor);
            }
        }
    }

    return sorted; 
}

/*
 * 
 */
int main(int argc, char** argv) {
    unordered_map<string, vector<string> >  g; 
    g["a"] = {"b","c","d"};
    g["d"] = {"c", "b" };
    g["c"] = {"b"};
    
    for(auto& node : topological_sort(g)) {
        cout << node << endl;
    }
    return 0;
}

