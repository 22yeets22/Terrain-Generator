# Constants
WIDTH = 600
NOISE_CHANGE = 60
TILE_SIZE_DEFAULT = 25
MOVE_DIST = 0.3
FPS = 30

# Terrain Generation
HEIGHT_MULT = 0.7
HEIGHT_MAX = 2
HEIGHT_MIN = -2

# Biome definitions with ideal center points (heat, dryness)
BIOMES = {
    "desert": {"center": (0.225, 0.3)},
    "grasslands": {"center": (0.05, 0.1)},
    "rainforest": {"center": (-0.075, -0.425)},
    "arctic": {"center": (-0.5, 0.0)},
    "water": {"height": -0.25},
    "mountain": {"minheight": 0.3, "maxheight": 0.45, "height": 0.375},
    "snow": {"height": 0.45}
}

BIOME_COLORS = {
    "desert": (255, 243, 148),
    "grasslands": (181, 219, 147),
    "rainforest": (30, 143, 30),
    "arctic": (213, 213, 245),
    "water": (69, 115, 222),
    "mountain": (84, 63, 59),
    "snow": (225, 239, 245)
}
