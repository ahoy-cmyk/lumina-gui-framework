from typing import Optional, Callable, Union
import pygame
import time
from lumina.core.widget import Widget
from lumina.core.style import Style
from lumina.core.types import Color, EventType, Rect, Padding
from lumina.core.graphics import ModernGraphics


class ModernButton(Widget):
    """Modern button with smooth animations and beautiful design"""
    
    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        variant: str = "primary",
        size: str = "medium",
        disabled: bool = False,
        icon: Optional[str] = None,
        **kwargs
    ):
        # Set default padding based on size
        if "padding" not in kwargs:
            size_padding = {
                "small": Padding.symmetric(vertical=8, horizontal=16),
                "medium": Padding.symmetric(vertical=12, horizontal=24),
                "large": Padding.symmetric(vertical=16, horizontal=32),
            }
            kwargs["padding"] = size_padding.get(size, size_padding["medium"])
        
        super().__init__(**kwargs)
        
        self.text = text
        self.on_click = on_click
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.icon = icon
        
        # Animation states
        self._is_hovered = False
        self._is_pressed = False
        self._hover_animation = 0.0  # 0.0 to 1.0
        self._press_animation = 0.0  # 0.0 to 1.0
        self._last_update = time.time()
        
        # Style configuration
        self._apply_size_style()
        self._setup_animations()
    
    def _apply_size_style(self) -> None:
        """Apply styles based on button size"""
        size_styles = {
            "small": {"font_size": 14, "border_radius": 6},
            "medium": {"font_size": 16, "border_radius": 8},
            "large": {"font_size": 18, "border_radius": 10},
        }
        
        style_props = size_styles.get(self.size, size_styles["medium"])
        for prop, value in style_props.items():
            setattr(self.style, prop, value)
        
        self.style.font_weight = "600"
        self.style.cursor = "pointer" if not self.disabled else "default"
    
    def _setup_animations(self) -> None:
        """Setup animation parameters"""
        self.animation_speed = 8.0  # Animation speed multiplier
        self.hover_scale = 1.02  # Scale on hover
        self.press_scale = 0.98  # Scale when pressed
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate button size with modern proportions"""
        font = self.style.get_font()
        text_surface = font.render(self.text, True, (0, 0, 0))
        
        # Base size from text
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        
        # Add icon space if present
        icon_width = 20 if self.icon else 0
        icon_spacing = 8 if self.icon else 0
        
        # Calculate total size
        content_width = text_width + icon_width + icon_spacing
        content_height = max(text_height, 20)  # Minimum 20px height for icons
        
        total_width = content_width + self.padding.left + self.padding.right
        total_height = content_height + self.padding.top + self.padding.bottom
        
        # Apply minimum sizes based on variant
        min_sizes = {
            "small": (60, 32),
            "medium": (80, 40),
            "large": (100, 48),
        }
        min_width, min_height = min_sizes.get(self.size, min_sizes["medium"])
        
        return max(total_width, min_width), max(total_height, min_height)
    
    def _update_animations(self) -> None:
        """Update animation states - simplified to prevent text pulsing"""
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        # Snap animations to target instantly to prevent render loops
        # This fixes the text pulsing issue caused by constant invalidation
        target_hover = 1.0 if self._is_hovered and not self.disabled else 0.0
        target_press = 1.0 if self._is_pressed and not self.disabled else 0.0
        
        # Store old values to check if we changed
        old_hover = self._hover_animation
        old_press = self._press_animation
        
        # Snap directly to target (no smooth animation for now to fix pulsing)
        self._hover_animation = target_hover
        self._press_animation = target_press
        
        # Only invalidate once when state actually changes
        if (old_hover != self._hover_animation or old_press != self._press_animation):
            self.invalidate()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events with smooth animations"""
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self._is_hovered
            self._is_hovered = self.contains_point(*event.pos)
            if was_hovered != self._is_hovered:
                self.invalidate()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        """Render modern button with animations"""
        if not self.visible:
            return
        
        # Update animations only when state might have changed
        # This prevents constant re-rendering that causes text pulsing
        self._update_animations()
        
        # Get theme colors
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Calculate animated scale
        scale = 1.0
        if not self.disabled:
            scale += (self.hover_scale - 1.0) * self._hover_animation
            scale += (self.press_scale - 1.0) * self._press_animation
        
        # Calculate scaled rect
        scaled_width = self.rect.width * scale
        scaled_height = self.rect.height * scale
        scaled_x = self.rect.x + (self.rect.width - scaled_width) / 2
        scaled_y = self.rect.y + (self.rect.height - scaled_height) / 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw shadow first
        if not self.disabled and self.variant != "text":
            shadow_alpha = int(20 + 10 * self._hover_animation)
            shadow_offset = (0, int(2 + 2 * self._hover_animation))
            ModernGraphics.draw_shadow(
                surface,
                scaled_rect,
                self.style.border_radius,
                blur_radius=4 + 2 * self._hover_animation,
                offset=shadow_offset,
                color=ModernGraphics.get_color_with_alpha((0, 0, 0), shadow_alpha)
            )
        
        # Determine colors based on variant and state
        bg_color, text_color, border_color = self._get_button_colors(theme)
        
        # Draw button background
        if bg_color:
            ModernGraphics.draw_rounded_rect(
                surface,
                bg_color,
                scaled_rect,
                self.style.border_radius
            )
        
        # Draw border for outlined variants
        if border_color and self.variant in ["secondary", "outlined"]:
            ModernGraphics.draw_rounded_rect(
                surface,
                border_color,
                scaled_rect,
                self.style.border_radius,
                width=2
            )
        
        # Draw button content (icon + text)
        self._draw_button_content(surface, scaled_rect, text_color)
    
    def _get_button_colors(self, theme) -> tuple[Optional[pygame.Color], pygame.Color, Optional[pygame.Color]]:
        """Get button colors based on variant and state"""
        if self.disabled:
            return (
                pygame.Color(theme.surface_color),
                pygame.Color(theme.text_disabled),
                pygame.Color(theme.border_color)
            )
        
        if self.variant == "primary":
            bg_color = pygame.Color(theme.primary_color)
            text_color = pygame.Color("#FFFFFF")
            
            # Apply state effects
            if self._press_animation > 0:
                bg_color = ModernGraphics.darken_color(bg_color, 0.1 * self._press_animation)
            elif self._hover_animation > 0:
                bg_color = ModernGraphics.lighten_color(bg_color, 0.1 * self._hover_animation)
            
            return bg_color, text_color, None
        
        elif self.variant == "secondary":
            bg_color = pygame.Color(theme.background_color)
            text_color = pygame.Color(theme.primary_color)
            border_color = pygame.Color(theme.primary_color)
            
            # Apply hover effects
            if self._press_animation > 0:
                bg_color = pygame.Color(theme.primary_color)
                text_color = pygame.Color("#FFFFFF")
            elif self._hover_animation > 0:
                overlay_alpha = int(20 * self._hover_animation)
                bg_color = ModernGraphics.get_color_with_alpha(theme.primary_color, overlay_alpha)
            
            return bg_color, text_color, border_color
        
        elif self.variant == "success":
            bg_color = pygame.Color(theme.success_color)
            text_color = pygame.Color("#FFFFFF")
            
            if self._press_animation > 0:
                bg_color = ModernGraphics.darken_color(bg_color, 0.1 * self._press_animation)
            elif self._hover_animation > 0:
                bg_color = ModernGraphics.lighten_color(bg_color, 0.1 * self._hover_animation)
            
            return bg_color, text_color, None
        
        elif self.variant == "danger":
            bg_color = pygame.Color(theme.error_color)
            text_color = pygame.Color("#FFFFFF")
            
            if self._press_animation > 0:
                bg_color = ModernGraphics.darken_color(bg_color, 0.1 * self._press_animation)
            elif self._hover_animation > 0:
                bg_color = ModernGraphics.lighten_color(bg_color, 0.1 * self._hover_animation)
            
            return bg_color, text_color, None
        
        else:  # text variant
            bg_color = None
            text_color = pygame.Color(theme.primary_color)
            
            if self._press_animation > 0 or self._hover_animation > 0:
                alpha = int(30 * max(self._press_animation, self._hover_animation * 0.5))
                bg_color = ModernGraphics.get_color_with_alpha(theme.primary_color, alpha)
            
            return bg_color, text_color, None
    
    def _draw_button_content(self, surface: pygame.Surface, rect: pygame.Rect, text_color: pygame.Color) -> None:
        """Draw button content (icon + text) with proper spacing"""
        font = self.style.get_font()
        text_surface = font.render(self.text, True, text_color)
        
        # Calculate content positioning
        icon_width = 20 if self.icon else 0
        icon_spacing = 8 if self.icon and self.text else 0
        total_content_width = text_surface.get_width() + icon_width + icon_spacing
        
        # Center content in button
        content_x = rect.x + (rect.width - total_content_width) / 2
        content_y = rect.y + (rect.height - text_surface.get_height()) / 2
        
        # Draw icon if present
        if self.icon:
            icon_rect = pygame.Rect(content_x, rect.y + (rect.height - 20) / 2, 20, 20)
            self._draw_icon(surface, icon_rect, text_color)
            content_x += icon_width + icon_spacing
        
        # Draw text
        surface.blit(text_surface, (content_x, content_y))
    
    def _draw_icon(self, surface: pygame.Surface, rect: pygame.Rect, color: pygame.Color) -> None:
        """Draw button icon (placeholder - would use actual icon system)"""
        # For now, draw a simple shape as placeholder
        if self.icon == "check":
            # Draw checkmark
            points = [
                (rect.x + 4, rect.y + 10),
                (rect.x + 8, rect.y + 14),
                (rect.x + 16, rect.y + 6)
            ]
            pygame.draw.lines(surface, color, False, points, 2)
        elif self.icon == "plus":
            # Draw plus sign
            pygame.draw.line(surface, color, 
                           (rect.x + 10, rect.y + 4), 
                           (rect.x + 10, rect.y + 16), 2)
            pygame.draw.line(surface, color, 
                           (rect.x + 4, rect.y + 10), 
                           (rect.x + 16, rect.y + 10), 2)
        elif self.icon == "close":
            # Draw X
            pygame.draw.line(surface, color, 
                           (rect.x + 4, rect.y + 4), 
                           (rect.x + 16, rect.y + 16), 2)
            pygame.draw.line(surface, color, 
                           (rect.x + 16, rect.y + 4), 
                           (rect.x + 4, rect.y + 16), 2)


# Alias for backwards compatibility
Button = ModernButton