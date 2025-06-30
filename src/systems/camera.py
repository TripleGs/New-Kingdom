from ..util.vector2d import Vector2d


class Camera:
    def __init__(self, screen_width, screen_height, universe_width, universe_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.universe_width = universe_width
        self.universe_height = universe_height
        
        # Camera position in world coordinates (center of view)
        self.x = universe_width // 2
        self.y = universe_height // 2
        
        # Camera bounds (top-left corner of visible area)
        self.view_x = self.x - screen_width // 2
        self.view_y = self.y - screen_height // 2
        
        # Target to follow (usually the player)
        self.target = None
        
        # Camera smoothing
        self.follow_speed = 0.1
        
    def setTarget(self, target):
        """Set the object for the camera to follow"""
        self.target = target
        
    def update(self):
        """Update camera position to follow target"""
        if self.target:
            # Calculate desired camera position (centered on target)
            target_x = self.target.position.x
            target_y = self.target.position.y
            
            # Smooth camera movement
            self.x += (target_x - self.x) * self.follow_speed
            self.y += (target_y - self.y) * self.follow_speed
            
            # Keep camera within universe bounds
            half_screen_w = self.screen_width // 2
            half_screen_h = self.screen_height // 2
            
            self.x = max(half_screen_w, min(self.universe_width - half_screen_w, self.x))
            self.y = max(half_screen_h, min(self.universe_height - half_screen_h, self.y))
            
            # Update view bounds (top-left corner of visible area)
            self.view_x = self.x - half_screen_w
            self.view_y = self.y - half_screen_h
            
    def worldToScreen(self, world_pos):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_pos.x - self.view_x
        screen_y = world_pos.y - self.view_y
        return Vector2d(screen_x, screen_y)
        
    def screenToWorld(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        world_x = screen_pos.x + self.view_x
        world_y = screen_pos.y + self.view_y
        return Vector2d(world_x, world_y)
        
    def isVisible(self, world_pos, padding=50):
        """Check if a world position is visible on screen"""
        return (world_pos.x >= self.view_x - padding and
                world_pos.x <= self.view_x + self.screen_width + padding and
                world_pos.y >= self.view_y - padding and
                world_pos.y <= self.view_y + self.screen_height + padding)
                
    def getVisibleRegion(self):
        """Get the visible region in world coordinates"""
        return (self.view_x, self.view_y, self.screen_width, self.screen_height) 