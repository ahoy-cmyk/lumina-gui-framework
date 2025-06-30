from typing import Optional, List, Dict, Any, Callable, Union
import pygame
import time
from lumina.core.widget import Widget
from lumina.core.types import Rect, Padding
from lumina.core.graphics import ModernGraphics


class DataTable(Widget):
    """Modern data table with sorting, pagination, and selection"""
    
    def __init__(
        self,
        columns: List[Dict[str, Any]],
        data: List[Dict[str, Any]],
        selectable: bool = True,
        sortable: bool = True,
        paginated: bool = True,
        rows_per_page: int = 10,
        on_row_click: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_selection_change: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
        **kwargs
    ):
        if "padding" not in kwargs:
            kwargs["padding"] = Padding.all(16)
        
        super().__init__(**kwargs)
        
        self.columns = columns  # [{"key": "name", "title": "Name", "width": 150, "sortable": True}]
        self.data = data
        self.selectable = selectable
        self.sortable = sortable
        self.paginated = paginated
        self.rows_per_page = rows_per_page
        self.on_row_click = on_row_click
        self.on_selection_change = on_selection_change
        
        # Table state
        self.sort_column = None
        self.sort_direction = "asc"  # "asc" or "desc"
        self.current_page = 0
        self.selected_rows = set()
        self.hovered_row = -1
        
        # Animation state
        self._hover_animation = {}
        self._last_update = time.time()
        
        # Calculate row height
        self.row_height = 48
        self.header_height = 56
        
        # Apply styling
        self.style.border_radius = 8
    
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        """Calculate table size"""
        # Calculate total width from columns
        total_width = sum(col.get("width", 150) for col in self.columns)
        total_width += self.padding.left + self.padding.right
        
        # Calculate height based on visible rows
        visible_rows = min(len(self.get_current_page_data()), self.rows_per_page)
        total_height = (self.header_height + 
                       visible_rows * self.row_height + 
                       self.padding.top + self.padding.bottom)
        
        # Add pagination height if enabled
        if self.paginated and len(self.data) > self.rows_per_page:
            total_height += 60
        
        return min(total_width, available_width), min(total_height, available_height)
    
    def get_current_page_data(self) -> List[Dict[str, Any]]:
        """Get data for current page"""
        if not self.paginated:
            return self.data
        
        start_idx = self.current_page * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        return self.data[start_idx:end_idx]
    
    def get_total_pages(self) -> int:
        """Get total number of pages"""
        if not self.paginated:
            return 1
        return (len(self.data) + self.rows_per_page - 1) // self.rows_per_page
    
    def sort_data(self, column_key: str) -> None:
        """Sort data by column"""
        if not self.sortable:
            return
        
        # Toggle sort direction if same column
        if self.sort_column == column_key:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column_key
            self.sort_direction = "asc"
        
        # Sort data
        reverse = self.sort_direction == "desc"
        self.data.sort(key=lambda row: row.get(column_key, ""), reverse=reverse)
        
        # Reset to first page
        self.current_page = 0
        self.invalidate()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle table events"""
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            old_hovered = self.hovered_row
            self.hovered_row = self._get_row_at_position(event.pos)
            if old_hovered != self.hovered_row:
                self.invalidate()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check header clicks (for sorting)
            header_rect = self._get_header_rect()
            if header_rect.collidepoint(event.pos):
                column_index = self._get_column_at_position(event.pos[0])
                if column_index >= 0 and column_index < len(self.columns):
                    column = self.columns[column_index]
                    if column.get("sortable", True):
                        self.sort_data(column["key"])
                        return True
            
            # Check row clicks
            row_index = self._get_row_at_position(event.pos)
            if row_index >= 0:
                current_data = self.get_current_page_data()
                if row_index < len(current_data):
                    row_data = current_data[row_index]
                    
                    # Handle selection
                    if self.selectable:
                        if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                            # Multi-select with Ctrl
                            if id(row_data) in self.selected_rows:
                                self.selected_rows.remove(id(row_data))
                            else:
                                self.selected_rows.add(id(row_data))
                        else:
                            # Single select
                            self.selected_rows = {id(row_data)}
                        
                        if self.on_selection_change:
                            selected_data = [row for row in self.data if id(row) in self.selected_rows]
                            self.on_selection_change(selected_data)
                    
                    # Row click callback
                    if self.on_row_click:
                        self.on_row_click(row_data)
                    
                    self.invalidate()
                    return True
            
            # Check pagination clicks
            if self.paginated and len(self.data) > self.rows_per_page:
                pagination_rect = self._get_pagination_rect()
                if pagination_rect.collidepoint(event.pos):
                    return self._handle_pagination_click(event.pos)
        
        return False
    
    def _get_row_at_position(self, pos: tuple[int, int]) -> int:
        """Get row index at screen position"""
        table_rect = self._get_table_content_rect()
        if not table_rect.collidepoint(pos):
            return -1
        
        y_offset = pos[1] - table_rect.y - self.header_height
        if y_offset < 0:
            return -1
        
        row_index = int(y_offset // self.row_height)
        return row_index if row_index < len(self.get_current_page_data()) else -1
    
    def _get_column_at_position(self, x: int) -> int:
        """Get column index at x position"""
        table_rect = self._get_table_content_rect()
        x_offset = x - table_rect.x
        
        current_x = 0
        for i, column in enumerate(self.columns):
            column_width = column.get("width", 150)
            if current_x <= x_offset < current_x + column_width:
                return i
            current_x += column_width
        
        return -1
    
    def _get_header_rect(self) -> pygame.Rect:
        """Get header rectangle"""
        table_rect = self._get_table_content_rect()
        return pygame.Rect(table_rect.x, table_rect.y, table_rect.width, self.header_height)
    
    def _get_table_content_rect(self) -> pygame.Rect:
        """Get table content rectangle"""
        return pygame.Rect(
            self.rect.x + self.padding.left,
            self.rect.y + self.padding.top,
            self.rect.width - self.padding.left - self.padding.right,
            self.rect.height - self.padding.top - self.padding.bottom
        )
    
    def _get_pagination_rect(self) -> pygame.Rect:
        """Get pagination area rectangle"""
        table_rect = self._get_table_content_rect()
        return pygame.Rect(
            table_rect.x,
            table_rect.bottom - 60,
            table_rect.width,
            60
        )
    
    def _handle_pagination_click(self, pos: tuple[int, int]) -> bool:
        """Handle pagination button clicks"""
        pagination_rect = self._get_pagination_rect()
        
        # Previous button
        prev_rect = pygame.Rect(pagination_rect.x, pagination_rect.y + 15, 80, 30)
        if prev_rect.collidepoint(pos) and self.current_page > 0:
            self.current_page -= 1
            self.invalidate()
            return True
        
        # Next button
        next_rect = pygame.Rect(pagination_rect.x + 100, pagination_rect.y + 15, 80, 30)
        if (next_rect.collidepoint(pos) and 
            self.current_page < self.get_total_pages() - 1):
            self.current_page += 1
            self.invalidate()
            return True
        
        return False
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the data table"""
        if not self.visible:
            return
        
        # Get theme
        theme = self.window.theme if self.window else None
        if not theme:
            return
        
        # Draw table background
        table_rect = self._get_table_content_rect()
        bg_color = pygame.Color(theme.surface_color)
        
        ModernGraphics.draw_rounded_rect(
            surface,
            bg_color,
            table_rect,
            self.style.border_radius
        )
        
        # Draw table border
        border_color = pygame.Color(theme.border_color)
        ModernGraphics.draw_rounded_rect(
            surface,
            border_color,
            table_rect,
            self.style.border_radius,
            width=1
        )
        
        # Draw header
        self._draw_header(surface, theme)
        
        # Draw rows
        self._draw_rows(surface, theme)
        
        # Draw pagination
        if self.paginated and len(self.data) > self.rows_per_page:
            self._draw_pagination(surface, theme)
    
    def _draw_header(self, surface: pygame.Surface, theme) -> None:
        """Draw table header"""
        header_rect = self._get_header_rect()
        
        # Header background
        header_bg = ModernGraphics.lighten_color(pygame.Color(theme.surface_color), 0.05)
        ModernGraphics.draw_rounded_rect(
            surface,
            header_bg,
            header_rect,
            self.style.border_radius
        )
        
        # Draw header bottom border
        pygame.draw.line(
            surface,
            pygame.Color(theme.border_color),
            (header_rect.x, header_rect.bottom - 1),
            (header_rect.right, header_rect.bottom - 1),
            1
        )
        
        # Draw column headers
        x_offset = header_rect.x
        font = self.style.get_font()
        font.set_bold(True)
        
        for column in self.columns:
            column_width = column.get("width", 150)
            column_rect = pygame.Rect(x_offset, header_rect.y, column_width, header_rect.height)
            
            # Draw column separator
            if x_offset > header_rect.x:
                pygame.draw.line(
                    surface,
                    pygame.Color(theme.border_color),
                    (x_offset, header_rect.y + 8),
                    (x_offset, header_rect.bottom - 8),
                    1
                )
            
            # Draw column title
            title_color = pygame.Color(theme.text_primary)
            title_surface = font.render(column["title"], True, title_color)
            
            title_x = column_rect.x + 12
            title_y = column_rect.y + (column_rect.height - title_surface.get_height()) // 2
            surface.blit(title_surface, (title_x, title_y))
            
            # Draw sort indicator
            if self.sortable and column.get("sortable", True) and self.sort_column == column["key"]:
                arrow_x = column_rect.right - 20
                arrow_y = column_rect.y + column_rect.height // 2
                
                if self.sort_direction == "asc":
                    # Up arrow
                    points = [(arrow_x, arrow_y + 3), (arrow_x + 6, arrow_y - 3), (arrow_x + 12, arrow_y + 3)]
                else:
                    # Down arrow
                    points = [(arrow_x, arrow_y - 3), (arrow_x + 6, arrow_y + 3), (arrow_x + 12, arrow_y - 3)]
                
                pygame.draw.polygon(surface, title_color, points)
            
            x_offset += column_width
    
    def _draw_rows(self, surface: pygame.Surface, theme) -> None:
        """Draw table rows"""
        table_rect = self._get_table_content_rect()
        current_data = self.get_current_page_data()
        
        y_offset = table_rect.y + self.header_height
        font = self.style.get_font()
        
        for row_index, row_data in enumerate(current_data):
            row_rect = pygame.Rect(table_rect.x, y_offset, table_rect.width, self.row_height)
            
            # Draw row background
            if id(row_data) in self.selected_rows:
                row_bg = ModernGraphics.get_color_with_alpha(theme.primary_color, 30)
            elif row_index == self.hovered_row:
                row_bg = ModernGraphics.get_color_with_alpha(theme.text_secondary, 10)
            elif row_index % 2 == 1:
                row_bg = ModernGraphics.get_color_with_alpha(theme.text_secondary, 5)
            else:
                row_bg = None
            
            if row_bg:
                pygame.draw.rect(surface, row_bg, row_rect)
            
            # Draw row border
            if row_index < len(current_data) - 1:
                pygame.draw.line(
                    surface,
                    pygame.Color(theme.border_color),
                    (row_rect.x, row_rect.bottom),
                    (row_rect.right, row_rect.bottom),
                    1
                )
            
            # Draw cell content
            x_offset = row_rect.x
            for column in self.columns:
                column_width = column.get("width", 150)
                cell_rect = pygame.Rect(x_offset, row_rect.y, column_width, row_rect.height)
                
                # Draw column separator
                if x_offset > row_rect.x:
                    pygame.draw.line(
                        surface,
                        pygame.Color(theme.border_color),
                        (x_offset, row_rect.y),
                        (x_offset, row_rect.bottom),
                        1
                    )
                
                # Draw cell text
                cell_value = str(row_data.get(column["key"], ""))
                if cell_value:
                    text_color = pygame.Color(theme.text_primary)
                    text_surface = font.render(cell_value, True, text_color)
                    
                    # Clip text to cell
                    clipped_surface = text_surface.subsurface(
                        (0, 0, min(text_surface.get_width(), column_width - 24), text_surface.get_height())
                    ) if text_surface.get_width() > column_width - 24 else text_surface
                    
                    text_x = cell_rect.x + 12
                    text_y = cell_rect.y + (cell_rect.height - text_surface.get_height()) // 2
                    surface.blit(clipped_surface, (text_x, text_y))
                
                x_offset += column_width
            
            y_offset += self.row_height
    
    def _draw_pagination(self, surface: pygame.Surface, theme) -> None:
        """Draw pagination controls"""
        pagination_rect = self._get_pagination_rect()
        
        # Pagination background
        pagination_bg = ModernGraphics.lighten_color(pygame.Color(theme.surface_color), 0.02)
        pygame.draw.rect(surface, pagination_bg, pagination_rect)
        
        # Draw top border
        pygame.draw.line(
            surface,
            pygame.Color(theme.border_color),
            (pagination_rect.x, pagination_rect.y),
            (pagination_rect.right, pagination_rect.y),
            1
        )
        
        # Draw pagination info
        font = self.style.get_font()
        total_pages = self.get_total_pages()
        page_info = f"Page {self.current_page + 1} of {total_pages}"
        
        info_color = pygame.Color(theme.text_secondary)
        info_surface = font.render(page_info, True, info_color)
        
        info_x = pagination_rect.right - info_surface.get_width() - 12
        info_y = pagination_rect.y + (pagination_rect.height - info_surface.get_height()) // 2
        surface.blit(info_surface, (info_x, info_y))
        
        # Draw navigation buttons
        button_y = pagination_rect.y + 15
        
        # Previous button
        prev_enabled = self.current_page > 0
        prev_color = pygame.Color(theme.primary_color) if prev_enabled else pygame.Color(theme.text_disabled)
        prev_rect = pygame.Rect(pagination_rect.x + 12, button_y, 80, 30)
        
        ModernGraphics.draw_rounded_rect(
            surface,
            ModernGraphics.get_color_with_alpha(prev_color, 20),
            prev_rect,
            6
        )
        
        prev_text = font.render("Previous", True, prev_color)
        prev_text_x = prev_rect.x + (prev_rect.width - prev_text.get_width()) // 2
        prev_text_y = prev_rect.y + (prev_rect.height - prev_text.get_height()) // 2
        surface.blit(prev_text, (prev_text_x, prev_text_y))
        
        # Next button
        next_enabled = self.current_page < total_pages - 1
        next_color = pygame.Color(theme.primary_color) if next_enabled else pygame.Color(theme.text_disabled)
        next_rect = pygame.Rect(pagination_rect.x + 100, button_y, 80, 30)
        
        ModernGraphics.draw_rounded_rect(
            surface,
            ModernGraphics.get_color_with_alpha(next_color, 20),
            next_rect,
            6
        )
        
        next_text = font.render("Next", True, next_color)
        next_text_x = next_rect.x + (next_rect.width - next_text.get_width()) // 2
        next_text_y = next_rect.y + (next_rect.height - next_text.get_height()) // 2
        surface.blit(next_text, (next_text_x, next_text_y))