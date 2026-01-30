import classes
import helpers



if __name__ == "__main__":
    tiles = []
    helpers.generate_n_tiles_at_random(5)
    with open('input_tileset.xml', 'r') as file:
        content = file.read().split('\n')
        for line in content:
            sides = line.split(' ')
            tiles.append(classes.Tile(int(sides[0][1]), int(sides[1][1]), int(sides[1][1]), int(sides[1][1])))

    

    