"""
Entry point
"""

from pathlib import Path
from helpers import read_from_tileset_file, find_valid_tilings_of_square

if __name__ == "__main__":
    tile_set_path = Path(__file__).parent / 'input_tileset' / 'input_tileset.txt'
    tile_set = read_from_tileset_file(tile_set_path)

    find_valid_tilings_of_square(7, tile_set)