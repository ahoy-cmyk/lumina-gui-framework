"""
Advanced text rendering with emoji support and better typography
"""
import pygame
import sys
import re
from typing import Optional, Tuple, List
from lumina.core.style import Style


class TextRenderer:
    """Advanced text renderer with emoji and typography support"""
    
    _emoji_font_cache = {}
    _system_font_cache = {}
    
    @classmethod
    def render_text(cls, text: str, style: Style, color: pygame.Color) -> pygame.Surface:
        """Render text with emoji support and better typography"""
        if not text:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Replace emojis with Unicode symbols that work well in pygame
        from lumina.core.emoji_handler import replace_emojis_with_symbols
        processed_text = replace_emojis_with_symbols(text)
        
        # Render the processed text
        return cls._render_simple_text(processed_text, style, color)
    
    @classmethod
    def _contains_emoji(cls, text: str) -> bool:
        """Check if text contains emoji characters"""
        # Unicode ranges for emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U00002600-\U000027BF"  # miscellaneous symbols
            "\U0000FE00-\U0000FE0F"  # variation selectors
            "]+", 
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(text))
    
    @classmethod
    def _render_simple_text(cls, text: str, style: Style, color: pygame.Color) -> pygame.Surface:
        """Render text without emojis using system font"""
        font = style.get_font()
        
        # Use anti-aliased rendering for quality
        surface = font.render(text, True, color)
        
        # Convert to optimal pixel format to prevent rendering issues
        return surface.convert_alpha()
    
    @classmethod
    def _render_text_with_emojis(cls, text: str, style: Style, color: pygame.Color) -> pygame.Surface:
        """Render text with emoji support"""
        # Always split text into emoji and non-emoji parts for better control
        parts = cls._split_text_and_emojis(text)
        
        if len(parts) == 1 and not parts[0][1]:
            # No emojis found, render normally
            return cls._render_simple_text(text, style, color)
        
        # Render each part separately and combine
        return cls._combine_text_parts(parts, style, color)
    
    @classmethod
    def _get_emoji_font(cls, size: float) -> Optional[pygame.font.Font]:
        """Get an emoji-capable font"""
        size_key = int(size)
        if size_key in cls._emoji_font_cache:
            return cls._emoji_font_cache[size_key]
        
        # Try different emoji fonts based on platform
        emoji_fonts = []
        
        if sys.platform == "darwin":  # macOS
            emoji_fonts = [
                "applecoloremoji",     # Actual font name found in pygame
                "Apple Color Emoji",
                "Apple Emoji",
                ".AppleColorEmojiUI",
            ]
        elif sys.platform == "win32":  # Windows
            emoji_fonts = [
                "Segoe UI Emoji",
                "Segoe UI Symbol",
                "Microsoft Sans Serif",
            ]
        else:  # Linux
            emoji_fonts = [
                "Noto Color Emoji",
                "Noto Emoji",
                "DejaVu Sans",
            ]
        
        # Try to load emoji font
        for font_name in emoji_fonts:
            try:
                font = pygame.font.SysFont(font_name, size_key)
                if font:
                    cls._emoji_font_cache[size_key] = font
                    return font
            except:
                continue
        
        # No emoji font found
        cls._emoji_font_cache[size_key] = None
        return None
    
    @classmethod
    def _split_text_and_emojis(cls, text: str) -> List[Tuple[str, bool]]:
        """Split text into parts marking which are emojis"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF" 
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U0001F900-\U0001F9FF"
            "\U00002600-\U000027BF"
            "\U0000FE00-\U0000FE0F"
            "]+",
            flags=re.UNICODE
        )
        
        parts = []
        last_end = 0
        
        for match in emoji_pattern.finditer(text):
            # Add text before emoji
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            
            # Add emoji
            parts.append((match.group(), True))
            last_end = match.end()
        
        # Add remaining text
        if last_end < len(text):
            parts.append((text[last_end:], False))
        
        return parts
    
    @classmethod
    def _combine_text_parts(cls, parts: List[Tuple[str, bool]], style: Style, color: pygame.Color) -> pygame.Surface:
        """Combine text and emoji parts into a single surface"""
        if not parts:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Get fonts
        text_font = style.get_font()
        emoji_font = cls._get_emoji_font(style.font_size)
        
        # Calculate total size needed
        total_width = 0
        max_height = 0
        
        rendered_parts = []
        
        for part_text, is_emoji in parts:
            if not part_text:
                continue
            
            if is_emoji and emoji_font:
                # Try to render with emoji font using a larger size for visibility
                try:
                    # Use a larger emoji font for better visibility
                    large_emoji_font = cls._get_emoji_font(style.font_size * 1.2)
                    if large_emoji_font:
                        surface = large_emoji_font.render(part_text, True, color)
                        # If that fails or is too small, try fallback
                        if surface.get_width() < 5:
                            raise Exception("Emoji too small")
                    else:
                        raise Exception("No large emoji font")
                except:
                    # Fallback: render emoji as text with regular font
                    surface = text_font.render(part_text, True, color)
                    # If still too small, use placeholder
                    if surface.get_width() < 5:
                        surface = text_font.render("🙂", True, color)  # Fallback emoji
            else:
                # Render with text font
                surface = text_font.render(part_text, True, color)
            
            rendered_parts.append(surface)
            total_width += surface.get_width()
            max_height = max(max_height, surface.get_height())
        
        if not rendered_parts:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Create combined surface
        combined = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
        combined.fill((0, 0, 0, 0))  # Transparent background
        
        # Blit all parts
        x_offset = 0
        for surface in rendered_parts:
            # Center vertically
            y_offset = (max_height - surface.get_height()) // 2
            combined.blit(surface, (x_offset, y_offset))
            x_offset += surface.get_width()
        
        # Convert to optimal format
        return combined.convert_alpha()
    
    @classmethod
    def get_text_size(cls, text: str, style: Style) -> Tuple[int, int]:
        """Get the size of rendered text"""
        if not text:
            return (0, 0)
        
        # Process emojis first
        from lumina.core.emoji_handler import replace_emojis_with_symbols
        processed_text = replace_emojis_with_symbols(text)
        
        # Use font metrics for size calculation
        font = style.get_font()
        return font.size(processed_text)