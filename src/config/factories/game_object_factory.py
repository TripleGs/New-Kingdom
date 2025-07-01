class GameObjectFactory:
    """Base factory for game objects"""
    
    def __init__(self, universe, stage):
        self.universe = universe
        self.stage = stage