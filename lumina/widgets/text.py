from typing import Optional, Union
import pygame
from lumina.core.widget import Widget
from lumina.core.style import Style
from lumina.core.types import Color


class Text(Widget):
    """Basic text widget"""
    
    def __init__(
        self,
        text: str,
        style: Optional[Union[str, Style]] = None,
        color: Optional[Color] = None,
        **kwargs
    ):
        # Handle style presets
        if isinstance(style, str):
            style_obj = self._get_style_preset(style)
        else:
            style_obj = style or Style()
        
        super().__init__(style=style_obj, **kwargs)
        
        self.text = text
        if color:
            self.style.foreground_color = color
        
        self._rendered_text: Optional[pygame.Surface] = None
        self._last_text: Optional[str] = None
    
    def _get_style_preset(self, preset: str) -> Style:
        """Get predefined text styles"""
        if preset == "heading":
            return Style(font_size=32, font_weight="bold")
        elif preset == "subheading":
            return Style(font_size=24, font_weight="600")
        elif preset == "body":
            return Style(font_size=16)
        elif preset == "caption":
            return Style(font_size=14, opacity=0.7)
        elif preset == "small":
            return Style(font_size=12)
        else:
            return Style()
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate text size"""
        from lumina.core.text_renderer import TextRenderer
        
        text_width, text_height = TextRenderer.get_text_size(self.text, self.style)
        
        width = text_width + self.padding.left + self.padding.right
        height = text_height + self.padding.top + self.padding.bottom
        
        return width, height
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the text"""
        if not self.visible:
            return
        
        # Render text if needed
        if self._rendered_text is None or self._last_text != self.text:
            from lumina.core.text_renderer import TextRenderer
            
            # Get text color
            if self.style.foreground_color:
                color = self.style.to_pygame_color(self.style.foreground_color)
            elif self.window and self.window.theme:
                color = pygame.Color(self.window.theme.text_primary)
            else:
                color = pygame.Color("black")
            
            # Render with advanced text renderer (supports emojis)
            self._rendered_text = TextRenderer.render_text(self.text, self.style, color)
            self._last_text = self.text
        
        # Calculate position
        x = self.rect.x + self.padding.left
        y = self.rect.y + self.padding.top
        
        # Apply text alignment
        if self.style.text_align == "center":
            x = self.rect.x + (self.rect.width - self._rendered_text.get_width()) // 2
        elif self.style.text_align == "right":
            x = self.rect.x + self.rect.width - self._rendered_text.get_width() - self.padding.right
        
        # Draw text
        surface.blit(self._rendered_text, (x, y))


class Header(Text):
    """Header text widget"""
    
    def __init__(self, text: str, level: int = 1, **kwargs):
        # Set font size based on header level
        font_sizes = {1: 32, 2: 28, 3: 24, 4: 20, 5: 18, 6: 16}
        font_size = font_sizes.get(level, 16)
        
        style = Style(font_size=font_size, font_weight="bold")
        super().__init__(text, style=style, **kwargs)


class Paragraph(Text):
    """Paragraph text widget with word wrapping"""
    
    def __init__(self, text: str, **kwargs):
        style = Style(font_size=16)
        super().__init__(text, style=style, **kwargs)
    
    # TODO: Implement word wrapping in calculate_size and render methods