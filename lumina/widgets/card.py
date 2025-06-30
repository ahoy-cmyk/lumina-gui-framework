from typing import Optional, Union, Callable
import pygame
import time
from lumina.core.widget import Widget
from lumina.core.types import Rect, Padding
from lumina.core.graphics import ModernGraphics
from lumina.widgets.container import Container


class Card(Container):
    """Modern card component with elevation and hover effects"""
    
    def __init__(
        self,
        title: Optional[str] = None,
        children: Optional[Union[Widget, list[Widget]]] = None,
        elevation: int = 1,
        hoverable: bool = False,
        clickable: bool = False,
        on_click: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        # Set default padding for cards
        if "padding" not in kwargs:
            kwargs["padding"] = Padding.all(16)
        
        super().__init__(children, **kwargs)
        
        self.title = title
        self.elevation = elevation
        self.hoverable = hoverable
        self.clickable = clickable
        self.on_click = on_click
        
        # Animation state
        self._is_hovered = False
        self._hover_animation = 0.0
        self._last_update = time.time()
        
        # Apply card styling
        self.style.border_radius = 12
        self.style.cursor = "pointer" if clickable else "default"
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate card size including title"""
        width, height = super().calculate_size(available_width, available_height)
        
        # Add space for title
        if self.title:
            font = self.style.get_font()
            title_height = font.get_height() + 8  # Add some spacing
            height += title_height
        
        return width, height
    
    def layout(self, rect: Rect) -> None:
        """Layout card content with title space"""
        self._rect = rect
        
        if not self.children:
            return
        
        # Calculate content area (excluding title)
        title_height = 0
        if self.title:
            font = self.style.get_font()
            title_height = font.get_height() + 8
        
        content_rect = Rect(
            self.rect.x + self.padding.left,
            self.rect.y + self.padding.top + title_height,
            self.rect.width - self.padding.left - self.padding.right,
            self.rect.height - self.padding.top - self.padding.bottom - title_height
        )
        
        # Layout children in content area
        y_offset = content_rect.y
        
        for child in self.children:
            child_width, child_height = child.calculate_size(content_rect.width, float('inf'))
            
            child_rect = Rect(
                content_rect.x,
                y_offset,
                min(child_width, content_rect.width),
                child_height
            )
            
            child.layout(child_rect)
            y_offset += child_height + 8  # Add spacing between children
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle card events including hover and click"""
        # Handle hover state
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self._is_hovered
            self._is_hovered = self.contains_point(*event.pos)
            if was_hovered != self._is_hovered and self.hoverable:
                self.invalidate()
        
        # Handle click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(*event.pos) and self.clickable:
                if self.on_click:
                    self.on_click()
                return True
        
        # Pass events to children
        return super().handle_event(event)
    
    def _update_animations(self) -> None:
        """Update hover animation"""
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        # Update hover animation
        target_hover = 1.0 if self._is_hovered and self.hoverable else 0.0
        self._hover_animation += (target_hover - self._hover_animation) * 8.0 * dt
        self._hover_animation = max(0.0, min(1.0, self._hover_animation))
        
        # Request redraw if animating
        if abs(self._hover_animation - target_hover) > 0.01:
            self.invalidate()
    
    def render(self, surface: pygame.Surface) -> None:
        """Render card with elevation and hover effects"""
        if not self.visible:
            return
        
        # Update animations
        self._update_animations()
        
        # Get theme
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Calculate elevation and hover effects
        current_elevation = self.elevation + (2 * self._hover_animation)
        shadow_offset = (0, int(2 + current_elevation))
        shadow_blur = 4 + current_elevation * 2
        shadow_alpha = int(20 + current_elevation * 5)
        
        # Draw shadow
        ModernGraphics.draw_shadow(
            surface,
            self.rect.to_pygame_rect(),
            self.style.border_radius,
            blur_radius=shadow_blur,
            offset=shadow_offset,
            color=ModernGraphics.get_color_with_alpha((0, 0, 0), shadow_alpha)
        )
        
        # Draw card background
        bg_color = pygame.Color(theme.surface_color)
        if self._hover_animation > 0:
            bg_color = ModernGraphics.lighten_color(bg_color, 0.02 * self._hover_animation)
        
        ModernGraphics.draw_rounded_rect(
            surface,
            bg_color,
            self.rect.to_pygame_rect(),
            self.style.border_radius
        )
        
        # Draw title if present
        if self.title:
            self._draw_title(surface, theme)
        
        # Render children
        for child in self.children:
            if child.visible:
                child.render(surface)
    
    def _draw_title(self, surface: pygame.Surface, theme) -> None:
        """Draw card title"""
        font = pygame.font.Font(None, 20)  # Larger font for title
        font.set_bold(True)
        
        title_color = pygame.Color(theme.text_primary)
        title_surface = font.render(self.title, True, title_color)
        
        # Position title
        title_x = self.rect.x + self.padding.left
        title_y = self.rect.y + self.padding.top
        
        surface.blit(title_surface, (title_x, title_y))


class Modal(Widget):
    """Modern modal dialog with backdrop and animations"""
    
    def __init__(
        self,
        title: str,
        content: Union[Widget, list[Widget]],
        width: int = 400,
        height: int = 300,
        closable: bool = True,
        on_close: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.title = title
        self.modal_width = width
        self.modal_height = height
        self.closable = closable
        self.on_close = on_close
        
        # Convert content to list
        if isinstance(content, Widget):
            self.content = [content]
        else:
            self.content = content
        
        # Animation state
        self._backdrop_animation = 0.0
        self._modal_animation = 0.0
        self._is_opening = True
        self._last_update = time.time()
        
        # Mount content
        for child in self.content:
            child.mount(self, self.window)
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Modal takes full screen"""
        return available_width, available_height
    
    def layout(self, rect: Rect) -> None:
        """Layout modal in center of screen"""
        super().layout(rect)
        
        # Calculate modal position (centered)
        modal_x = rect.x + (rect.width - self.modal_width) / 2
        modal_y = rect.y + (rect.height - self.modal_height) / 2
        
        modal_rect = Rect(modal_x, modal_y, self.modal_width, self.modal_height)
        
        # Layout content within modal
        content_rect = Rect(
            modal_rect.x + 24,
            modal_rect.y + 60,  # Space for title bar
            modal_rect.width - 48,
            modal_rect.height - 84  # Space for title and padding
        )
        
        y_offset = content_rect.y
        for child in self.content:
            child_width, child_height = child.calculate_size(content_rect.width, float('inf'))
            
            child_rect = Rect(
                content_rect.x,
                y_offset,
                min(child_width, content_rect.width),
                child_height
            )
            
            child.layout(child_rect)
            y_offset += child_height + 8
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle modal events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if click is outside modal (close on backdrop click)
            modal_x = self.rect.x + (self.rect.width - self.modal_width) / 2
            modal_y = self.rect.y + (self.rect.height - self.modal_height) / 2
            modal_rect = pygame.Rect(modal_x, modal_y, self.modal_width, self.modal_height)
            
            if not modal_rect.collidepoint(event.pos) and self.closable:
                self.close()
                return True
            
            # Check close button click
            if self.closable:
                close_button_rect = pygame.Rect(
                    modal_x + self.modal_width - 40,
                    modal_y + 8,
                    32, 32
                )
                if close_button_rect.collidepoint(event.pos):
                    self.close()
                    return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.closable:
                self.close()
                return True
        
        # Pass events to content
        for child in self.content:
            if child.handle_event(event):
                return True
        
        return True  # Modal consumes all events
    
    def close(self) -> None:
        """Close the modal"""
        self._is_opening = False
        if self.on_close:
            self.on_close()
    
    def _update_animations(self) -> None:
        """Update modal animations"""
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        # Update animations
        target_backdrop = 1.0 if self._is_opening else 0.0
        target_modal = 1.0 if self._is_opening else 0.0
        
        self._backdrop_animation += (target_backdrop - self._backdrop_animation) * 8.0 * dt
        self._modal_animation += (target_modal - self._modal_animation) * 10.0 * dt
        
        self._backdrop_animation = max(0.0, min(1.0, self._backdrop_animation))
        self._modal_animation = max(0.0, min(1.0, self._modal_animation))
        
        # Request redraw if animating
        if (abs(self._backdrop_animation - target_backdrop) > 0.01 or 
            abs(self._modal_animation - target_modal) > 0.01):
            self.invalidate()
        
        # Remove modal when animation completes
        if not self._is_opening and self._modal_animation < 0.01:
            if self.parent:
                self.parent.remove_child(self)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render modal with backdrop and animations"""
        if not self.visible:
            return
        
        # Update animations
        self._update_animations()
        
        # Get theme
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Draw backdrop
        backdrop_alpha = int(128 * self._backdrop_animation)
        backdrop_color = ModernGraphics.get_color_with_alpha((0, 0, 0), backdrop_alpha)
        
        backdrop_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        backdrop_surface.fill(backdrop_color)
        surface.blit(backdrop_surface, (self.rect.x, self.rect.y))
        
        # Calculate modal rect with animation
        modal_x = self.rect.x + (self.rect.width - self.modal_width) / 2
        modal_y = self.rect.y + (self.rect.height - self.modal_height) / 2
        
        # Apply scale animation
        scale = 0.8 + 0.2 * self._modal_animation
        scaled_width = self.modal_width * scale
        scaled_height = self.modal_height * scale
        scaled_x = modal_x + (self.modal_width - scaled_width) / 2
        scaled_y = modal_y + (self.modal_height - scaled_height) / 2
        
        modal_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw modal shadow
        ModernGraphics.draw_shadow(
            surface,
            modal_rect,
            16,
            blur_radius=20,
            offset=(0, 8),
            color=ModernGraphics.get_color_with_alpha((0, 0, 0), int(40 * self._modal_animation))
        )
        
        # Draw modal background
        modal_bg = pygame.Color(theme.background_color)
        ModernGraphics.draw_rounded_rect(
            surface,
            modal_bg,
            modal_rect,
            16
        )
        
        # Draw title bar
        self._draw_title_bar(surface, modal_rect, theme)
        
        # Render content (only if fully animated)
        if self._modal_animation > 0.8:
            for child in self.content:
                if child.visible:
                    child.render(surface)
    
    def _draw_title_bar(self, surface: pygame.Surface, modal_rect: pygame.Rect, theme) -> None:
        """Draw modal title bar"""
        # Draw title
        title_font = pygame.font.Font(None, 24)
        title_font.set_bold(True)
        title_color = pygame.Color(theme.text_primary)
        title_surface = title_font.render(self.title, True, title_color)
        
        title_x = modal_rect.x + 24
        title_y = modal_rect.y + 20
        surface.blit(title_surface, (title_x, title_y))
        
        # Draw close button
        if self.closable:
            close_x = modal_rect.x + modal_rect.width - 40
            close_y = modal_rect.y + 8
            close_rect = pygame.Rect(close_x, close_y, 32, 32)
            
            # Close button background
            close_bg = ModernGraphics.get_color_with_alpha(theme.text_secondary, 30)
            ModernGraphics.draw_rounded_rect(surface, close_bg, close_rect, 16)
            
            # Close icon (X)
            close_color = pygame.Color(theme.text_secondary)
            pygame.draw.line(surface, close_color, 
                           (close_x + 10, close_y + 10), 
                           (close_x + 22, close_y + 22), 2)
            pygame.draw.line(surface, close_color, 
                           (close_x + 22, close_y + 10), 
                           (close_x + 10, close_y + 22), 2)