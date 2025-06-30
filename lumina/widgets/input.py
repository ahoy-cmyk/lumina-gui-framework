from typing import Optional, Callable, Union
import pygame
import time
from lumina.core.widget import Widget
from lumina.core.style import Style
from lumina.core.types import Color, EventType, Rect, Padding
from lumina.core.graphics import ModernGraphics


class TextInput(Widget):
    """Modern text input with floating label and smooth animations"""
    
    def __init__(
        self,
        placeholder: str = "",
        value: str = "",
        label: Optional[str] = None,
        variant: str = "outlined",  # outlined, filled, underlined
        size: str = "medium",
        disabled: bool = False,
        multiline: bool = False,
        password: bool = False,
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        # Set default padding
        if "padding" not in kwargs:
            size_padding = {
                "small": Padding.symmetric(vertical=8, horizontal=12),
                "medium": Padding.symmetric(vertical=12, horizontal=16),
                "large": Padding.symmetric(vertical=16, horizontal=20),
            }
            kwargs["padding"] = size_padding.get(size, size_padding["medium"])
        
        super().__init__(**kwargs)
        
        self.placeholder = placeholder
        self.value = value
        self.label = label
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.multiline = multiline
        self.password = password
        self.on_change = on_change
        self.on_submit = on_submit
        
        # Input state
        self._is_focused = False
        self._is_hovered = False
        self._cursor_position = len(value)
        self._selection_start = 0
        self._selection_end = 0
        self._cursor_visible = True
        self._last_cursor_blink = time.time()
        self._scroll_offset = 0
        
        # Animation states
        self._focus_animation = 0.0
        self._label_animation = 1.0 if value else 0.0
        self._last_update = time.time()
        
        # Style configuration
        self._apply_size_style()
    
    def _apply_size_style(self) -> None:
        """Apply styles based on input size"""
        size_styles = {
            "small": {"font_size": 14, "border_radius": 6},
            "medium": {"font_size": 16, "border_radius": 8},
            "large": {"font_size": 18, "border_radius": 10},
        }
        
        style_props = size_styles.get(self.size, size_styles["medium"])
        for prop, value in style_props.items():
            setattr(self.style, prop, value)
        
        self.style.cursor = "text" if not self.disabled else "default"
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate input size"""
        font = self.style.get_font()
        
        # Base height from font + padding
        font_height = font.get_height()
        total_height = font_height + self.padding.top + self.padding.bottom
        
        # Add space for floating label
        if self.label:
            total_height += 20
        
        # Minimum width
        min_width = 200
        
        # For multiline, add extra height
        if self.multiline:
            total_height *= 3  # Default to 3 lines
        
        return min_width, total_height
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events"""
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(*event.pos):
                self._is_focused = True
                self._place_cursor_at_position(event.pos[0])
                self.invalidate()
                return True
            else:
                if self._is_focused:
                    self._is_focused = False
                    self.invalidate()
        
        elif event.type == pygame.MOUSEMOTION:
            was_hovered = self._is_hovered
            self._is_hovered = self.contains_point(*event.pos)
            if was_hovered != self._is_hovered:
                self.invalidate()
        
        elif event.type == pygame.KEYDOWN and self._is_focused:
            return self._handle_key_event(event)
        
        return False
    
    def _handle_key_event(self, event: pygame.event.Event) -> bool:
        """Handle keyboard input"""
        if event.key == pygame.K_RETURN:
            if not self.multiline:
                if self.on_submit:
                    self.on_submit(self.value)
                self._emit_event(EventType.SUBMIT, self.value)
                return True
            else:
                self._insert_text("\n")
                return True
        
        elif event.key == pygame.K_BACKSPACE:
            if self._cursor_position > 0:
                self.value = self.value[:self._cursor_position-1] + self.value[self._cursor_position:]
                self._cursor_position -= 1
                self._on_value_changed()
                return True
        
        elif event.key == pygame.K_DELETE:
            if self._cursor_position < len(self.value):
                self.value = self.value[:self._cursor_position] + self.value[self._cursor_position+1:]
                self._on_value_changed()
                return True
        
        elif event.key == pygame.K_LEFT:
            self._cursor_position = max(0, self._cursor_position - 1)
            self.invalidate()
            return True
        
        elif event.key == pygame.K_RIGHT:
            self._cursor_position = min(len(self.value), self._cursor_position + 1)
            self.invalidate()
            return True
        
        elif event.key == pygame.K_HOME:
            self._cursor_position = 0
            self.invalidate()
            return True
        
        elif event.key == pygame.K_END:
            self._cursor_position = len(self.value)
            self.invalidate()
            return True
        
        elif event.unicode and event.unicode.isprintable():
            self._insert_text(event.unicode)
            return True
        
        return False
    
    def _insert_text(self, text: str) -> None:
        """Insert text at cursor position"""
        self.value = self.value[:self._cursor_position] + text + self.value[self._cursor_position:]
        self._cursor_position += len(text)
        self._on_value_changed()
    
    def _on_value_changed(self) -> None:
        """Handle value change"""
        if self.on_change:
            self.on_change(self.value)
        self._emit_event(EventType.CHANGE, self.value)
        self.invalidate()
    
    def _place_cursor_at_position(self, x: float) -> None:
        """Place cursor at screen position"""
        font = self.style.get_font()
        text_x = self.rect.x + self.padding.left - self._scroll_offset
        
        # Find closest character position
        best_pos = 0
        best_distance = float('inf')
        
        for i in range(len(self.value) + 1):
            text_width = font.size(self.value[:i])[0]
            char_x = text_x + text_width
            distance = abs(x - char_x)
            
            if distance < best_distance:
                best_distance = distance
                best_pos = i
        
        self._cursor_position = best_pos
        self.invalidate()
    
    def _update_animations(self) -> None:
        """Update animation states"""
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        # Update focus animation
        target_focus = 1.0 if self._is_focused else 0.0
        self._focus_animation += (target_focus - self._focus_animation) * 8.0 * dt
        self._focus_animation = max(0.0, min(1.0, self._focus_animation))
        
        # Update label animation (float up when focused or has value)
        target_label = 1.0 if (self._is_focused or self.value) else 0.0
        self._label_animation += (target_label - self._label_animation) * 8.0 * dt
        self._label_animation = max(0.0, min(1.0, self._label_animation))
        
        # Update cursor blink
        if current_time - self._last_cursor_blink > 0.5:
            self._cursor_visible = not self._cursor_visible
            self._last_cursor_blink = current_time
        
        # Request redraw if animating
        if (abs(self._focus_animation - target_focus) > 0.01 or 
            abs(self._label_animation - target_label) > 0.01):
            self.invalidate()
    
    def render(self, surface: pygame.Surface) -> None:
        """Render modern text input"""
        if not self.visible:
            return
        
        # Update animations
        self._update_animations()
        
        # Get theme colors
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Calculate colors based on state
        bg_color, border_color, text_color = self._get_input_colors(theme)
        
        # Draw input background
        if self.variant == "filled":
            ModernGraphics.draw_rounded_rect(
                surface,
                bg_color,
                self.rect.to_pygame_rect(),
                self.style.border_radius
            )
        elif self.variant == "outlined":
            # Draw background
            if bg_color:
                ModernGraphics.draw_rounded_rect(
                    surface,
                    bg_color,
                    self.rect.to_pygame_rect(),
                    self.style.border_radius
                )
            
            # Draw border
            border_width = 2 if self._is_focused else 1
            ModernGraphics.draw_rounded_rect(
                surface,
                border_color,
                self.rect.to_pygame_rect(),
                self.style.border_radius,
                width=border_width
            )
        elif self.variant == "underlined":
            # Draw underline
            underline_y = self.rect.y + self.rect.height - 2
            underline_width = 2 if self._is_focused else 1
            pygame.draw.line(
                surface,
                border_color,
                (self.rect.x, underline_y),
                (self.rect.x + self.rect.width, underline_y),
                underline_width
            )
        
        # Draw floating label
        if self.label:
            self._draw_floating_label(surface, theme)
        
        # Draw text content
        self._draw_text_content(surface, text_color)
        
        # Draw cursor if focused
        if self._is_focused and self._cursor_visible:
            self._draw_cursor(surface, text_color)
    
    def _get_input_colors(self, theme) -> tuple[Optional[pygame.Color], pygame.Color, pygame.Color]:
        """Get input colors based on state"""
        if self.disabled:
            return (
                pygame.Color(theme.surface_color),
                pygame.Color(theme.border_color),
                pygame.Color(theme.text_disabled)
            )
        
        # Background color
        if self.variant == "filled":
            bg_color = pygame.Color(theme.surface_color)
            if self._is_hovered:
                bg_color = ModernGraphics.lighten_color(bg_color, 0.05)
        else:
            bg_color = pygame.Color(theme.background_color)
        
        # Border color
        if self._is_focused:
            border_color = pygame.Color(theme.primary_color)
        elif self._is_hovered:
            border_color = pygame.Color(theme.text_secondary)
        else:
            border_color = pygame.Color(theme.border_color)
        
        # Text color
        text_color = pygame.Color(theme.text_primary)
        
        return bg_color, border_color, text_color
    
    def _draw_floating_label(self, surface: pygame.Surface, theme) -> None:
        """Draw floating label with animation"""
        if not self.label:
            return
        
        # Calculate label properties based on animation
        label_font_size = int(12 + (16 - 12) * (1 - self._label_animation))
        label_color = pygame.Color(theme.primary_color) if self._is_focused else pygame.Color(theme.text_secondary)
        
        # Create label font
        label_font = pygame.font.Font(None, label_font_size)
        label_surface = label_font.render(self.label, True, label_color)
        
        # Calculate label position
        if self._label_animation > 0.5:
            # Floating position
            label_x = self.rect.x + self.padding.left
            label_y = self.rect.y + 4
        else:
            # Placeholder position
            label_x = self.rect.x + self.padding.left
            label_y = self.rect.y + self.padding.top + (self.rect.height - self.padding.top - self.padding.bottom - label_surface.get_height()) / 2
        
        # Interpolate position
        final_x = label_x
        final_y = label_y * self._label_animation + (self.rect.y + self.padding.top + 8) * (1 - self._label_animation)
        
        surface.blit(label_surface, (final_x, final_y))
    
    def _draw_text_content(self, surface: pygame.Surface, text_color: pygame.Color) -> None:
        """Draw text content with proper scrolling"""
        font = self.style.get_font()
        
        # Determine display text
        display_text = self.value
        if self.password:
            display_text = "•" * len(self.value)
        
        # Show placeholder if no value and not focused
        if not display_text and not self._is_focused and self.placeholder:
            display_text = self.placeholder
            text_color = pygame.Color(self.window.theme.text_hint if self.window else "#999999")
        
        if display_text:
            # Calculate text position
            text_y_offset = 20 if self.label and self._label_animation > 0.5 else 0
            text_x = self.rect.x + self.padding.left - self._scroll_offset
            text_y = self.rect.y + self.padding.top + text_y_offset
            
            # Render text
            text_surface = font.render(display_text, True, text_color)
            
            # Create clipping rect
            clip_rect = pygame.Rect(
                self.rect.x + self.padding.left,
                self.rect.y,
                self.rect.width - self.padding.left - self.padding.right,
                self.rect.height
            )
            
            # Draw with clipping
            surface.set_clip(clip_rect)
            surface.blit(text_surface, (text_x, text_y))
            surface.set_clip(None)
    
    def _draw_cursor(self, surface: pygame.Surface, text_color: pygame.Color) -> None:
        """Draw blinking cursor"""
        font = self.style.get_font()
        
        # Calculate cursor position
        text_before_cursor = self.value[:self._cursor_position]
        if self.password:
            text_before_cursor = "•" * len(text_before_cursor)
        
        text_width = font.size(text_before_cursor)[0]
        text_y_offset = 20 if self.label and self._label_animation > 0.5 else 0
        
        cursor_x = self.rect.x + self.padding.left + text_width - self._scroll_offset
        cursor_y = self.rect.y + self.padding.top + text_y_offset
        cursor_height = font.get_height()
        
        # Draw cursor line
        pygame.draw.line(
            surface,
            text_color,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + cursor_height),
            2
        )