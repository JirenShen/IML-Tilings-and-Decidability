import classes
import helpers

if __name__ == "__main__":
    tiles = []

    # Generates n tiles at random
    n = 5
    file_name = helpers.generate_n_tiles_at_random(n)

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().split('\n')
        for line in content:
            sides = line.split(' ')
            tiles.append(classes.Tile(int(sides[0][1]),
                                      int(sides[1][1]),
                                      int(sides[1][1]),
                                      int(sides[1][1])))

    # plane = classes.Plane(10,10,tiles)
    # plane.insert(1,1,2)
    # print(plane)
    
    # helpers.find_valid_tilings_of_square(1, tiles)
    # helpers.read_output_file('output_tiles/output_size_1.xml')

    
    
    