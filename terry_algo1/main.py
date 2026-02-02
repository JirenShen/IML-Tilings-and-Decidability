import classes
import helpers

if __name__ == "__main__":
    tiles = []

    # Generates n tiles at random
    n = 10
    helpers.generate_n_tiles_at_random(n)

    with open('input_tileset.xml', 'r', encoding='utf-8') as file:
        content = file.read().split('\n')
        for line in content:
            sides = line.split(' ')
            tiles.append(classes.Tile(int(sides[0][1]), int(sides[1][1]), int(sides[1][1]), int(sides[1][1])))

    plane = classes.Plane(3,3, tiles)
    plane.insert(0,0,2)
    plane.insert(0,1,2)
    print(plane)
    
    