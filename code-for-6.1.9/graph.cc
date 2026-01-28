#include "graph.hpp"


bool Graph::dfs(int u, std::map<int, int>& visited, std::vector<int>& currentPath) {
        visited[u] = 1; 
        currentPath.push_back(u); 

        if (adjList.find(u) != adjList.end()) { //make sure there is edge going out from this node, which means this node is added into the adjlist
            for (auto const& [v, label] : adjList[u]) { //go through all the neighbour
                if (visited[v] == 1) { 
                    bool startRecording = false; //the cyxle starts from v, and ends in v. 
                    for (int node : currentPath) {
                        if (node == v) startRecording = true;
                        if (startRecording) {
                            cyclePath.push_back(node);
                        }
                    }
                    cyclePath.push_back(v); 
                    return true;
                }
                if (visited[v] == 0) {
                    if (dfs(v, visited, currentPath)) {
                        return true; 
                    }
                }
            }
        }

        visited[u] = 2; 
        currentPath.pop_back();
        return false;
    }


void Graph::addEdge(int u, int v, int south, int north) {
        adjList[u][v] = {south, north};
    }


bool Graph::hasCycle() {
        cyclePath.clear(); 
        std::map<int, int> visited;
        std::vector<int> currentPath;

        for (auto const& [node, edges] : adjList) {
            if (visited[node] == 0) {
                if (dfs(node, visited, currentPath)) {
                    return true;
                }
            }
        }
        return false;
    }

std::vector<int> Graph::getCyclePath() const {
        return cyclePath;
    }