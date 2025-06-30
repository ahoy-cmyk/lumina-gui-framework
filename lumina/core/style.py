from dataclasses import dataclass, field
from typing import Optional, Union
from lumina.core.types import Color
import pygame


@dataclass
class Style:
    """Style properties for widgets"""
    
    # Colors
    background_color: Optional[Color] = None
    foreground_color: Optional[Color] = None
    border_color: Optional[Color] = None
    
    # Borders
    border_width: float = 0
    border_radius: float = 0
    
    # Typography
    font_family: str = "system"
    font_size: float = 14
    font_weight: str = "normal"
    font_style: str = "normal"
    
    # Layout
    width: Optional[Union[float, str]] = None
    height: Optional[Union[float, str]] = None
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    min_height: Optional[float] = None
    max_height: Optional[float] = None
    
    # Spacing
    padding_top: float = 0
    padding_right: float = 0
    padding_bottom: float = 0
    padding_left: float = 0
    margin_top: float = 0
    margin_right: float = 0
    margin_bottom: float = 0
    margin_left: float = 0
    
    # Alignment
    text_align: str = "left"
    vertical_align: str = "top"
    
    # Effects
    opacity: float = 1.0
    shadow: Optional[dict] = None
    
    # Transforms
    scale: float = 1.0
    rotation: float = 0.0
    
    # Cursor
    cursor: str = "default"
    
    # Transitions
    transition_duration: float = 0.0
    transition_property: Optional[str] = None
    
    def merge(self, other: "Style") -> "Style":
        """Merge another style into this one, with other taking precedence"""
        result = Style()
        
        # Copy all attributes from self
        for attr in vars(self):
            setattr(result, attr, getattr(self, attr))
        
        # Override with non-None values from other
        for attr in vars(other):
            value = getattr(other, attr)
            if value is not None:
                setattr(result, attr, value)
        
        return result
    
    def to_pygame_color(self, color: Optional[Color]) -> Optional[pygame.Color]:
        """Convert color to pygame Color object"""
        if color is None:
            return None
        
        if isinstance(color, str):
            # Handle named colors or hex colors
            return pygame.Color(color)
        elif isinstance(color, (tuple, list)):
            return pygame.Color(*color)
        
        return None
    
    def get_font(self) -> pygame.font.Font:
        """Get pygame font object based on style settings"""
        # Initialize pygame font if not already done
        if not pygame.font.get_init():
            pygame.font.init()
        
        # Check if we have a cached font for this exact style
        cache_key = (self.font_family, self.font_size, self.font_weight, self.font_style)
        if hasattr(self, '_font_cache') and cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        if not hasattr(self, '_font_cache'):
            self._font_cache = {}
        
        # Map font weights to pygame font styles
        bold = self.font_weight in ["bold", "600", "700", "800", "900"]
        italic = self.font_style == "italic"
        
        # Get high-quality fonts with better kerning
        font_name = None
        
        # Better font selection for quality and kerning
        if self.font_family == "system":
            import sys
            
            if sys.platform == "darwin":  # macOS
                # Use fonts known for crisp rendering on macOS
                preferred_fonts = [
                    "SF Pro Text",         # Native San Francisco font
                    "Helvetica",           # Classic, crisp font
                    "Arial",               # Universal fallback
                ]
            elif sys.platform == "win32":  # Windows
                preferred_fonts = [
                    "Segoe UI",
                    "Calibri", 
                    "Arial",
                ]
            else:  # Linux
                preferred_fonts = [
                    "Ubuntu",
                    "Liberation Sans",
                    "DejaVu Sans",
                    "Arial",
                ]
            
            # Try to find the best available font
            available_fonts = pygame.font.get_fonts()
            for font in preferred_fonts:
                # Try exact match first
                if font in pygame.font.get_fonts():
                    font_name = font
                    break
                # Try case-insensitive match
                font_key = font.lower().replace(" ", "").replace(".", "")
                for available in available_fonts:
                    if font_key in available.lower():
                        font_name = available
                        break
                if font_name:
                    break
            
            if not font_name:
                font_name = pygame.font.get_default_font()
        else:
            # Check if requested font exists
            if self.font_family.lower().replace(" ", "") in pygame.font.get_fonts():
                font_name = self.font_family
        
        # Scale font size for high DPI displays
        from lumina.core.display import DisplayManager
        font_size = DisplayManager.scale_font_size(self.font_size)
        
        if font_name:
            font = pygame.font.SysFont(font_name, int(font_size), bold, italic)
        else:
            # Fallback to default font
            font = pygame.font.Font(None, int(font_size))
        
        # Cache the font for future use
        self._font_cache[cache_key] = font
        return font