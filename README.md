# Terrain Generation with Biomes
## A fun Pygame project you can interact with that uses Perlin noise.
Based on heat, wetness, and elevation maps, the terrain is divided into biomes like deserts, grasslands, rainforests, mountains, and snow regions. Games like Minecraft inspire the project and demonstrates noise-based terrain generation with biomes.

## Features
- Perlin Noise Integration: Uses Perlin noise to create natural-looking terrains.
- Dynamic Biomes: Biomes are determined by:
    - Heat: Ranges from cold (snow) to hot (deserts).
    - Wetness (Dryness): Separates dry areas (deserts) from wet areas (rainforests).
    - Elevation: Adds mountains, snow caps, and water levels.
    - Interactive Controls: Zoom, pan, and regenerate the terrain interactively.
    - Custom Seeds: Generate terrains based on user-provided seeds for reproducibility.
 
## Controls
 - Move: `WASD` & arrow keys
 - Zoom: `Q` to zoom out, `E` to zoom in

## Requirements
 - Python 3.9+
 - Libraries:
    - pygame
    - perlin-noise
    - math (included)

## Demo
![Demo](https://github.com/22yeets22/Terrain-Generator/blob/main/demo.png?raw=true "Demo")
