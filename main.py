import pygame
from perlin_noise import PerlinNoise
import math

# Constants
WIDTH = 600
NOISE_CHANGE = 60
TILE_SIZE_DEFAULT = 25
MOVE_DIST = 0.3
FPS = 30

# Biome definitions with ideal center points (heat, dryness)
BIOMES = {
    "desert": {"center": (0.225, 0.3)},
    "grasslands": {"center": (0.05, 0.1)},
    "rainforest": {"center": (-0.075, -0.425)},
    "arctic": {"center": (-0.5, 0.0)},
    "water": {"height": -0.25},
    "mountain": {"height": 0.325},
    "snow": {"height": 0.7}
}

BIOME_COLORS = {
    "desert": (255, 220, 170),
    "grasslands": (62, 220, 59),
    "rainforest": (0, 128, 0),
    "arctic": (200, 200, 255),
    "water": (0, 0, 255),
    "mountain": (140, 90, 80),
    "snow": (255, 250, 250)
}

def get_seed(raw_seed):
    """Convert raw seed input into a numeric seed."""
    if raw_seed.isdigit():
        return abs(int(raw_seed))
    return sum(ord(char) for char in raw_seed)


def generate_noise(seed):
    """Initialize Perlin noise generators."""
    return {
        "base1": PerlinNoise(octaves=3, seed=seed),
        "base2": PerlinNoise(octaves=8, seed=seed),
        "heatmap": PerlinNoise(octaves=0.75, seed=seed),
        "wetmap": PerlinNoise(octaves=0.6, seed=seed),
    }


def calculate_noise(noise, position):
    """Calculate combined noise for a given position."""
    n1 = noise["base1"](position)
    n2 = noise["base2"](position)
    h = noise["heatmap"](position)
    w = noise["wetmap"](position)
    return (n1 + n2 + (h + w) * 0.4) * 0.6, h, w


def euclidean_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def get_biome_weights(height, heat, dryness):
    """Calculate weights for each biome based on distance to their centers."""
    # First handle height-based biomes
    if height <= BIOMES["water"]["height"]:
        return {"water": 1.0}
    elif height >= BIOMES["snow"]["height"]:
        return {"snow": 1.0}
    elif BIOMES["mountain"]["height"] - 0.1 <= height <= BIOMES["mountain"]["height"] + 0.1:
        return {"mountain": 1.0}

    # Calculate distances to temperature/moisture-based biomes
    point = (heat, dryness)
    distances = {
        biome: euclidean_distance(point, BIOMES[biome]["center"])
        for biome in ["desert", "grasslands", "rainforest", "arctic"]
    }
    
    # Convert distances to weights using inverse square and avoid small values
    total_weight = sum(1 / (d * d + 0.01) for d in distances.values())
    weights = {
        biome: (1 / (dist * dist + 0.01)) / total_weight
        for biome, dist in distances.items() if (1 / (dist * dist + 0.01)) > 0.1
    }

    return weights


def blend_colors(weights):
    """Blend colors based on biome weights."""
    r, g, b = 0, 0, 0
    for biome, weight in weights.items():
        color = BIOME_COLORS[biome]
        r += color[0] * weight
        g += color[1] * weight
        b += color[2] * weight
    return (int(r), int(g), int(b))


def handle_input(keys, velocity, tile_size, delta_time):
    """Process user input for movement and zoom with smooth scrolling."""
    acceleration = 0.1  # Adjust the acceleration for smooth scrolling
    deceleration = 0.9  # Slow down the movement gradually

    # Handle movement based on key presses
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        velocity.y -= acceleration
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        velocity.y += acceleration
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        velocity.x -= acceleration
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        velocity.x += acceleration

    # Apply friction (deceleration) to smooth out the movement
    velocity.x *= deceleration
    velocity.y *= deceleration

    # Handle zoom
    if keys[pygame.K_q] and tile_size >= 19:
        tile_size -= 2
    if keys[pygame.K_e] and tile_size <= 49:
        tile_size += 2

    # Apply movement based on velocity and delta_time
    velocity *= delta_time * 0.1  # Adjust the 0.1 to control scrolling speed

    return velocity, tile_size


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Terrain Generator")
    
    raw_seed = input("Enter a seed: ")
    seed = get_seed(raw_seed)
    noise = generate_noise(seed)
    tile_size = TILE_SIZE_DEFAULT
    position = pygame.Vector2()
    velocity = pygame.Vector2()
    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000.0  # Get delta_time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))
        keys = pygame.key.get_pressed()
        velocity, tile_size = handle_input(keys, velocity, tile_size, delta_time)

        # Update position based on velocity
        position += velocity

        tile_iters = round(WIDTH / tile_size)
        for x in range(tile_iters + 1):
            for y in range(tile_iters + 1):
                currpos = [(x + position.x) / NOISE_CHANGE, (y + position.y) / NOISE_CHANGE]
                height, heat, wet = calculate_noise(noise, currpos)
                
                # Get biome weights and blend colors
                weights = get_biome_weights(height, heat, wet)
                color = blend_colors(weights)
                
                tile_rect = [x * tile_size, y * tile_size, tile_size, tile_size]
                pygame.draw.rect(window, color, tile_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

