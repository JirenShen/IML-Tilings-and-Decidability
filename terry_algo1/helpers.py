import classes
import random

print("hello world")

def generate_n_tiles_at_random(n: int):
    with open('input_tileset.xml', 'w') as file:
        for i in range(n):
            N = random.randint(1, 4)
            E = random.randint(1, 4)
            S = random.randint(1, 4)
            W = random.randint(1, 4)
            file.write(str(f'N{N} E{E} S{S} W{W}'))
            if i != n-1:
                file.write('\n')
            