#include <iostream>
#include "graph.hpp"

int main() {
    Graph g;

    g.addEdge(0, 1, 2, 0);
    g.addEdge(1, 2, 0, 1);
    g.addEdge(2, 0, 1, 1); 
    g.addEdge(2, 3, 0, 0); 

    if (g.hasCycle()) {
      
        std::vector<int> path = g.getCyclePath();
        std::cout << "Cycle Path: ";
        for (size_t i = 0; i < path.size(); ++i) {
            std::cout << path[i];
            if (i < path.size() - 1) std::cout << " -> ";
        }
        std::cout << std::endl;
    } else {
        std::cout << "No cycle found." << std::endl;
    }

    return 0;
}