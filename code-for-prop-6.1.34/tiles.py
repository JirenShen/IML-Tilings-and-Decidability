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
        self.num_missing_from_each_side = [0, 0] # denotes num of tiles missing from north and west sides respectively

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

def squaresForm2by2(four_squares_nw_sw_se_ne):
    for i in range(len(four_squares_nw_sw_se_ne)):
        clockwise = (i + 1) % 4
        counter_clockwise = (i - 1) % 4
        if four_squares_nw_sw_se_ne[i-1].square_sides[clockwise] != four_squares_nw_sw_se_ne[i].square_sides[counter_clockwise]:
            return False

    return True


def joinSquaresNeSeSwNw(four_squares_nw_sw_se_ne):
    new_sqr = TilingSquare()
    for i in range(len(four_squares_nw_sw_se_ne)):
        new_sqr.square_sides[i].extend(four_squares_nw_sw_se_ne[i-1].square_sides[i])
        new_sqr.square_sides[i].extend(four_squares_nw_sw_se_ne[i].square_sides[i])
    return new_sqr


class Tilings:
    def __init__(self):
        self.tiles = []
        self.square_tilings = [[TilingSquare()]]

    def findLargerByOneSquareTilings(self):
        if not self.square_tilings[-1]: return # have not found any square tilings of prev size

        worklist = Queue()
        for square in self.square_tilings[-1]:
            self.putSquareWithAddedCornerTiles(square, self.tiles, worklist)

        next_sqr_size = len(self.square_tilings[-1][0].square_sides[0]) + 1
        self.square_tilings.append([])

        while not worklist.empty():
            curr_sq = worklist.get()
            
            # to cover trivial case of forming 1 by 1 square from 0 by 0
            if curr_sq.firstMissingSide() is None:
                self.square_tilings[-1].append(curr_sq)
                continue

            for tile in self.tiles:
                filled_sq = squaresWithTileInserted(curr_sq, tile)

                if filled_sq is None: # does not continue search on invalid tilings
                    continue
                elif filled_sq.firstMissingSide() is None: # is a solution, saves result
                    self.square_tilings[-1].append(filled_sq)
                else: # continues searching on incomplete valid tilings
                    worklist.put(filled_sq)

        # checks if solutions is not empty
        if self.square_tilings[-1]: 
            print(f"Found square tiling of size {next_sqr_size}.")
        else:
            print(f"Failed to find square tilings of size {next_sqr_size}.")

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

    # have not yet observed significant performance benefits
    def findDoubledSquareTilings(self):
        prev_solns = self.square_tilings[-1]
        if not prev_solns: return # have not found any square tilings of prev size

        self.square_tilings.append([])

        for northeast_sqr in prev_solns:
            for southeast_sqr in prev_solns:
                for southwest_sqr in prev_solns:
                    for northwest_sqr in prev_solns:
                        squares = (northeast_sqr, southeast_sqr, southwest_sqr, northwest_sqr)
                        if squaresForm2by2(squares):
                            self.square_tilings[-1].append(joinSquaresNeSeSwNw(squares))

