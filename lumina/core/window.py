from typing import Optional, Union, Callable
import pygame
import asyncio
from lumina.core.widget import Widget
from lumina.core.types import Rect, Color
from lumina.themes import Theme, themes


class Window:
    """Main window container for Lumina applications"""
    
    def __init__(
        self,
        title: str = "Lumina Window",
        width: int = 800,
        height: int = 600,
        resizable: bool = True,
        min_width: int = 400,
        min_height: int = 300,
        theme: Optional[Theme] = None,
        children: Optional[Union[Widget, list[Widget]]] = None,
        on_close: Optional[Callable[[], None]] = None,
    ):
        self.title = title
        self.width = width
        self.height = height
        self.resizable = resizable
        self.min_width = min_width
        self.min_height = min_height
        self.theme = theme or themes.default_light
        self.on_close = on_close
        
        # Convert single child to list
        if children is None:
            self.children = []
        elif isinstance(children, Widget):
            self.children = [children]
        else:
            self.children = children
        
        # Internal state
        self._surface: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None
        self._running = False
        self._needs_redraw = True
        self._mouse_pos = (0, 0)
        self._focused_widget: Optional[Widget] = None
        self._hovered_widget: Optional[Widget] = None
        self._last_invalidate_time = 0.0
        self._invalidate_throttle = 1.0 / 120.0  # Max 120fps invalidation
        
        # Event loop
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
    
    def mount_children(self) -> None:
        """Mount all child widgets"""
        for child in self.children:
            child.mount(parent=None, window=self)
    
    def unmount_children(self) -> None:
        """Unmount all child widgets"""
        for child in self.children:
            child.unmount()
    
    def add_child(self, child: Widget) -> None:
        """Add a child widget to the window"""
        self.children.append(child)
        if self._running:
            child.mount(parent=None, window=self)
            self.invalidate()
    
    def remove_child(self, child: Widget) -> None:
        """Remove a child widget from the window"""
        if child in self.children:
            child.unmount()
            self.children.remove(child)
            self.invalidate()
    
    def invalidate(self) -> None:
        """Mark window as needing redraw"""
        import time
        current_time = time.time()
        
        # Throttle invalidation to prevent excessive redraws that cause text pulsing
        if current_time - self._last_invalidate_time > self._invalidate_throttle:
            self._needs_redraw = True
            self._last_invalidate_time = current_time
    
    def set_theme(self, theme) -> None:
        """Update window theme and trigger complete redraw"""
        print(f"Setting theme: {theme.primary_color}")
        self.theme = theme
        
        # Force complete re-render by clearing all caches
        self._clear_all_caches()
        
        # Force immediate redraw
        self.invalidate()
        
        # Trigger layout recalculation 
        self.layout()
    
    def _clear_all_caches(self) -> None:
        """Clear all cached rendering data recursively"""
        def clear_recursive(widget):
            # Clear all possible cached data
            if hasattr(widget, '_rendered_text'):
                widget._rendered_text = None
            if hasattr(widget, '_last_text'):
                widget._last_text = None
            if hasattr(widget, '_cached_surface'):
                widget._cached_surface = None
            
            # Clear any button state caches
            if hasattr(widget, '_button_surface'):
                widget._button_surface = None
            
            # Force widget to re-render
            if hasattr(widget, 'invalidate'):
                widget.invalidate()
            
            # Recursively clear children
            if hasattr(widget, 'children') and widget.children:
                for child in widget.children:
                    clear_recursive(child)
        
        # Clear all widget caches
        for child in self.children:
            clear_recursive(child)
    
    def layout(self) -> None:
        """Layout all child widgets"""
        if not self.children:
            return
        
        # For now, simple vertical stack layout
        window_rect = Rect(0, 0, self.width, self.height)
        y_offset = 0
        
        for child in self.children:
            # Calculate child size
            child_width, child_height = child.calculate_size(self.width, self.height - y_offset)
            
            # Position child
            child_rect = Rect(0, y_offset, child_width, child_height)
            child.layout(child_rect)
            
            y_offset += child_height
    
    def render(self) -> None:
        """Render the window and all children"""
        if not self._surface or not self._needs_redraw:
            return
        
        # Clear background
        bg_color = self.theme.background_color
        if isinstance(bg_color, str):
            bg_color = pygame.Color(bg_color)
        self._surface.fill(bg_color)
        
        # Render children
        for child in self.children:
            if child.visible:
                child.render(self._surface)
        
        # Update display
        pygame.display.flip()
        self._needs_redraw = False
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events"""
        if event.type == pygame.QUIT:
            self._running = False
            if self.on_close:
                self.on_close()
        
        elif event.type == pygame.VIDEORESIZE:
            if self.resizable:
                self.width = max(event.w, self.min_width)
                self.height = max(event.h, self.min_height)
                self._surface = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.RESIZABLE if self.resizable else 0
                )
                self.layout()
                self.invalidate()
        
        elif event.type == pygame.MOUSEMOTION:
            self._mouse_pos = event.pos
            self._update_hover_state()
        
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            # Find widget under mouse and send click event
            for child in reversed(self.children):
                if child.visible and child.contains_point(*self._mouse_pos):
                    if child.handle_event(event):
                        break
        
        # Pass events to focused widget
        elif self._focused_widget and event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self._focused_widget.handle_event(event)
    
    def _update_hover_state(self) -> None:
        """Update which widget is being hovered"""
        new_hovered = None
        
        for child in reversed(self.children):
            if child.visible and child.contains_point(*self._mouse_pos):
                new_hovered = child
                break
        
        if new_hovered != self._hovered_widget:
            # Update hover states but don't invalidate entire window
            # This prevents constant re-rendering that causes text pulsing
            self._hovered_widget = new_hovered
            # Let individual widgets handle their own invalidation
    
    def run(self) -> None:
        """Run the window event loop"""
        pygame.init()
        
        # Setup high DPI support
        from lumina.core.display import DisplayManager
        DisplayManager.setup_high_dpi_support()
        
        # Position window nicely
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
        
        # Scale window size for high DPI displays
        scaled_width, scaled_height = DisplayManager.scale_window_size(self.width, self.height)
        
        # Create window with better quality
        flags = pygame.RESIZABLE if self.resizable else 0
        
        # Try to enable anti-aliasing and better rendering
        try:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        except:
            pass  # Fallback if OpenGL not available
        
        self._surface = pygame.display.set_mode((scaled_width, scaled_height), flags)
        pygame.display.set_caption(self.title)
        
        # Setup
        self._clock = pygame.time.Clock()
        self._running = True
        
        # Mount children
        self.mount_children()
        
        # Initial layout
        self.layout()
        
        # Main loop
        while self._running:
            # Handle events
            for event in pygame.event.get():
                self.handle_event(event)
            
            # Render
            self.render()
            
            # Cap at 60 FPS
            self._clock.tick(60)
        
        # Cleanup
        self.unmount_children()
        pygame.quit()