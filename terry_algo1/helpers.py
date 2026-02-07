"""
Helper functions
"""

import random
from pathlib import Path
import hashlib
import os
import classes


def hash_file(filename, algorithm='sha256'):
    """
    Calculates the hash of a file using a specified algorithm.
    Returns the hexadecimal digest of the hash.
    """
    try:
        with open(filename, 'rb') as f:
            digest = hashlib.file_digest(f, algorithm)
        return digest.hexdigest()
    except FileNotFoundError:
        return "File not found"
    except ValueError as e:
        return f"Error: {e}"

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
                                 tiles: list[classes.Tile]):
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
    file_path = Path(__file__).parent / 'valid_tilings' / f'valid_tilings_of_size_{size}.xml'

    with open(file_path, 'a+', encoding='utf-8') as file:
        for i in range(len(tiles)):
            plane = classes.Plane(1,1, tiles)
            plane.insert(0,0,i)
            content = str(plane)
            file.write(content)
            file.write('\n')

    return file_path
    
def read_tiling_file(file_path: Path, 
                     tile_set: list[classes.Tile]) -> list[classes.Plane]:
    """
    Reads a file which we store all the valid tilings of a plane

    Returns a list of valid tilings as a list of plane objects

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
            if line == '':
                planes.append(convert_str_format_to_plane_object(current_plane, len(current_plane[0]), tile_set))
            else:
                current_plane.append(line.strip())
    return planes

def convert_str_format_to_plane_object(tile_str_format: list[str],
                                       size: int,
                                       tile_set: list[classes.Tile]):
    """

    Converts a txt file storing the valid tilings into a list of plane (tilings) objects

    """
    plane = classes.Plane(size, size, tile_set)
    for index_row, line in enumerate(tile_str_format):
        for index_col in range(size):
            plane.insert(index_col, index_row, int(line[index_col]))
    return plane
