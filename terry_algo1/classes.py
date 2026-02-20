"""
Abstract data types of the tiles and the plane.

"""

class Tile:
    """
    A tile.

    Attributes:
        north, east, south, west: sides of the tile
    """
    def __init__(self,
                 north: int,
                 east: int,
                 south: int,
                 west: int):
        
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
    def __init__(self,
                 width: int,
                 height: int,
                 tile_set: list[Tile]):
        assert(width > 0 and height >0)
        self.width = width
        self.height = height
        self.tile_set = tile_set

        self.board = [["X" for i in range(width)] for j in range(height)]

    @classmethod
    def from_minor_plane(cls, 
                         plane):
        """
        Constructs a plane object of size N+1 given a smaller plane of size N. Specifically, it puts the 
        smaller plane in the lower left corner of the new plane.
        
        Args:
            plane: The smaller plane of size N

        Returns:
            None
        """
        assert plane.width == plane.height
        # Create new plane with same dimensions and tile_set
        new_plane = cls(plane.width+1, plane.height+1, plane.tile_set)

        for row_index, row in enumerate(plane.board):
            for col_index, value in enumerate(row):
                new_plane.board[row_index + 1][col_index] = value

        return new_plane

    def __str__(self):
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += self.board[i][j]
                if j != self.width - 1:
                    out += ','
            if i != self.height - 1:
                out += '\n'
        return out

    def insert(self,
               x: int,
               y: int,
               tile_idx: int):
        """
        Insert the tile with given index at the given location

        Args:
            x: The position in the horizontal direction
            y: The position in the vertical direction

        Returns:
            None
        """
        assert self._check_within_bounds(x, y)
        if self._check_is_valid_insertion(x, y, tile_idx):
            self.board[y][x] = str(tile_idx)
            return True
        return False

    def remove(self,
               x: int,
               y: int):
        """
        Removes the tile at given location by replacing it with the symbol that indicates an empty location
        
        Args:
            x: The position in the horizontal direction
            y: The position in the vertical direction

        Returns:
            None
        """
        assert self._check_within_bounds(x, y)
        self.board[y][x] = 'X'

    def _check_is_valid_insertion(self, x: int,
                                  y: int,
                                  tile_idx: int) -> bool:
        """
        Checks if the current insertion is a valid insertion
        
        Args:
            x: The position in the horizontal direction
            y: The position in the vertical direction
            tile_idx: The index of the tile to be inserted

        Returns:
            True if the insertion was valid; false otherwise

        """
        board = self.board
        width = self.width
        height = self.height
        tile_set = self.tile_set


        to_place_tile = tile_set[tile_idx]
        if y - 1 >= 0 and board[y-1][x] != "X":
            if tile_set[int(board[y-1][x])].south != to_place_tile.north:
                return False

        if y + 1 < height and board[y + 1][x] != "X":
            if tile_set[int(board[y + 1][x])].north != to_place_tile.south:
                return False

        if x - 1 >= 0 and board[y][x - 1] != "X":
            if tile_set[int(board[y][x - 1])].west != to_place_tile.east:
                return False

        if x + 1 < width and board[y][x + 1] != "X":
            if tile_set[int(board[y][x + 1])].east != to_place_tile.west:
                return False

        return True

    def _check_within_bounds(self,
                             x: int,
                             y: int) -> bool:
        """
        Checks whether the given location is whitin the bounds of the board

        Args:
            x: The position in the horizontal direction
            y: The position in the vertical direction
        
        Returns:
            True if (x,y) falls within the board
        """
        assert(0 <= x < self.width and 0 <= y < self.height)
        return True
