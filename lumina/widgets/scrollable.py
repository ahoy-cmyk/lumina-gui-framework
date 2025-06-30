from typing import Optional, Union
import pygame
import time
from lumina.core.widget import Widget
from lumina.core.types import Rect, Padding, EventType
from lumina.core.graphics import ModernGraphics
from lumina.widgets.container import Container


class ScrollableContainer(Container):
    """Scrollable container with modern scrollbars"""
    
    def __init__(
        self,
        children: Optional[Union[Widget, list[Widget]]] = None,
        scroll_horizontal: bool = False,
        scroll_vertical: bool = True,
        scrollbar_width: int = 12,
        **kwargs
    ):
        super().__init__(children, **kwargs)
        
        self.scroll_horizontal = scroll_horizontal
        self.scroll_vertical = scroll_vertical
        self.scrollbar_width = scrollbar_width
        
        # Scroll state
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.content_width = 0.0
        self.content_height = 0.0
        self.viewport_width = 0.0
        self.viewport_height = 0.0
        
        # Scrollbar state
        self._v_scrollbar_rect = None
        self._v_thumb_rect = None
        self._h_scrollbar_rect = None
        self._h_thumb_rect = None
        self._dragging_v_scrollbar = False
        self._dragging_h_scrollbar = False
        self._drag_start_y = 0
        self._drag_start_x = 0
        self._drag_start_scroll = 0
        
        # Animation
        self._scrollbar_hover = 0.0
        self._last_update = time.time()
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate size including scrollbars"""
        # Calculate content size
        content_width, content_height = super().calculate_size(available_width, available_height)
        
        # Store content dimensions
        self.content_width = content_width
        self.content_height = content_height
        
        # Calculate viewport size (excluding scrollbars)
        self.viewport_width = available_width
        self.viewport_height = available_height
        
        if self.scroll_vertical and content_height > available_height:
            self.viewport_width -= self.scrollbar_width
        
        if self.scroll_horizontal and content_width > available_width:
            self.viewport_height -= self.scrollbar_width
        
        return available_width, available_height
    
    def layout(self, rect: Rect) -> None:
        """Layout with scrolling support"""
        super().layout(rect)
        
        # Update viewport dimensions
        self.viewport_width = self.rect.width
        self.viewport_height = self.rect.height
        
        # Calculate actual content size
        total_content_height = 0
        max_content_width = 0
        
        for child in self.children:
            child_width, child_height = child.calculate_size(self.viewport_width, float('inf'))
            max_content_width = max(max_content_width, child_width)
            total_content_height += child_height + 8  # Add spacing
        
        self.content_width = max_content_width
        self.content_height = total_content_height
        
        # Adjust for scrollbars
        if self.scroll_vertical and self.content_height > self.viewport_height:
            self.viewport_width -= self.scrollbar_width
        
        if self.scroll_horizontal and self.content_width > self.viewport_width:
            self.viewport_height -= self.scrollbar_width
        
        # Layout children with scroll offset
        y_offset = self.rect.y + self.padding.top - self.scroll_y
        
        for child in self.children:
            child_width, child_height = child.calculate_size(self.viewport_width, float('inf'))
            
            child_rect = Rect(
                self.rect.x + self.padding.left - self.scroll_x,
                y_offset,
                min(child_width, self.viewport_width - self.padding.left - self.padding.right),
                child_height
            )
            
            child.layout(child_rect)
            y_offset += child_height + 8
        
        # Update scrollbar positions
        self._update_scrollbar_rects()
    
    def _update_scrollbar_rects(self) -> None:
        """Update scrollbar and thumb rectangles"""
        # Vertical scrollbar
        if self.scroll_vertical and self.content_height > self.viewport_height:
            self._v_scrollbar_rect = pygame.Rect(
                self.rect.x + self.viewport_width,
                self.rect.y,
                self.scrollbar_width,
                self.viewport_height
            )
            
            # Calculate thumb size and position
            thumb_ratio = self.viewport_height / self.content_height
            thumb_height = max(20, self.viewport_height * thumb_ratio)
            
            scroll_ratio = self.scroll_y / (self.content_height - self.viewport_height)
            thumb_y = self.rect.y + scroll_ratio * (self.viewport_height - thumb_height)
            
            self._v_thumb_rect = pygame.Rect(
                self.rect.x + self.viewport_width + 2,
                thumb_y,
                self.scrollbar_width - 4,
                thumb_height
            )
        else:
            self._v_scrollbar_rect = None
            self._v_thumb_rect = None
        
        # Horizontal scrollbar (similar logic)
        if self.scroll_horizontal and self.content_width > self.viewport_width:
            self._h_scrollbar_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + self.viewport_height,
                self.viewport_width,
                self.scrollbar_width
            )
            
            thumb_ratio = self.viewport_width / self.content_width
            thumb_width = max(20, self.viewport_width * thumb_ratio)
            
            scroll_ratio = self.scroll_x / (self.content_width - self.viewport_width)
            thumb_x = self.rect.x + scroll_ratio * (self.viewport_width - thumb_width)
            
            self._h_thumb_rect = pygame.Rect(
                thumb_x,
                self.rect.y + self.viewport_height + 2,
                thumb_width,
                self.scrollbar_width - 4
            )
        else:
            self._h_scrollbar_rect = None
            self._h_thumb_rect = None
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle scrolling events"""
        # Mouse wheel scrolling
        if event.type == pygame.MOUSEWHEEL:
            if self.contains_point(*pygame.mouse.get_pos()):
                if self.scroll_vertical:
                    self.scroll_y -= event.y * 30  # Scroll speed
                    self.scroll_y = max(0, min(self.scroll_y, 
                                              max(0, self.content_height - self.viewport_height)))
                    self._update_scrollbar_rects()
                    self.invalidate()
                    return True
        
        # Scrollbar dragging
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check vertical scrollbar thumb
            if (self._v_thumb_rect and self._v_thumb_rect.collidepoint(event.pos)):
                self._dragging_v_scrollbar = True
                self._drag_start_y = event.pos[1]
                self._drag_start_scroll = self.scroll_y
                return True
            
            # Check horizontal scrollbar thumb
            elif (self._h_thumb_rect and self._h_thumb_rect.collidepoint(event.pos)):
                self._dragging_h_scrollbar = True
                self._drag_start_x = event.pos[0]
                self._drag_start_scroll = self.scroll_x
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging_v_scrollbar = False
            self._dragging_h_scrollbar = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self._dragging_v_scrollbar:
                # Calculate new scroll position
                delta_y = event.pos[1] - self._drag_start_y
                max_scroll = max(0, self.content_height - self.viewport_height)
                scroll_range = self.viewport_height - (self._v_thumb_rect.height if self._v_thumb_rect else 20)
                
                if scroll_range > 0:
                    scroll_delta = (delta_y / scroll_range) * max_scroll
                    self.scroll_y = max(0, min(max_scroll, self._drag_start_scroll + scroll_delta))
                    self.layout(self.rect)
                    self.invalidate()
                return True
            
            elif self._dragging_h_scrollbar:
                # Similar logic for horizontal scrolling
                delta_x = event.pos[0] - self._drag_start_x
                max_scroll = max(0, self.content_width - self.viewport_width)
                scroll_range = self.viewport_width - (self._h_thumb_rect.width if self._h_thumb_rect else 20)
                
                if scroll_range > 0:
                    scroll_delta = (delta_x / scroll_range) * max_scroll
                    self.scroll_x = max(0, min(max_scroll, self._drag_start_scroll + scroll_delta))
                    self.layout(self.rect)
                    self.invalidate()
                return True
        
        # Pass events to visible children
        for child in self.children:
            if child.visible and self._is_child_visible(child):
                if child.handle_event(event):
                    return True
        
        return False
    
    def _is_child_visible(self, child: Widget) -> bool:
        """Check if child is within the viewport"""
        viewport_rect = pygame.Rect(
            self.rect.x,
            self.rect.y, 
            self.viewport_width,
            self.viewport_height
        )
        
        child_rect = pygame.Rect(
            child.rect.x,
            child.rect.y,
            child.rect.width,
            child.rect.height
        )
        
        return viewport_rect.colliderect(child_rect)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render with clipping and scrollbars"""
        if not self.visible:
            return
        
        # Draw background
        if self.style.background_color:
            bg_color = self.style.to_pygame_color(self.style.background_color)
            if bg_color:
                pygame.draw.rect(surface, bg_color, self.rect.to_pygame_rect())
        
        # Create clipping rectangle for content
        viewport_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            int(self.viewport_width),
            int(self.viewport_height)
        )
        
        # Set clipping
        old_clip = surface.get_clip()
        surface.set_clip(viewport_rect)
        
        # Render visible children
        for child in self.children:
            if child.visible and self._is_child_visible(child):
                child.render(surface)
        
        # Restore clipping
        surface.set_clip(old_clip)
        
        # Draw scrollbars
        self._draw_scrollbars(surface)
    
    def _draw_scrollbars(self, surface: pygame.Surface) -> None:
        """Draw modern scrollbars"""
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Vertical scrollbar
        if self._v_scrollbar_rect and self._v_thumb_rect:
            # Scrollbar track
            track_color = ModernGraphics.get_color_with_alpha(theme.text_secondary, 20)
            ModernGraphics.draw_rounded_rect(
                surface,
                track_color,
                self._v_scrollbar_rect,
                self.scrollbar_width // 2
            )
            
            # Scrollbar thumb
            thumb_color = pygame.Color(theme.text_secondary)
            if self._dragging_v_scrollbar:
                thumb_color = pygame.Color(theme.primary_color)
            
            ModernGraphics.draw_rounded_rect(
                surface,
                thumb_color,
                self._v_thumb_rect,
                (self.scrollbar_width - 4) // 2
            )
        
        # Horizontal scrollbar (similar)
        if self._h_scrollbar_rect and self._h_thumb_rect:
            track_color = ModernGraphics.get_color_with_alpha(theme.text_secondary, 20)
            ModernGraphics.draw_rounded_rect(
                surface,
                track_color,
                self._h_scrollbar_rect,
                self.scrollbar_width // 2
            )
            
            thumb_color = pygame.Color(theme.text_secondary)
            if self._dragging_h_scrollbar:
                thumb_color = pygame.Color(theme.primary_color)
            
            ModernGraphics.draw_rounded_rect(
                surface,
                thumb_color,
                self._h_thumb_rect,
                (self.scrollbar_width - 4) // 2
            )