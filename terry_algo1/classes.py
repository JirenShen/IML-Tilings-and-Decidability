class Tile:
    def __init__(self, north: int, east: int, south: int, west: int):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        
    def __str__(self):
        return f"N{self.north} E{self.east} S{self.south} W{self.west}"

class Plane:
    """
    A plane. Mimics a square of size n in which we can insert tiles.

    Attributes:
        width: The width of the board
        height: The height of the board
        tile_set: The tile set used to tile the plane
        board: Stores the information about where each tile is place on the plane
    """
    def __init__(self, width: int, height: int, tile_set: list[Tile]):
        assert(width > 0 and height >0)
        self.width = width
        self.height = height
        self.tile_set = tile_set

        self.board = [["X" for i in range(width)] for j in range(height)]
    
    def __str__(self):
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += self.board[i][j]
            out += '\n'
        return out

    def insert(self, x: int, y: int, tile_idx: int):
        assert(self._check_within_bounds(x, y))
        
        if self._check_is_valid_insertion(x, y, tile_idx):
            self.board[y][x] = str(tile_idx)
        else:
            print(f'Tile {tile_idx} at ({x},{y})' + " is not valid placement")
    
    def _check_is_valid_insertion(self, x: int, y: int, tile_idx: int):
        to_place_tile = self.tile_set[tile_idx]
        if y - 1 >= 0 and self.board[x][y-1] != "X":
            #Look at the south of the top tile. Does it match the north of the tile we want to place?
            if self.tile_set[int(self.board[x][y-1])].south != to_place_tile.north:
                return False

        if y + 1 < self.height and self.board[x][y + 1] != "X":
            if self.tile_set[int(self.board[x][y + 1])].north != to_place_tile.south:
                return False

        if x - 1 >= 0 and self.board[x - 1][y] != "X":
            if self.tile_set[int(self.board[x - 1][y])].west != to_place_tile.east:
                return False
  
        if x + 1 < self.width and self.board[x + 1][y] != "X":
            if self.tile_set[int(self.board[x + 1][y])].east != to_place_tile.west:
                return False
        return True

    def _check_within_bounds(self, x: int, y: int):
        assert(x < self.width and x >= 0 and y < self.height and y >= 0)
        return True
