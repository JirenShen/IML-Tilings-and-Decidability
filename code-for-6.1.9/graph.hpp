#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <map>
#include <vector>
#include <utility> 
#include <iostream>
#include <algorithm> 


using EdgeLabel = std::pair<int, int>; //this is to store the edge name, (south, north) of the edge tile

class Graph {
private:
    std::map<int, std::map<int, EdgeLabel>> adjList; //outer key is the west, inner key is the east, inner value is the edgae name.
    std::vector<int> cyclePath;
    //0 as not visited, 1 is currently in stack, 2 is completed
    bool dfs(int u, std::map<int, int>& visited, std::vector<int>& currentPath);

public:
    Graph() = default;
    void addEdge(int u, int v, int south, int north);
    bool hasCycle();
    std::vector<int> getCyclePath() const ;
};

#endif 