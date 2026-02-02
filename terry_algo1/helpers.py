import random
from pathlib import Path

def generate_n_tiles_at_random(n: int):
    """
    Generates n tiles at random and writes it out into a file named input_tileset.xml

    Args:
        a (int): Number of tiles to generate

    Returns:
        None
    """
    print(Path(__file__).parent)
    file_path = Path(__file__).parent / 'input_tileset.xml'
    with open(file_path, 'w', encoding='utf-8') as file:
        for i in range(n):
            N = random.randint(1, 4)
            E = random.randint(1, 4)
            S = random.randint(1, 4)
            W = random.randint(1, 4)
            file.write(str(f'N{N} E{E} S{S} W{W}'))
            if i != n-1:
                file.write('\n')