"""
Object Factories
Centralized object creation with proper dependency injection
"""

import random
from ...util.vector2d import Vector2d
from ...entities.ship import Ship, ThrustJet
from ...entities.rock import Rock
from ...entities.saucer import Saucer
from ...entities.debris import Debris
from ..config import *
from .ship_factory import ShipFactory
from .rock_factory import RockFactory
from .saucer_factory import SaucerFactory
from .debris_factory import DebrisFactory


class GameObjectFactoryManager:
    """Manages all object factories"""
    
    def __init__(self, universe, stage):
        self.ship_factory = ShipFactory(universe, stage)
        self.rock_factory = RockFactory(universe, stage)
        self.saucer_factory = SaucerFactory(universe, stage)
        self.debris_factory = DebrisFactory(universe, stage) 