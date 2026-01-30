class Tile:
    def __init__(self, north: int, east: int, south: int, west: int):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        
    def __str__(self):
        return f"N{self.north} E{self.east} S{self.south} W{self.west}"

