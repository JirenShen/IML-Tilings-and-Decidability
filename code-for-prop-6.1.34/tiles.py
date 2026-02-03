from enum import Enum
from queue import Queue
import copy

class Sides(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

NUM_OF_SIDES = 4

def nextSide(n):
    return (n+1) % NUM_OF_SIDES

def oppSide(n):
    return (n + (NUM_OF_SIDES // 2)) % NUM_OF_SIDES

def prevSide(n):
    return (n-1) % NUM_OF_SIDES

def eastWestMatch(tile1, tile2):
    return tile1[Sides.East.value] == tile2[Sides.West.value]

def southNorthMatch(tile1, tile2):
    return tile1[Sides.South.value] == tile2[Sides.North.value]

def parity(n) -> int:
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1

# tileset is a list of tiles
class TilingSquare:
    def __init__(self):
        self.square_sides = ([], [], [], []) # respective color sequences of north, east, south, and west sides
        self.num_missing_from_each_side = [0, 0] # denotes num of tiles missing from north and west sides respectively, pos/neg indicates missing from which end

    def __str__(self):
        return str(self.square_sides) + ", " + str(self.num_missing_from_each_side)
    
    def __repr__(self):
        to_return = str(self.square_sides)
        if not self.firstMissingSide() is None:
            to_return += ", " + str(self.square_sides)
        return to_return
    
    def __eq__(self, other):
        return self.square_sides == other.square_sides and self.num_missing_from_each_side == other.num_missing_from_each_side
    
    def __hash__(self):
        return hash(str(self))
    
    def isPeriodic(self):
        return (self.square_sides[Sides.North.value] == self.square_sides[Sides.South.value]
                and self.square_sides[Sides.East.value] == self.square_sides[Sides.West.value])

    # finds arbitrary side with missing tiles
    def firstMissingSide(self):
        for i in range(len(self.num_missing_from_each_side)):
            if self.num_missing_from_each_side[i]: # != 0
                return i
        return None


# returns None if cannot add tile, otherwise returns tiled_square with new tile
def squaresWithTileInserted(sqr, tile):
    curr_side = sqr.firstMissingSide()
    # has no missing tiles, should not try adding tile in first place
    if curr_side is None: return None
    
    curr_idx = sqr.num_missing_from_each_side[curr_side] - 1
    prev_tile_interfacing_side = 1 - curr_side
    prev_tile_interfacing_idx = len(sqr.square_sides[curr_side]) - 1

    if (tile[oppSide(curr_side)] == sqr.square_sides[curr_side][curr_idx]
            and tile[oppSide(prev_tile_interfacing_side)] == sqr.square_sides[prev_tile_interfacing_side][prev_tile_interfacing_idx]):
        new_sq = copy.deepcopy(sqr)
        new_sq.square_sides[curr_side][curr_idx] = tile[curr_side]
        new_sq.square_sides[prev_tile_interfacing_side][prev_tile_interfacing_idx] = tile[prev_tile_interfacing_side]
        new_sq.num_missing_from_each_side[curr_side] -= 1
        return new_sq
    else:
        return None


class Tilings:
    def __init__(self):
        self.tiles = []
        self.squareTilings = [[TilingSquare()]]

    def findLargerByOneSquareTilings(self):
        if not self.squareTilings[-1]: return # have not found any square tilings of prev size

        worklist = Queue()
        seen_solns = set()
        for square in self.squareTilings[-1]:
            self.putSquareWithAddedCornerTiles(square, self.tiles, worklist)

        next_sqr_size = len(self.squareTilings[-1][0].square_sides[0]) + 1
        self.squareTilings.append([])

        while not worklist.empty():
            curr_sq = worklist.get()
            
            # to cover trivial case
            if curr_sq.firstMissingSide() is None:
                if not curr_sq in seen_solns:
                    self.squareTilings[-1].append(curr_sq)
                    seen_solns.add(curr_sq)
                continue

            for tile in self.tiles:
                filled_sq = squaresWithTileInserted(curr_sq, tile)

                if filled_sq is None or filled_sq in seen_solns: # ignores invalid tiling or previous solution
                    continue
                elif filled_sq.firstMissingSide() is None: # is a solution
                    self.squareTilings[-1].append(filled_sq)
                    seen_solns.add(filled_sq)
                else: # incomplete tiling (work in progress)
                    worklist.put(filled_sq)

        # checks if solutions is not empty
        if self.squareTilings[-1]: 
            print(f"Found square tiling of size {next_sqr_size}.")
        else:
            print(f"Failed to find square tilings of size {next_sqr_size}.")

    # def findDoubledSquareTilings(self): to implement later

    def putSquareWithAddedCornerTiles(self, square, tiles, worklist):
        if not square.firstMissingSide() is None: return # square not tiled

        # only one corner is necessary, so doing Northeast
        old_sqr_size = len(square.square_sides[0])
        for tile in tiles:
            new_sq = copy.deepcopy(square)

            for dir in range(NUM_OF_SIDES):
                new_sq.square_sides[dir].append(tile[dir])

            new_sq.num_missing_from_each_side[0] = old_sqr_size
            new_sq.num_missing_from_each_side[1] = old_sqr_size

            worklist.put(new_sq)
    
