# Settings and rules shared by the game modules.

GRID_WIDTH = 30
GRID_HEIGHT = 15

START_LENGTH = 3
START_DELAY = 0.25

SPECIAL_OBJECT_TIME = 10
SPEED_BOOST_TIME = 5

MENU_WIDTH = 40

DIRECTIONS = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0)
}

OPPOSITE_DIRECTION = {
    "w": "s",
    "s": "w",
    "a": "d",
    "d": "a"
}

GAME_OBJECTS = {
    "*": "Apple",
    "G": "Golden",
    "S": "Speed",
    "X": "Poison",
    "F": "Freeze",
    "B": "Bomb"
}
