# trying to create a new branch, but testing if I did so correctly
from classes import Plane, Tile
from enum import Enum
from queue import Queue

import helpers
import copy

from collections import deque

class Sides(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

NUM_OF_SIDES = 4

def oppSide(n):
    return (n + (NUM_OF_SIDES/2)) % NUM_OF_SIDES


class expandingEdge:
    def __init__(self, sides, missing: list[int], previous):
        self.sides = sides
        self.missing = missing
        self.previous_edge = previous
    
    def __init__(self, previous_edge: expandingEdge, new_corner_tile: int):
        for i in range(NUM_OF_SIDES):
            self.sides[i] = previous_edge.sides[i].copy()
            self.sides[i].append(new_corner_tile)

        self.missing = [len(previous_edge.north_tiles), len(previous_edge.east_tiles)]
        self.previous_edge = previous_edge

    def buildPlane(self, tile_set) -> helpers.Plane: # tile_set information not recoverable from within expandingEdge
        new_plane = helpers.Plane(len(self.north_tiles), len(self.east_tiles), tile_set)
        new_plane.board = self.getTiling()
        return new_plane

    def getTiling(self) -> list[list[int]]:
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
    
    def insertTile(self, tile, side, idx):
        adj_side = NUM_OF_SIDES-side
        side_neighbor = self.sides[side][idx]
        adj_neighbor = self.sides[side][idx+1]

        size = len(self.sides[adj_side])

        if not (tile[oppSide(side)] == side_neighbor[side] and
            tile[oppSide(adj_side)] == adj_neighbor[adj_side]):
            return False
        else:
            adj_neighbor = tile
            self.sides[adj_side][size-1] = tile
            return True


def createExpandingEdgeWithTileInserted(expanding_edge, tile):
    curr_side = getFirstNonzeroIdx(expanding_edge.missing)
    if curr_side is None: return None
    curr_idx = expanding_edge.missing[curr_side]

    new_edge = copy.deepcopy(expanding_edge)
    if new_edge.insertTile(tile, curr_side, curr_idx):
        return new_edge
    else:
        return None


def getFirstNonzeroIdx(arr):
    for i in range(arr):
        if arr[i] != 0:
            return i
    return None


class Tileset:
    def __init__(self, tiles = []):
        self.tiles = tiles
        self.tilings = [expandingEdge([[],[],[],[]], [0,0], None)]
    
    def findNextSizeTilings(self):
        if not self.tilings[-1]: return # have not found any square tilings of prev size
        
        worklist = Queue()
        for tiling in self.tilings[-1]:
            for tile in self.tiles:
                worklist.put(createExpandingEdgeWithTileInserted(tiling, tile))
            
        next_size = len(self.tilings[-1][0].sides[0]) + 1
        self.squareTilings.append([])

        while not worklist.empty():
            curr_edge = worklist.get()

            # check for trivial case of generated n = 1 tilings
            if getFirstNonzeroIdx(curr_edge.missing) is None:
                self.squareTilings[-1].append(curr_edge)
                continue

            for tile in self.tiles:
                next_edge = createExpandingEdgeWithTileInserted(curr_edge, tile)
                if next_edge is None:
                    continue
                elif getFirstNonzeroIdx(next_edge.missing) is None:
                    self.tilings[-1].append(next_edge)
                else:
                    worklist.put(next_edge)
        
        # checks if solutions is not empty
        if self.square_tilings[-1]: 
            print(f"Found square tiling of size {next_size}.")
        else:
            print(f"Failed to find square tilings of size {next_size}.")

