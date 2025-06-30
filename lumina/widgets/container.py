from typing import Optional, Union, TYPE_CHECKING
import pygame
from lumina.core.widget import Widget
from lumina.core.types import Rect

if TYPE_CHECKING:
    from lumina.core.window import Window


class Container(Widget):
    """Base container widget that can hold child widgets"""
    
    def __init__(
        self,
        children: Optional[Union[Widget, list[Widget]]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Convert single child to list
        if children is None:
            self.children = []
        elif isinstance(children, Widget):
            self.children = [children]
        else:
            self.children = children
    
    def mount(self, parent: Optional[Widget] = None, window: Optional["Window"] = None) -> None:
        """Mount container and all children"""
        super().mount(parent, window)
        for child in self.children:
            child.mount(self, self.window)
    
    def unmount(self) -> None:
        """Unmount container and all children"""
        for child in self.children:
            child.unmount()
        super().unmount()
    
    def add_child(self, child: Widget) -> None:
        """Add a child widget"""
        self.children.append(child)
        if self._is_mounted:
            child.mount(self, self.window)
            self.invalidate()
    
    def remove_child(self, child: Widget) -> None:
        """Remove a child widget"""
        if child in self.children:
            child.unmount()
            self.children.remove(child)
            self.invalidate()
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate container size based on children"""
        if not self.children:
            return self.padding.left + self.padding.right, self.padding.top + self.padding.bottom
        
        # Simple stacking for now
        total_width = 0
        total_height = self.padding.top + self.padding.bottom
        
        for child in self.children:
            child_width, child_height = child.calculate_size(
                available_width - self.padding.left - self.padding.right,
                available_height - total_height
            )
            total_width = max(total_width, child_width)
            total_height += child_height
        
        return total_width + self.padding.left + self.padding.right, total_height
    
    def layout(self, rect: Rect) -> None:
        """Layout container and children"""
        super().layout(rect)
        
        # Layout children vertically
        y_offset = self.rect.y + self.padding.top
        content_width = self.rect.width - self.padding.left - self.padding.right
        
        for child in self.children:
            child_width, child_height = child.calculate_size(content_width, float('inf'))
            
            child_rect = Rect(
                self.rect.x + self.padding.left,
                y_offset,
                min(child_width, content_width),
                child_height
            )
            
            child.layout(child_rect)
            y_offset += child_height
    
    def render(self, surface: pygame.Surface) -> None:
        """Render container background and children"""
        if not self.visible:
            return
        
        # Render background if specified
        if self.style.background_color:
            bg_color = self.style.to_pygame_color(self.style.background_color)
            if bg_color:
                pygame.draw.rect(surface, bg_color, self.rect.to_pygame_rect())
        
        # Render children
        for child in self.children:
            if child.visible:
                child.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Pass events to children"""
        # Check children in reverse order (top to bottom)
        for child in reversed(self.children):
            if child.visible:
                # For mouse events, check if the child contains the point
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                    if hasattr(event, 'pos') and child.contains_point(*event.pos):
                        if child.handle_event(event):
                            return True
                else:
                    # For other events, pass them through
                    if child.handle_event(event):
                        return True
        return False


class Row(Container):
    """Container that arranges children horizontally"""
    
    def __init__(
        self,
        children: Optional[Union[Widget, list[Widget]]] = None,
        spacing: float = 8,
        align: str = "start",
        **kwargs
    ):
        super().__init__(children, **kwargs)
        self.spacing = spacing
        self.align = align  # start, center, end, space-between, space-around
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate row size"""
        if not self.children:
            return self.padding.left + self.padding.right, self.padding.top + self.padding.bottom
        
        total_width = self.padding.left + self.padding.right
        max_height = 0
        
        for i, child in enumerate(self.children):
            child_width, child_height = child.calculate_size(float('inf'), available_height)
            total_width += child_width
            if i < len(self.children) - 1:
                total_width += self.spacing
            max_height = max(max_height, child_height)
        
        return total_width, max_height + self.padding.top + self.padding.bottom
    
    def layout(self, rect: Rect) -> None:
        """Layout children horizontally"""
        super().layout(rect)
        
        if not self.children:
            return
        
        # Calculate total width needed
        total_width = 0
        child_sizes = []
        
        for i, child in enumerate(self.children):
            width, height = child.calculate_size(float('inf'), self.rect.height)
            child_sizes.append((width, height))
            total_width += width
            if i < len(self.children) - 1:
                total_width += self.spacing
        
        # Calculate starting position based on alignment
        content_width = self.rect.width - self.padding.left - self.padding.right
        
        if self.align == "center":
            x_offset = self.rect.x + self.padding.left + (content_width - total_width) / 2
        elif self.align == "end":
            x_offset = self.rect.x + self.rect.width - self.padding.right - total_width
        else:  # start
            x_offset = self.rect.x + self.padding.left
        
        # Layout each child
        for i, (child, (width, height)) in enumerate(zip(self.children, child_sizes)):
            y_offset = self.rect.y + self.padding.top
            
            child_rect = Rect(x_offset, y_offset, width, height)
            child.layout(child_rect)
            
            x_offset += width
            if i < len(self.children) - 1:
                x_offset += self.spacing


class Column(Container):
    """Container that arranges children vertically"""
    
    def __init__(
        self,
        children: Optional[Union[Widget, list[Widget]]] = None,
        spacing: float = 8,
        align: str = "start",
        **kwargs
    ):
        super().__init__(children, **kwargs)
        self.spacing = spacing
        self.align = align  # start, center, end, stretch
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate column size"""
        if not self.children:
            return self.padding.left + self.padding.right, self.padding.top + self.padding.bottom
        
        max_width = 0
        total_height = self.padding.top + self.padding.bottom
        
        for i, child in enumerate(self.children):
            child_width, child_height = child.calculate_size(available_width, float('inf'))
            max_width = max(max_width, child_width)
            total_height += child_height
            if i < len(self.children) - 1:
                total_height += self.spacing
        
        return max_width + self.padding.left + self.padding.right, total_height
    
    def layout(self, rect: Rect) -> None:
        """Layout children vertically with spacing"""
        super().layout(rect)
        
        y_offset = self.rect.y + self.padding.top
        content_width = self.rect.width - self.padding.left - self.padding.right
        
        for i, child in enumerate(self.children):
            child_width, child_height = child.calculate_size(content_width, float('inf'))
            
            # Apply horizontal alignment
            if self.align == "center":
                x_offset = self.rect.x + self.padding.left + (content_width - child_width) / 2
            elif self.align == "end":
                x_offset = self.rect.x + self.rect.width - self.padding.right - child_width
            elif self.align == "stretch":
                x_offset = self.rect.x + self.padding.left
                child_width = content_width
            else:  # start
                x_offset = self.rect.x + self.padding.left
            
            child_rect = Rect(x_offset, y_offset, child_width, child_height)
            child.layout(child_rect)
            
            y_offset += child_height
            if i < len(self.children) - 1:
                y_offset += self.spacing


class Stack(Container):
    """Container that stacks children on top of each other"""
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate stack size (maximum of all children)"""
        if not self.children:
            return self.padding.left + self.padding.right, self.padding.top + self.padding.bottom
        
        max_width = 0
        max_height = 0
        
        for child in self.children:
            child_width, child_height = child.calculate_size(available_width, available_height)
            max_width = max(max_width, child_width)
            max_height = max(max_height, child_height)
        
        return (
            max_width + self.padding.left + self.padding.right,
            max_height + self.padding.top + self.padding.bottom
        )
    
    def layout(self, rect: Rect) -> None:
        """Layout all children in the same space"""
        super().layout(rect)
        
        content_rect = Rect(
            self.rect.x + self.padding.left,
            self.rect.y + self.padding.top,
            self.rect.width - self.padding.left - self.padding.right,
            self.rect.height - self.padding.top - self.padding.bottom
        )
        
        for child in self.children:
            child.layout(content_rect)