"""
Modern graphics utilities for smooth, anti-aliased rendering
"""
import pygame
import numpy as np
from typing import Tuple, Union, Optional
from lumina.core.types import Color, Rect
import math


class ModernGraphics:
    """High-quality graphics rendering utilities"""
    
    @staticmethod
    def draw_rounded_rect(
        surface: pygame.Surface,
        color: pygame.Color,
        rect: pygame.Rect,
        radius: float,
        width: int = 0,
        border_color: Optional[pygame.Color] = None,
        border_width: int = 0
    ) -> None:
        """Draw a rounded rectangle with smooth anti-aliasing"""
        if radius <= 0:
            pygame.draw.rect(surface, color, rect, width)
            return
        
        # Ensure radius doesn't exceed half the smaller dimension
        max_radius = min(rect.width, rect.height) // 2
        radius = min(radius, max_radius)
        
        # Create a temporary surface for anti-aliasing
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))
        
        # Draw rounded rectangle on temp surface
        if width == 0:  # Filled rectangle
            ModernGraphics._draw_filled_rounded_rect(temp_surface, color, radius)
        else:  # Outlined rectangle
            ModernGraphics._draw_outlined_rounded_rect(temp_surface, color, radius, width)
        
        # Draw border if specified
        if border_color and border_width > 0:
            ModernGraphics._draw_outlined_rounded_rect(
                temp_surface, border_color, radius, border_width
            )
        
        # Blit with anti-aliasing
        surface.blit(temp_surface, (rect.x, rect.y))
    
    @staticmethod
    def _draw_filled_rounded_rect(surface: pygame.Surface, color: pygame.Color, radius: float) -> None:
        """Draw a filled rounded rectangle"""
        width, height = surface.get_size()
        
        # Draw corner circles
        pygame.draw.circle(surface, color, (int(radius), int(radius)), int(radius))
        pygame.draw.circle(surface, color, (int(width - radius), int(radius)), int(radius))
        pygame.draw.circle(surface, color, (int(radius), int(height - radius)), int(radius))
        pygame.draw.circle(surface, color, (int(width - radius), int(height - radius)), int(radius))
        
        # Draw rectangles to connect corners
        pygame.draw.rect(surface, color, (radius, 0, width - 2 * radius, height))
        pygame.draw.rect(surface, color, (0, radius, width, height - 2 * radius))
    
    @staticmethod
    def _draw_outlined_rounded_rect(
        surface: pygame.Surface, 
        color: pygame.Color, 
        radius: float, 
        width: int
    ) -> None:
        """Draw an outlined rounded rectangle"""
        w, h = surface.get_size()
        
        # Draw corner arcs
        ModernGraphics._draw_arc(surface, color, (0, 0, 2*radius, 2*radius), 
                                math.pi, 3*math.pi/2, width)
        ModernGraphics._draw_arc(surface, color, (w-2*radius, 0, 2*radius, 2*radius), 
                                3*math.pi/2, 2*math.pi, width)
        ModernGraphics._draw_arc(surface, color, (w-2*radius, h-2*radius, 2*radius, 2*radius), 
                                0, math.pi/2, width)
        ModernGraphics._draw_arc(surface, color, (0, h-2*radius, 2*radius, 2*radius), 
                                math.pi/2, math.pi, width)
        
        # Draw straight lines
        pygame.draw.line(surface, color, (radius, 0), (w-radius, 0), width)
        pygame.draw.line(surface, color, (w, radius), (w, h-radius), width)
        pygame.draw.line(surface, color, (w-radius, h), (radius, h), width)
        pygame.draw.line(surface, color, (0, h-radius), (0, radius), width)
    
    @staticmethod
    def _draw_arc(surface: pygame.Surface, color: pygame.Color, rect: Tuple[int, int, int, int], 
                  start_angle: float, end_angle: float, width: int) -> None:
        """Draw a smooth arc"""
        pygame.draw.arc(surface, color, rect, start_angle, end_angle, width)
    
    @staticmethod
    def draw_shadow(
        surface: pygame.Surface,
        rect: pygame.Rect,
        radius: float,
        blur_radius: float = 4,
        offset: Tuple[int, int] = (0, 2),
        color: pygame.Color = pygame.Color(0, 0, 0, 30)
    ) -> None:
        """Draw a modern drop shadow"""
        shadow_rect = pygame.Rect(
            rect.x + offset[0],
            rect.y + offset[1],
            rect.width,
            rect.height
        )
        
        # Create shadow surface
        shadow_surface = pygame.Surface(
            (rect.width + blur_radius * 2, rect.height + blur_radius * 2),
            pygame.SRCALPHA
        )
        
        # Draw shadow shape
        ModernGraphics.draw_rounded_rect(
            shadow_surface,
            color,
            pygame.Rect(blur_radius, blur_radius, rect.width, rect.height),
            radius
        )
        
        # Apply blur effect (simplified)
        ModernGraphics._apply_blur(shadow_surface, blur_radius)
        
        # Blit shadow
        surface.blit(shadow_surface, (shadow_rect.x - blur_radius, shadow_rect.y - blur_radius))
    
    @staticmethod
    def _apply_blur(surface: pygame.Surface, radius: float) -> None:
        """Apply a simple blur effect (placeholder for more complex blur)"""
        # This is a simplified blur - in a real implementation, 
        # you'd use a proper gaussian blur algorithm
        pass
    
    @staticmethod
    def draw_gradient(
        surface: pygame.Surface,
        rect: pygame.Rect,
        color1: pygame.Color,
        color2: pygame.Color,
        direction: str = "vertical"
    ) -> None:
        """Draw a smooth gradient"""
        if direction == "vertical":
            for y in range(rect.height):
                ratio = y / rect.height
                r = int(color1.r * (1 - ratio) + color2.r * ratio)
                g = int(color1.g * (1 - ratio) + color2.g * ratio)
                b = int(color1.b * (1 - ratio) + color2.b * ratio)
                a = int(color1.a * (1 - ratio) + color2.a * ratio)
                
                line_color = pygame.Color(r, g, b, a)
                pygame.draw.line(
                    surface, 
                    line_color, 
                    (rect.x, rect.y + y), 
                    (rect.x + rect.width, rect.y + y)
                )
        else:  # horizontal
            for x in range(rect.width):
                ratio = x / rect.width
                r = int(color1.r * (1 - ratio) + color2.r * ratio)
                g = int(color1.g * (1 - ratio) + color2.g * ratio)
                b = int(color1.b * (1 - ratio) + color2.b * ratio)
                a = int(color1.a * (1 - ratio) + color2.a * ratio)
                
                line_color = pygame.Color(r, g, b, a)
                pygame.draw.line(
                    surface, 
                    line_color, 
                    (rect.x + x, rect.y), 
                    (rect.x + x, rect.y + rect.height)
                )
    
    @staticmethod
    def get_color_with_alpha(color: Union[pygame.Color, str, Tuple], alpha: int) -> pygame.Color:
        """Get a color with specified alpha"""
        if isinstance(color, str):
            base_color = pygame.Color(color)
        elif isinstance(color, tuple):
            base_color = pygame.Color(*color)
        else:
            base_color = color
        
        return pygame.Color(base_color.r, base_color.g, base_color.b, alpha)
    
    @staticmethod
    def lighten_color(color: pygame.Color, factor: float = 0.1) -> pygame.Color:
        """Lighten a color by a factor (0.0 to 1.0)"""
        r = min(255, int(color.r + (255 - color.r) * factor))
        g = min(255, int(color.g + (255 - color.g) * factor))
        b = min(255, int(color.b + (255 - color.b) * factor))
        return pygame.Color(r, g, b, color.a)
    
    @staticmethod
    def darken_color(color: pygame.Color, factor: float = 0.1) -> pygame.Color:
        """Darken a color by a factor (0.0 to 1.0)"""
        r = max(0, int(color.r * (1 - factor)))
        g = max(0, int(color.g * (1 - factor)))
        b = max(0, int(color.b * (1 - factor)))
        return pygame.Color(r, g, b, color.a)