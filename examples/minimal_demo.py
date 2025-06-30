#!/usr/bin/env python3
"""
Minimal Demo - Just basic widgets without scrolling
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lumina.core.app import App
from lumina.core.window import Window
from lumina.widgets import Text, Button, Container
from lumina.themes import themes
from lumina.core.style import Style
from lumina.core.types import Padding

def main():
    """Run minimal demo"""
    print("Starting minimal demo...")
    
    # Need to define window first for closure
    window = None
    
    def on_button_click():
        print("Button clicked!")
    
    def on_theme_click():
        print("Theme button clicked!")
        # Toggle theme
        current = window.theme
        if current == themes.default_light:
            window.set_theme(themes.default_dark)
            print("Switched to dark theme")
        else:
            window.set_theme(themes.default_light)
            print("Switched to light theme")
    
    # Simple content without scrolling
    content = Container([
        Text("🚀 Lumina Minimal Demo", style=Style(font_size=24, font_weight="bold")),
        Text("Text with emoji support: ★ ♥ ✓ ☺"),
        Button("Click Me!", on_click=on_button_click),
        Button("Toggle Theme 🎨", on_click=on_theme_click),
        Text("Window should stay open until you close it."),
    ], padding=Padding.all(30))
    
    window = Window(
        title="Lumina - Minimal Demo", 
        width=700,
        height=500,
        theme=themes.default_light,
        children=[content]
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