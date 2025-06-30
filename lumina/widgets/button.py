from typing import Optional, Callable, Union
import pygame
from lumina.core.widget import Widget
from lumina.core.style import Style
from lumina.core.types import Color, EventType, Rect, Padding


class Button(Widget):
    """Interactive button widget"""
    
    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        variant: str = "primary",
        disabled: bool = False,
        **kwargs
    ):
        # Set default padding if not provided
        if "padding" not in kwargs:
            kwargs["padding"] = Padding.symmetric(vertical=12, horizontal=24)
        
        super().__init__(**kwargs)
        
        self.text = text
        self.on_click = on_click
        self.variant = variant
        self.disabled = disabled
        
        # Button states
        self._is_hovered = False
        self._is_pressed = False
        
        # Apply variant styles
        self._apply_variant_style()
    
    def _apply_variant_style(self) -> None:
        """Apply styles based on button variant"""
        if self.variant == "primary":
            self.style.border_radius = 8
            self.style.font_weight = "600"
            self.style.cursor = "pointer"
        elif self.variant == "secondary":
            self.style.border_radius = 8
            self.style.border_width = 2
            self.style.cursor = "pointer"
        elif self.variant == "text":
            self.style.cursor = "pointer"
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate button size based on text"""
        font = self.style.get_font()
        text_surface = font.render(self.text, True, (0, 0, 0))
        
        width = text_surface.get_width() + self.padding.left + self.padding.right
        height = text_surface.get_height() + self.padding.top + self.padding.bottom
        
        # Apply minimum size
        min_width = 80
        min_height = 36
        
        return max(width, min_width), max(height, min_height)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events"""
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(*event.pos):
                self._is_pressed = True
                self.invalidate()
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._is_pressed
            self._is_pressed = False
            
            if was_pressed and self.contains_point(*event.pos):
                if self.on_click:
                    self.on_click()
                self._emit_event(EventType.CLICK)
                self.invalidate()
                return True
            elif was_pressed:
                self.invalidate()
        
        return False
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the button"""
        if not self.visible:
            return
        
        # Get theme colors
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Determine colors based on variant and state
        if self.disabled:
            bg_color = pygame.Color(theme.surface_color)
            text_color = pygame.Color(theme.text_disabled)
            border_color = pygame.Color(theme.border_color)
        elif self.variant == "primary":
            bg_color = pygame.Color(theme.primary_color)
            text_color = pygame.Color("#FFFFFF")
            border_color = bg_color
            
            # Apply state overlays
            if self._is_pressed:
                bg_color = self._apply_overlay(bg_color, (0, 0, 0), 0.2)
            elif self._is_hovered:
                bg_color = self._apply_overlay(bg_color, (255, 255, 255), 0.1)
        
        elif self.variant == "secondary":
            bg_color = pygame.Color(theme.background_color)
            text_color = pygame.Color(theme.primary_color)
            border_color = pygame.Color(theme.primary_color)
            
            if self._is_pressed:
                bg_color = pygame.Color(theme.primary_color)
                text_color = pygame.Color("#FFFFFF")
            elif self._is_hovered:
                primary_color = pygame.Color(theme.primary_color)
                bg_color = self._apply_overlay(bg_color, primary_color, 0.05)
        
        else:  # text variant
            bg_color = None
            text_color = pygame.Color(theme.primary_color)
            border_color = None
            
            if self._is_pressed or self._is_hovered:
                bg_color = self._apply_overlay(
                    pygame.Color(theme.background_color),
                    theme.primary_color,
                    0.05
                )
        
        # Draw background
        if bg_color:
            if self.style.border_radius > 0:
                pygame.draw.rect(
                    surface,
                    bg_color,
                    self.rect.to_pygame_rect(),
                    border_radius=int(self.style.border_radius)
                )
            else:
                pygame.draw.rect(surface, bg_color, self.rect.to_pygame_rect())
        
        # Draw border
        if border_color and self.style.border_width > 0:
            pygame.draw.rect(
                surface,
                border_color,
                self.rect.to_pygame_rect(),
                width=int(self.style.border_width),
                border_radius=int(self.style.border_radius)
            )
        
        # Draw text
        font = self.style.get_font()
        text_surface = font.render(self.text, True, text_color)
        
        # Center text
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        
        surface.blit(text_surface, (text_x, text_y))
        
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self._is_hovered
        self._is_hovered = self.contains_point(*mouse_pos) and not self.disabled
        
        if was_hovered != self._is_hovered:
            self.invalidate()
    
    def _apply_overlay(self, base_color: pygame.Color, overlay_color: Union[pygame.Color, tuple], alpha: float) -> pygame.Color:
        """Apply an overlay color with alpha blending"""
        if isinstance(overlay_color, tuple):
            overlay = pygame.Color(*overlay_color)
        else:
            overlay = overlay_color
        
        r = int(base_color.r * (1 - alpha) + overlay.r * alpha)
        g = int(base_color.g * (1 - alpha) + overlay.g * alpha)
        b = int(base_color.b * (1 - alpha) + overlay.b * alpha)
        
        return pygame.Color(r, g, b)