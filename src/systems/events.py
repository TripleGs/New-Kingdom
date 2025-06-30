"""
Event System for Game Components
Allows loose coupling between different game systems
"""

from typing import Dict, List, Callable, Any
from enum import Enum


class EventType(Enum):
    """Enumeration of all game events"""
    SHIP_DESTROYED = "ship_destroyed"
    ROCK_DESTROYED = "rock_destroyed"
    SAUCER_DESTROYED = "saucer_destroyed"
    BULLET_FIRED = "bullet_fired"
    SCORE_CHANGED = "score_changed"
    LIFE_LOST = "life_lost"
    LIFE_GAINED = "life_gained"
    LEVEL_UP = "level_up"
    GAME_OVER = "game_over"
    HYPERSPACE_ACTIVATED = "hyperspace_activated"


class Event:
    """Represents a single game event"""
    def __init__(self, event_type: EventType, data: Dict[str, Any] = None):
        self.type = event_type
        self.data = data or {}
        

class EventManager:
    """Manages event subscriptions and dispatching"""
    
    def __init__(self):
        self.listeners: Dict[EventType, List[Callable]] = {}
        
    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to an event type"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """Unsubscribe from an event type"""
        if event_type in self.listeners:
            if callback in self.listeners[event_type]:
                self.listeners[event_type].remove(callback)
                
    def dispatch(self, event: Event):
        """Dispatch an event to all subscribers"""
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event callback for {event.type}: {e}")
                    
    def clear(self):
        """Clear all event listeners"""
        self.listeners.clear()


# Global event manager instance
event_manager = EventManager()


# Convenience functions
def subscribe(event_type: EventType, callback: Callable):
    """Subscribe to an event type"""
    event_manager.subscribe(event_type, callback)
    

def dispatch(event_type: EventType, data: Dict[str, Any] = None):
    """Dispatch an event"""
    event = Event(event_type, data)
    event_manager.dispatch(event) 