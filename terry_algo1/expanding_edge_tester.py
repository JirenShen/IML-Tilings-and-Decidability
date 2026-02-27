import expanding_edge

if __name__ == "__main__":
    instructions = "Input next to view square tilings of n+1 size found by algorithm."

    tiles = [(1,2,1,2), (2,1,2,1)]
    test = expanding_edge.Tileset(tiles)

    print(instructions)

    while (True):
        command = input()

        if command == "exit":
            exit(0)

        n = 1
        if command.isnumeric():
            n = int(command)
        
        for i in range(n):
            test.findNextSizeTilings()

        print(test.tilings[-1])