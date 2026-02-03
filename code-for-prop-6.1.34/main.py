import tiles

if __name__ == "__main__":
    instructions = "Input next to view square tilings of n+1 size found by algorithm."

    tileset = [(1, 1, 1, 1), (2, 2, 2, 2), (1, 2, 1, 2)]
    tilings = tiles.Tilings()
    tilings.tiles = tileset

    print(instructions)

    while (True):
        command = input()
        # if command == "next":
        if command == "exit":
            exit(0)

        n = 1
        if command.isnumeric():
            n = int(command)

        for i in range(n):
            tilings.findLargerByOneSquareTilings()

        print(tilings.squareTilings[-1])
        