"""
Entry point
"""

from classes import Tile, Plane
from helpers import read_from_tileset_file, read_from_tiling_file, find_valid_tilings_of_square, generate_n_tiles_at_random
from pathlib import Path


if __name__ == "__main__":
    tile_set_path = Path(__file__).parent / 'input_tileset' / 'input_tileset.txt'
    # tile_set_path = generate_n_tiles_at_random(11)
    tile_set = read_from_tileset_file(tile_set_path)

    
    find_valid_tilings_of_square(10, tile_set)
    

    # file_path = Path(__file__).parent / 'valid_tilings' / 'valid_tilings_of_size_1.txt'
    # planes = read_from_tiling_file(file_path, tile_set)
    # for plane in planes:
    #     print(plane)
    # helpers.read_output_file('output_tiles/output_size_1.xml')

    
    
    