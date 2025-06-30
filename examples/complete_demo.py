#!/usr/bin/env python3
"""
Complete Lumina Framework Demo
Showcases all working features with fixes applied:
- High-quality text rendering
- Emoji support via Unicode symbols  
- Functional scrollbars
- Working theme switching
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lumina.core.app import App
from lumina.core.window import Window
from lumina.widgets import Text, Button, Container, ScrollableContainer
from lumina.themes import themes
from lumina.core.style import Style
from lumina.core.types import Padding

class CompleteDemo:
    def __init__(self):
        self.current_theme = themes.default_light
        self.window = None
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == themes.default_light:
            self.current_theme = themes.default_dark
        else:
            self.current_theme = themes.default_light
        
        # Apply theme to window
        if self.window:
            self.window.set_theme(self.current_theme)
    
    def create_header_section(self):
        """Create the main header with theme toggle"""
        return Container([
            Text("🚀 Lumina Framework Complete Demo", style=Style(font_size=28, font_weight="bold")),
            Text("Showcasing high-quality text, emoji support ★, scrollbars, and theme switching"),
            Button("Toggle Theme 🎨", on_click=self.toggle_theme),
        ], padding=Padding.all(20))
    
    def create_text_showcase(self):
        """Create text quality and emoji showcase"""
        return Container([
            Text("Text Quality & Emoji Demo", style=Style(font_size=20, font_weight="bold")),
            Text("High-quality text rendering with perfect kerning and crisp fonts ✨"),
            Text("Emoji Support: Happy ☺ Star ★ Love ♥ Arrow → Check ✓ Cross × Fire ▲"),
            Text("Unicode Symbols: ♪ ♫ ◆ ✦ ☀ ☽ ⚡ ◎ ↑ ↓ ← → ▲ ▼"),
            Text("This text demonstrates the improved font rendering quality with proper anti-aliasing."),
        ], padding=Padding.all(15))
    
    def create_scrollable_demo(self):
        """Create scrollable content demo"""
        scroll_content = []
        for i in range(20):
            scroll_content.append(
                Text(f"Scrollable Item {i+1} - This demonstrates scrolling with emoji ★ and symbols ♥")
            )
        
        return Container([
            Text("Scrollable Container Demo", style=Style(font_size=20, font_weight="bold")),
            Text("Scroll with mouse wheel or drag the scrollbar:"),
            ScrollableContainer(
                scroll_content,
                scroll_vertical=True,
                scroll_horizontal=False
            ),
        ], padding=Padding.all(15))
    
    def create_layout_demo(self):
        """Create layout demo"""
        return Container([
            Text("Layout System Demo", style=Style(font_size=20, font_weight="bold")),
            Text("Container layouts with proper spacing:"),
            Container([
                Text("Card 1 - Flexible layouts ★"),
                Text("Card 2 - Auto-sizing ◆"),  
                Text("Card 3 - Responsive ✓"),
            ], padding=Padding.all(10)),
            Text("Vertical stacking with proper spacing"),
            Text("Each element maintains proper margins ↓"),
            Text("Clean typography throughout ✨"),
        ], padding=Padding.all(15))
    
    def create_window(self):
        """Create the main window with all demos"""
        # Main content in a scrollable container
        main_content = ScrollableContainer([
            self.create_header_section(),
            self.create_text_showcase(),
            self.create_scrollable_demo(),
            self.create_layout_demo(),
            
            # Footer
            Container([
                Text("✨ All features working: Theme switching, high-quality text, emoji support, and functional scrollbars ✨"),
            ], padding=Padding.all(20)),
        ], scroll_vertical=True)
        
        self.window = Window(
            title="Lumina Framework - Complete Demo",
            width=1000,
            height=700,
            theme=self.current_theme,
            children=[main_content]
        )
        
        return self.window

def main():
    """Run the complete demo"""
    app = App()
    demo = CompleteDemo()
    window = demo.create_window()
    app.run(window)

if __name__ == "__main__":
    main()