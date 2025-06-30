from dataclasses import dataclass, field
from typing import Optional, Union
from lumina.core.types import Color


@dataclass
class Theme:
    """Theme configuration for Lumina applications"""
    
    # Core colors
    primary_color: Color = "#0066CC"
    secondary_color: Color = "#6C757D"
    success_color: Color = "#28A745"
    warning_color: Color = "#FFC107"
    error_color: Color = "#DC3545"
    info_color: Color = "#17A2B8"
    
    # Surface colors
    background_color: Color = "#FFFFFF"
    surface_color: Color = "#F8F9FA"
    overlay_color: Color = "rgba(0, 0, 0, 0.5)"
    
    # Text colors
    text_primary: Color = "#212529"
    text_secondary: Color = "#6C757D"
    text_disabled: Color = "#ADB5BD"
    text_hint: Color = "#6C757D"
    
    # State colors
    hover_overlay: Color = "rgba(0, 0, 0, 0.04)"
    focus_overlay: Color = "rgba(0, 102, 204, 0.12)"
    pressed_overlay: Color = "rgba(0, 0, 0, 0.08)"
    selected_overlay: Color = "rgba(0, 102, 204, 0.08)"
    
    # Border colors
    border_color: Color = "#DEE2E6"
    divider_color: Color = "#E9ECEF"
    
    # Shadows
    shadow_color: Color = "rgba(0, 0, 0, 0.1)"
    
    # Typography
    font_family: str = "system"
    font_size_xs: float = 12
    font_size_sm: float = 14
    font_size_base: float = 16
    font_size_lg: float = 18
    font_size_xl: float = 24
    font_size_xxl: float = 32
    
    # Spacing
    spacing_xs: float = 4
    spacing_sm: float = 8
    spacing_base: float = 16
    spacing_lg: float = 24
    spacing_xl: float = 32
    spacing_xxl: float = 48
    
    # Border radius
    radius_sm: float = 4
    radius_base: float = 8
    radius_lg: float = 12
    radius_xl: float = 16
    radius_full: float = 9999
    
    # Transitions
    transition_fast: float = 150  # milliseconds
    transition_base: float = 250
    transition_slow: float = 400
    
    # Z-index layers
    z_dropdown: int = 1000
    z_modal: int = 1050
    z_popover: int = 1100
    z_tooltip: int = 1150
    z_notification: int = 1200
    
    def derive(self, **overrides) -> "Theme":
        """Create a new theme based on this one with overrides"""
        import copy
        new_theme = copy.deepcopy(self)
        
        for key, value in overrides.items():
            if hasattr(new_theme, key):
                setattr(new_theme, key, value)
        
        return new_theme
    
    @classmethod
    def from_primary_color(cls, primary_color: Color, dark_mode: bool = False) -> "Theme":
        """Generate a theme from a primary color"""
        # This would implement Material Design 3 color generation
        # For now, return a basic theme
        if dark_mode:
            return cls(
                primary_color=primary_color,
                background_color="#121212",
                surface_color="#1E1E1E",
                text_primary="#FFFFFF",
                text_secondary="#B0B0B0",
                border_color="#2E2E2E",
            )
        else:
            return cls(primary_color=primary_color)