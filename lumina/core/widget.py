from typing import Optional, Any, Callable, TYPE_CHECKING
from abc import ABC, abstractmethod
import pygame
from lumina.core.types import Rect, Padding, Margin, EventType
from lumina.core.style import Style
import uuid

if TYPE_CHECKING:
    from lumina.core.window import Window


class Widget(ABC):
    """Base class for all Lumina widgets"""
    
    def __init__(
        self,
        id: Optional[str] = None,
        style: Optional[Style] = None,
        padding: Optional[Padding] = None,
        margin: Optional[Margin] = None,
        visible: bool = True,
        **kwargs
    ):
        self.id = id or str(uuid.uuid4())
        self.style = style or Style()
        self.padding = padding or Padding()
        self.margin = margin or Margin()
        self.visible = visible
        
        self._rect = Rect(0, 0, 0, 0)
        self._parent: Optional[Widget] = None
        self._window: Optional["Window"] = None
        self._event_handlers: dict[EventType, list[Callable]] = {}
        self._is_mounted = False
        
        # Apply any additional kwargs as properties
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @property
    def rect(self) -> Rect:
        return self._rect
    
    @property
    def parent(self) -> Optional["Widget"]:
        return self._parent
    
    @property
    def window(self) -> Optional["Window"]:
        return self._window
    
    def mount(self, parent: Optional["Widget"] = None, window: Optional["Window"] = None) -> None:
        """Called when widget is added to the widget tree"""
        self._parent = parent
        self._window = window or (parent.window if parent else None)
        self._is_mounted = True
        self._emit_event(EventType.MOUNT)
        self.on_mount()
    
    def unmount(self) -> None:
        """Called when widget is removed from the widget tree"""
        self._emit_event(EventType.UNMOUNT)
        self.on_unmount()
        self._is_mounted = False
        self._parent = None
        self._window = None
    
    def on_mount(self) -> None:
        """Override to handle mount event"""
        pass
    
    def on_unmount(self) -> None:
        """Override to handle unmount event"""
        pass
    
    def add_event_listener(self, event_type: EventType, handler: Callable) -> Callable[[], None]:
        """Add an event listener. Returns function to remove listener."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        
        self._event_handlers[event_type].append(handler)
        
        def remove():
            if event_type in self._event_handlers:
                self._event_handlers[event_type].remove(handler)
        
        return remove
    
    def _emit_event(self, event_type: EventType, event_data: Optional[Any] = None) -> None:
        """Emit an event to all registered handlers"""
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    print(f"Error in event handler for {event_type}: {e}")
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame event. Returns True if event was consumed."""
        return False
    
    @abstractmethod
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate the widget's preferred size given available space"""
        pass
    
    def layout(self, rect: Rect) -> None:
        """Position and size the widget within the given rectangle"""
        self._rect = rect
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the widget to the given surface"""
        pass
    
    def invalidate(self) -> None:
        """Mark widget as needing redraw"""
        if self._window:
            self._window.invalidate()
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within widget bounds"""
        return self._rect.contains(x, y)