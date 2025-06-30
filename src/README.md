# Source Code Organization

This directory contains the Asteroids game source code organized into logical modules for better maintainability and extensibility.

## Key Features

### Asteroid Belt System
- Asteroids spawn in realistic belt formations distributed throughout the galaxy
- Rocks move dynamically and spread out over time due to physics interactions
- No longer spawn around the player - encouraging exploration of the galaxy

### Galaxy Mini Map
- Real-time mini map in the top right corner showing the entire galaxy
- Shows player position (green dot with direction indicator), space stations (blue squares), and enemy saucers (red triangles)
- Rocks are color-coded by material type: Gold (bright yellow), Iron (silver), Coal (gray)
- Toggle on/off with the 'M' key
- Visible in all game states including attract mode

### Enhanced Physics
- Rock-to-rock collision physics with realistic momentum transfer
- Rocks bounce off each other creating dynamic asteroid fields
- Different mass values for different rock sizes affecting collision behavior

## Directory Structure

```
src/
├── core/              # Core game logic and main loop
│   ├── asteroids.py   # Main game class and game loop
│   └── game_state.py  # Game state management system
├── entities/          # Game objects and characters
│   ├── ship.py        # Player ship and thrust jet
│   ├── badies.py      # Rocks, saucers, and debris
│   └── shooter.py     # Base class for shooting entities
├── systems/           # Game systems and managers
│   ├── universe.py    # Universe management and collision detection
│   ├── camera.py      # Camera system for viewport management
│   ├── minimap.py     # Mini map system for galaxy overview
│   └── events.py      # Event system for decoupled communication
├── audio/             # Sound and audio management
│   └── soundManager.py # Sound loading and playback
├── ui/                # User interface and rendering
│   └── stage.py       # Display/rendering management
├── config/            # Configuration and object creation
│   ├── config.py      # Game configuration constants
│   └── factories.py   # Object factory patterns
└── util/              # Utility classes and helpers
    ├── vector2d.py    # 2D vector mathematics
    ├── vectorsprites.py # Vector-based sprite system
    └── geometry.py    # Geometric calculations
```

## Module Responsibilities

### Core (`core/`)
- **asteroids.py**: Main game class containing the primary game loop, state transitions, and high-level game logic
- **game_state.py**: State machine for managing different game states (menu, playing, paused, etc.)

### Entities (`entities/`)
- **ship.py**: Player ship with movement, rotation, shooting, and thrust jet visualization
- **badies.py**: Enemy entities including rocks (asteroids), flying saucers, and debris particles
- **shooter.py**: Base class providing shooting capabilities and bullet management

### Systems (`systems/`)
- **universe.py**: Manages the game world, object tracking, collision detection, and asteroid belt generation
- **camera.py**: Handles viewport management, following the player, and world-to-screen coordinate conversion
- **minimap.py**: Galaxy overview mini map system showing player position, rocks, space stations, and other objects
- **events.py**: Event system for loose coupling between game components

### Audio (`audio/`)
- **soundManager.py**: Centralized sound loading, management, and playback system
- *Future audio features can be added here*

### UI (`ui/`)
- **stage.py**: Rendering system that draws visible objects using camera coordinates
- *Future UI components (HUD, menus, etc.) can be added here*

### Config (`config/`)
- **config.py**: Centralized configuration constants for easy game balance adjustments
- **factories.py**: Factory patterns for consistent object creation with proper dependency injection

### Util (`util/`)
- **vector2d.py**: 2D vector mathematics for position and velocity calculations
- **vectorsprites.py**: Vector-based sprite system with collision detection
- **geometry.py**: Geometric utility functions for line intersections and collision calculations

## Design Patterns Used

1. **Factory Pattern**: Centralized object creation in `factories.py`
2. **Event System**: Decoupled communication between components
3. **State Machine**: Proper game state management
4. **Dependency Injection**: Clean separation of concerns
5. **Module Organization**: Logical grouping of related functionality

## Adding New Features

When adding new features, follow these guidelines:

- **New game entities**: Add to `entities/`
- **New game systems**: Add to `systems/`
- **Audio features**: Add to `audio/`
- **UI elements**: Add to `ui/`
- **Configuration**: Update `config/config.py`
- **Utilities**: Add to `util/` if widely reusable

This organization makes the codebase more maintainable, testable, and easier to extend with new features. 