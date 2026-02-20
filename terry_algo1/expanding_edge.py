# trying to create a new branch, but testing if I did so correctly
from classes import Plane, Tile
import helpers

from collections import deque 

class expandingEdge:
    def __init__(self, north_edge: list[int], east_edge: list[int], missing: list[int], previous):
        self.north_tiles = north_edge
        self.east_tiles = east_edge
        self.missing = missing
        self.previous_edge = previous
    
    def __init__(self, previous_edge: expandingEdge, new_corner_tile: int):
        self.north_tiles = previous_edge.north_tiles.copy()
        self.north_tiles.append[new_corner_tile]
        self.east_tiles = previous_edge.east_tiles.copy()
        self.east_tiles.append[new_corner_tile]

        self.missing = [len(previous_edge.north_tiles), len(previous_edge.east_tiles)]

        self.previous_edge = previous_edge

    def buildPlane(self, tile_set) -> Plane: # tile_set information not recoverable from within expandingEdge
        new_plane = Plane(len(self.north_tiles), len(self.east_tiles), tile_set)
        new_plane.board = self.getTiling()
        return new_plane

    def getTiling(self) -> list[list[int]]: # 
        tiling = deque()

        lineage = self.getExpandingEdgeLineage()
        while lineage:
            curr_expanding_edge = lineage.popleft()

            # copy east edge tiles
            for i in range(len(tiling)): # avoid duplicating northeast corner tile
                tiling[-1-i].append(curr_expanding_edge.east_tiles[i])
        
            # copy north edge tiles
            tiling.appendleft(curr_expanding_edge.north_tiles)

        # account for missing tiles
        for i in range(self.missing[0]):
            tiling[0][i] = 'X'
        for i in range(self.missing[1]):
            tiling[i][-1] = 'X'

        return list(tiling)

    def getExpandingEdgeLineage(self) -> deque[expandingEdge]:
        lineage = deque()

        curr = self
        lineage.appendleft(curr)
        while (curr.previous_edge is not None):
            curr = curr.previous_edge
            lineage.appendleft(curr)
        return lineage

