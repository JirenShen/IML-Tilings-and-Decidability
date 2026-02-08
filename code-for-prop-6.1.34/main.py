import tiles

if __name__ == "__main__":
    instructions = "Input next to view square tilings of n+1 size found by algorithm."

    # 11-tile 4-color aperiodic tile set of Jendel-Rao;
    # Reference: https://amathr.org/an-aperiodic-set-of-eleven-wang-tiles/
    tileset = [
        (1, 2, 3, 2),
        (4, 4, 1, 2),
        (2, 3, 2, 4),
        (3, 1, 2, 1),
        (1, 1, 3, 1),
        (3, 3, 2, 3), 
        (2, 4, 1, 3),
        (1, 3, 1, 2),
        (2, 2, 2, 4),
        (1, 2, 1, 4),
        (2, 4, 4, 4)
        ]
    tilings = tiles.Tilings()
    tilings.tiles = tileset

    print(instructions)

    while (True):
        command = input()

        if command == "exit":
            exit(0)

        if command == "dub":
            tilings.findDoubledSquareTilings()
            print(tilings.square_tilings[-1])
            continue

        n = 1
        if command.isnumeric():
            n = int(command)
        
        for i in range(n):
            tilings.findLargerByOneSquareTilings()

        print(tilings.square_tilings[-1])
        