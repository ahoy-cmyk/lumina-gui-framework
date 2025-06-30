#!/usr/bin/env python3
"""
Simple Working Demo - Shows basic functionality with all fixes applied
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

def main():
    """Run the simple demo"""
    print("Running Lumina simple working demo...")
    
    # Need to define window first for closure
    window = None
    
    # Create scrollable content
    content_items = []
    for i in range(10):
        content_items.append(
            Text(f"Item {i+1}: High-quality text ★ with emoji symbols ♥ and perfect rendering ✓")
        )
    
    def toggle_theme():
        """Toggle between themes"""
        current = window.theme
        if current == themes.default_light:
            window.set_theme(themes.default_dark)
            print("Switched to dark theme")
        else:
            window.set_theme(themes.default_light)
            print("Switched to light theme")
    
    # Main content
    main_content = Container([
        Text("🚀 Lumina Framework - Working Demo", style=Style(font_size=24, font_weight="bold")),
        Text("All fixes applied: crisp text, emoji ★, scrollbars, theme switching ✓"),
        Button("Toggle Theme 🎨", on_click=toggle_theme),
        Text("Scrollable Content (use mouse wheel):"),
        ScrollableContainer(
            content_items,
            scroll_vertical=True
        ),
        Text("✨ Everything working perfectly! ✨"),
    ], padding=Padding.all(20))
    
    # Create window
    window = Window(
        title="Lumina - Simple Working Demo",
        width=800,
        height=600,
        theme=themes.default_light,
        children=[main_content]
    )
    
    app = App(debug=True)
    try:
        print("Window created successfully. Starting event loop...")
        app.run(window)
    except KeyboardInterrupt:
        print("Demo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()