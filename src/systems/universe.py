import random
import math
from ..util.vector2d import Vector2d
from ..entities.rock import Rock
from ..entities.saucer import Saucer
from ..entities.debris import Debris
from ..entities.ship import Ship
from ..entities.shooter import Bullet


class Universe:
    def __init__(self, width=10000, height=10000):
        self.width = width
        self.height = height
        self.objects = []
        self.rocks = []
        self.bullets = []
        self.debris = []
        self.ship = None
        self.saucer = None
        
    def addObject(self, obj):
        """Add an object to the universe"""
        self.objects.append(obj)
        
        # Categorize objects for easier management
        if isinstance(obj, Rock):
            self.rocks.append(obj)
        elif isinstance(obj, Bullet):
            self.bullets.append(obj)
        elif isinstance(obj, Debris):
            self.debris.append(obj)
        elif isinstance(obj, Ship):
            self.ship = obj
        elif isinstance(obj, Saucer):
            self.saucer = obj
            
    def removeObject(self, obj):
        """Remove an object from the universe"""
        if obj in self.objects:
            self.objects.remove(obj)
            
        # Remove from category lists
        if obj in self.rocks:
            self.rocks.remove(obj)
        elif obj in self.bullets:
            self.bullets.remove(obj)
        elif obj in self.debris:
            self.debris.remove(obj)
        elif obj == self.saucer:
            self.saucer = None
            
    def getObjectsInRegion(self, x, y, width, height):
        """Get all objects within a rectangular region"""
        visible_objects = []
        
        for obj in self.objects:
            # Check if object is within the visible region
            # Add some padding for objects that might be partially visible
            padding = 50
            if (obj.position.x >= x - padding and 
                obj.position.x <= x + width + padding and
                obj.position.y >= y - padding and 
                obj.position.y <= y + height + padding):
                visible_objects.append(obj)
                
        return visible_objects
        
    def updateObjects(self):
        """Update all objects in the universe"""
        # Update all objects
        for obj in self.objects[:]:  # Use slice to avoid modification during iteration
            obj.move()
            
            # Remove expired objects (bullets, debris with TTL)
            if hasattr(obj, 'ttl') and obj.ttl <= 0:
                self.removeObject(obj)
                
    def createAsteroidBelts(self, num_belts=8, rocks_per_belt=15):
        """Create asteroid belts randomly distributed throughout the universe"""
        # Clear existing rocks
        for rock in self.rocks[:]:
            self.removeObject(rock)
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        for belt_idx in range(num_belts):
            # Create belt centers avoiding the center spawn area
            while True:
                belt_center_x = random.randrange(int(self.width * 0.1), int(self.width * 0.9))
                belt_center_y = random.randrange(int(self.height * 0.1), int(self.height * 0.9))
                
                # Make sure belt isn't too close to center spawn
                distance_from_center = math.sqrt((belt_center_x - center_x)**2 + (belt_center_y - center_y)**2)
                if distance_from_center > 1000:  # Stay away from spawn area
                    break
            
            belt_center = Vector2d(belt_center_x, belt_center_y)
            belt_radius = random.randrange(300, 800)  # Varying belt sizes
            
            # Create rocks in this belt
            self.createRockBelt(belt_center, belt_radius, rocks_per_belt)
    
    def createRockBelt(self, belt_center, belt_radius, num_rocks):
        """Create a belt of rocks around a center point"""
        for _ in range(num_rocks):
            # Generate position within belt radius using polar coordinates
            angle = random.uniform(0, 2 * math.pi)
            # Use varying distances to create a more natural belt shape
            distance = random.uniform(belt_radius * 0.3, belt_radius)
            
            # Add some randomness to make it less circular
            distance += random.uniform(-belt_radius * 0.2, belt_radius * 0.2)
            
            x = belt_center.x + distance * math.cos(angle)
            y = belt_center.y + distance * math.sin(angle)
            
            # Keep within universe bounds
            x = max(50, min(self.width - 50, x))
            y = max(50, min(self.height - 50, y))
            
            position = Vector2d(x, y)
            
            # Create rocks of varying sizes, with more large rocks
            rock_type_chance = random.random()
            if rock_type_chance < 0.6:
                rock_type = Rock.largeRockType
            elif rock_type_chance < 0.85:
                rock_type = Rock.mediumRockType
            else:
                rock_type = Rock.smallRockType
                
            newRock = Rock(None, position, rock_type)
            self.addObject(newRock)
    
    def createRocksAroundPlayer(self, player_pos, num_rocks, min_distance=200):
        """Create rocks around the player but not too close - DEPRECATED, use createAsteroidBelts instead"""
        # This method is kept for compatibility but should not be used
        # The new system uses createAsteroidBelts()
        pass
    
    def addRocksToExistingBelts(self, additional_rocks_per_belt=5):
        """Add more rocks randomly throughout the universe (used for level progression)"""
        # Since rocks spread out, just add them randomly across the universe
        for _ in range(additional_rocks_per_belt * 8):  # Multiply by estimated belt count
            # Create random position avoiding center spawn
            center_x = self.width // 2
            center_y = self.height // 2
            
            while True:
                x = random.randrange(int(self.width * 0.1), int(self.width * 0.9))
                y = random.randrange(int(self.height * 0.1), int(self.height * 0.9))
                
                # Make sure not too close to center spawn
                distance_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance_from_center > 800:
                    break
            
            position = Vector2d(x, y)
            
            # Create rocks of varying sizes
            rock_type_chance = random.random()
            if rock_type_chance < 0.5:
                rock_type = Rock.largeRockType
            elif rock_type_chance < 0.8:
                rock_type = Rock.mediumRockType
            else:
                rock_type = Rock.smallRockType
                
            newRock = Rock(None, position, rock_type)
            self.addObject(newRock)

    def checkCollisions(self):
        """Check for collisions between objects"""
        collisions = []
        
        # Check ship collisions with rocks
        if self.ship and not self.ship.inHyperSpace:
            for rock in self.rocks:
                if rock.collidesWith(self.ship):
                    p = rock.checkPolygonCollision(self.ship)
                    if p is not None:
                        collisions.append(('ship_rock', self.ship, rock))
                        
        # Check all bullets (ship and saucer bullets) with rocks
        all_bullets = []
        if self.ship:
            all_bullets.extend(self.ship.bullets)
        if self.saucer:
            all_bullets.extend(self.saucer.bullets)
            
        for bullet in all_bullets:
            if bullet.ttl > 0:  # Only active bullets
                for rock in self.rocks[:]:
                    if rock.collidesWith(bullet):
                        collisions.append(('bullet_rock', bullet, rock))
                        break  # Each bullet can only hit one rock
                        
        # Check saucer bullets hitting ship
        if self.saucer and self.ship and not self.ship.inHyperSpace:
            for bullet in self.saucer.bullets:
                if bullet.ttl > 0 and self.ship.collidesWith(bullet):
                    collisions.append(('bullet_ship', bullet, self.ship))
                    
        # Check ship bullets hitting saucer
        if self.ship and self.saucer:
            for bullet in self.ship.bullets:
                if bullet.ttl > 0 and self.saucer.collidesWith(bullet):
                    collisions.append(('bullet_saucer', bullet, self.saucer))
                    
        # Check saucer collisions with rocks
        if self.saucer:
            for rock in self.rocks:
                if rock.collidesWith(self.saucer):
                    collisions.append(('saucer_rock', self.saucer, rock))
                    
        # Check direct ship-saucer collision
        if self.saucer and self.ship and not self.ship.inHyperSpace:
            if self.saucer.collidesWith(self.ship):
                collisions.append(('saucer_ship', self.saucer, self.ship))
        
        # Check rock-rock collisions for physics
        self.handleRockRockCollisions()
                    
        return collisions
        
    def handleRockRockCollisions(self):
        """Handle collisions between rocks with realistic physics"""
        import math
        
        # Check all pairs of rocks for collisions
        for i in range(len(self.rocks)):
            for j in range(i + 1, len(self.rocks)):
                rock1 = self.rocks[i]
                rock2 = self.rocks[j]
                
                # Calculate distance between rock centers
                dx = rock2.position.x - rock1.position.x
                dy = rock2.position.y - rock1.position.y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Estimate collision radius based on rock type
                radius1 = self.getRockRadius(rock1)
                radius2 = self.getRockRadius(rock2)
                min_distance = radius1 + radius2
                
                # Check if rocks are colliding
                if distance < min_distance and distance > 0.1:  # Avoid division by zero
                    # Calculate collision normal
                    nx = dx / distance
                    ny = dy / distance
                    
                    # Calculate overlap
                    overlap = min_distance - distance
                    
                    # Separate rocks to prevent overlap
                    separate_distance = overlap * 0.5
                    rock1.position.x -= nx * separate_distance
                    rock1.position.y -= ny * separate_distance
                    rock2.position.x += nx * separate_distance
                    rock2.position.y += ny * separate_distance
                    
                    # Calculate relative velocity
                    dvx = rock2.heading.x - rock1.heading.x
                    dvy = rock2.heading.y - rock1.heading.y
                    
                    # Calculate relative velocity in collision normal direction
                    dvn = dvx * nx + dvy * ny
                    
                    # Do not resolve if velocities are separating
                    if dvn > 0:
                        continue
                    
                    # Calculate collision response (elastic collision)
                    # Using conservation of momentum for different mass rocks
                    mass1 = self.getRockMass(rock1)
                    mass2 = self.getRockMass(rock2)
                    
                    # Calculate impulse scalar
                    impulse = 2 * dvn / (mass1 + mass2)
                    
                    # Apply restitution (bounciness) - make it slightly bouncy
                    restitution = 0.8
                    impulse *= restitution
                    
                    # Apply impulse to velocities
                    rock1.heading.x += impulse * mass2 * nx
                    rock1.heading.y += impulse * mass2 * ny
                    rock2.heading.x -= impulse * mass1 * nx
                    rock2.heading.y -= impulse * mass1 * ny
                    
                    # Add some spin when rocks collide
                    rock1.angle += random.uniform(-5, 5)
                    rock2.angle += random.uniform(-5, 5)
    
    def getRockRadius(self, rock):
        """Get approximate radius of a rock based on its type"""
        from ..entities.rock import Rock
        if rock.rockType == Rock.largeRockType:
            return 35
        elif rock.rockType == Rock.mediumRockType:
            return 22
        else:  # small rock
            return 12
    
    def getRockMass(self, rock):
        """Get mass of a rock based on its type"""
        from ..entities.rock import Rock
        if rock.rockType == Rock.largeRockType:
            return 3.0
        elif rock.rockType == Rock.mediumRockType:
            return 2.0
        else:  # small rock
            return 1.0
        
    def getShipPosition(self):
        """Get the current ship position"""
        if self.ship:
            return self.ship.position
        return Vector2d(self.width // 2, self.height // 2) 