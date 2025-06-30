"""
Game Configuration
Centralized configuration for all game constants and settings
"""

# Universe Settings
UNIVERSE_WIDTH = 20000
UNIVERSE_HEIGHT = 20000

# Screen Settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Ship Settings
SHIP_ACCELERATION = 0.2
SHIP_DECELERATION = -0.005
SHIP_MAX_VELOCITY = 10
SHIP_TURN_ANGLE = 6
SHIP_BULLET_VELOCITY = 13.0
SHIP_MAX_BULLETS = 4
SHIP_BULLET_TTL = 35

# Camera Settings
CAMERA_FOLLOW_SPEED = 0.1

# Rock Settings
ROCK_LARGE_TYPE = 0
ROCK_MEDIUM_TYPE = 1
ROCK_SMALL_TYPE = 2
ROCK_VELOCITIES = (1.5, 3.0, 4.5)
ROCK_SCALES = (2.5, 1.5, 0.6)
ROCK_SCORES = {
    ROCK_LARGE_TYPE: 50,
    ROCK_MEDIUM_TYPE: 100,
    ROCK_SMALL_TYPE: 200
}

# Rock sounds
ROCK_SOUNDS = {
    ROCK_LARGE_TYPE: "explode1",
    ROCK_MEDIUM_TYPE: "explode2", 
    ROCK_SMALL_TYPE: "explode3"
}

# Saucer Settings
SAUCER_LARGE_TYPE = 0
SAUCER_SMALL_TYPE = 1
SAUCER_VELOCITIES = (1.5, 2.5)
SAUCER_SCALES = (1.5, 1.0)
SAUCER_SCORES = (500, 1000)
SAUCER_MAX_BULLETS = 1
SAUCER_BULLET_TTL = [60, 90]
SAUCER_BULLET_VELOCITY = 5

# Debris Settings
DEBRIS_COUNT = 25
DEBRIS_TTL = 50

# Game Settings
INITIAL_ROCKS = 8
EXPLODING_TTL = 180
INITIAL_LIVES = 5
EXTRA_LIFE_SCORE = 10000
SAUCER_SPAWN_INTERVAL = 2000

# Sound Settings
SOUND_FILES = {
    "fire": "assets/audio/FIRE.WAV",
    "explode1": "assets/audio/EXPLODE1.WAV",
    "explode2": "assets/audio/EXPLODE2.WAV", 
    "explode3": "assets/audio/EXPLODE3.WAV",
    "lsaucer": "assets/audio/LSAUCER.WAV",
    "ssaucer": "assets/audio/SSAUCER.WAV",
    "thrust": "assets/audio/THRUST.WAV",
    "sfire": "assets/audio/SFIRE.WAV",
    "extralife": "assets/audio/LIFE.WAV"
}

# Font Settings
FONT_PATH = "assets/font/Hyperspace.otf"
FONT_SIZES = {
    "title": 50,
    "subtitle": 30,
    "normal": 20,
    "small": 15
}

# Colors
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0), 
    "gray": (180, 180, 180),
    "light_gray": (200, 200, 200),
    "background": (10, 10, 10)
} 