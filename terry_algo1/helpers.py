"""
Helper functions
"""
import copy
import pprint
import random
from pathlib import Path
import os
from classes import Plane, Tile

def generate_n_tiles_at_random(number_of_tiles: int):
    """
    Generates n tiles at random and writes it out into a file named input_tileset.txt

    Args:
        number_of_tiles: Number of tiles to generate

    Returns:
        None
    """
    out = ""
    for i in range(number_of_tiles):
        N = random.randint(1, 4)
        E = random.randint(1, 4)
        S = random.randint(1, 4)
        W = random.randint(1, 4)
        out += str(f'N{N} E{E} S{S} W{W}')
        if i != number_of_tiles-1:
            out += '\n'

    if not os.path.exists('input_tileset'):
        os.mkdir('input_tileset')

    file_path = Path(__file__).parent / 'input_tileset' / 'input_tileset.txt'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(out)
    
    return file_path

def find_valid_tilings_of_square(size: int, 
                                 tiles: list[Tile]):
    """
    Finds the valid tilings of size n given a tile set.

    Reads precomputed values stored in text files if it exists

    Otherwise recursively computes the valid tilings

    Stores the result into a txt file
    
    Args:
        size: the size of the plane which we want to find tilings for
        tile_set: the list of valid tiles
    
    Returns:
        None
    """
    if not os.path.exists('valid_tilings'):
        os.mkdir('valid_tilings')

    if size > 1:
        file_path = Path(__file__).parent / 'valid_tilings' / f'valid_tilings_of_size_{size}.txt'
        if file_path.exists():
            print('Results have already been computed')
            return file_path
        else:
            file_path_minor = find_valid_tilings_of_square(size-1, tiles)
            valid_tilings_of_minor = read_from_tiling_file(file_path_minor, tiles, size-1)
            valid_tilings = []
            valid_tilings_converted = []
            for plane in valid_tilings_of_minor:
                enlarged_plane = Plane.from_minor_plane(plane)
                valid_tilings += recursively_enumerate_tiles_of_the_plane(enlarged_plane, 0,0, tiles)
            
            print_board(valid_tilings, file_path)
            return file_path
            
    else:
        file_path = Path(__file__).parent / 'valid_tilings' / f'valid_tilings_of_size_{size}.txt'
        planes = []
        for tile_idx in range(len(tiles)):
            plane = Plane(1,1, tiles)
            plane.insert(0, 0, tile_idx)
            planes.append(plane)

        write_to_tiling_file(planes, file_path)
        return file_path

def write_to_tiling_file(planes: list[Plane], file_path: Path ):
    """
    Writes the tilings inputted as a parameter into the file specified by the file_path

    Args:
        planes: list of planes/tilings we want to write into the file
        file_path: the path of the file
    """
    with open(file_path, 'w+', encoding='utf-8') as file:
        for plane in planes:
            print(str(plane), file=file)
            print('', file=file)

def read_from_tileset_file(file_path: Path) -> list[Tile]:
    """
    Reads from a file containing the tileset

    Args:
        file_path: the path of the file
    
    Returns:
        A list of tile objects
    """
    tiles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('\n')
        for line in content:
            sides = line.split(' ')
            tiles.append(Tile(int(sides[0][1]),
                                    int(sides[1][1]),
                                    int(sides[2][1]),
                                    int(sides[3][1])))
        return tiles

def read_from_tiling_file(file_path: Path, 
                     tile_set: list[Tile], size) -> list[Plane]:
    """
    Reads a file which we store all the valid tilings of a plane

    Returns a list of valid tilings as a list of plane objects

    Assumes file_path exists

    Args:
        file_path: path of the file that is storing the string formatted tilings
        tile_set: the list of valid tiles
    
    Returns:
        a list of planes that are tiled

    """
    with open(file_path, 'r+', encoding='utf-8') as file:
        planes = []
        current_plane = []
        for line in file:
            if line == '\n':
                planes.append(convert_str_format_to_plane_object(current_plane,
                                                                 size,
                                                                 tile_set))
                current_plane = []
            else:
                current_plane.append(line.strip())
        return planes

def convert_str_format_to_plane_object(tile_str_format: list[str],
                                       size: int,
                                       tile_set: list[Tile]):
    """

    Converts a txt file storing the valid tilings into a list of plane (tilings) objects

    """
    plane = Plane(size, size, tile_set)
    for index_row, line in enumerate(tile_str_format):
        current_tile = ''
        current_x = 0
        for char in line:
            if char != ',':
                current_tile += char
            else:
                plane.insert(current_x,index_row, int(current_tile))
                current_x += 1
                current_tile = ''
        plane.insert(current_x,index_row, int(current_tile))
        current_x = 0
        current_tile = ''
    return plane

def recursively_enumerate_tiles_of_the_plane(plane: Plane, 
                                             x: int, y: int, 
                                             tile_set: list[Tile]) -> list[list[str]]:
    valid_tilings = []
    for tile_idx in range(len(tile_set)):
        if not plane.insert(x, y, tile_idx):
            continue
        if x+1 < plane.width:
            valid_tilings += recursively_enumerate_tiles_of_the_plane(plane, x+1, y, tile_set)
        elif y+1 < plane.height:
            valid_tilings += recursively_enumerate_tiles_of_the_plane(plane, x, y+1, tile_set)

        if  x+y+1 == plane.width + plane.height - 1:
            valid_tilings.append(copy.deepcopy(plane.board))
        plane.remove(x, y)
    return valid_tilings
    
def print_board(valid_tilings: list[list[list[str]]], file_path: Path):
    width = len(valid_tilings[0])
    height = width
    with open(file_path, 'w+', encoding='utf-8') as file:
        for tiling in valid_tilings:
            out = ""
            for i in range(height):
                for j in range(width):
                    out += tiling[i][j]
                    if j != width - 1:
                        out += ','
                out += '\n'
                if i == height -1:
                    out += '\n'
            file.write(out)
    