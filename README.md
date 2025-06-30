# 🚀 Lumina GUI Framework

**A modern Python GUI framework that strives to be simple to use, beautiful to behold, and completely standards-compliant.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **🎨 Beautiful Modern Design** - Material Design 3 theming with 6 built-in themes
- **📱 High DPI Support** - Perfect rendering on macOS Retina and high DPI displays  
- **😀 Emoji Support** - Unicode emoji rendering via symbol replacements
- **📜 Functional Scrollbars** - Mouse wheel + drag support with modern styling
- **🎭 Dynamic Theme Switching** - Instant theme changes without window recreation
- **🔤 High-Quality Text** - Anti-aliased text with crisp font rendering
- **⚡ Reactive State** - Modern reactive programming patterns
- **🧩 Component-Based** - Modular widget architecture

## 🏃 Quick Start

### Installation

```bash
git clone https://github.com/your-username/lumina-gui-framework.git
cd lumina-gui-framework
pip install -r requirements.txt
```

### Hello World

```python
from lumina.core.app import App
from lumina.core.window import Window
from lumina.widgets import Text, Button, Container
from lumina.themes import themes
from lumina.core.style import Style
from lumina.core.types import Padding

def main():
    window = None
    
    def on_click():
        print("Hello, Lumina! ✨")
    
    content = Container([
        Text("🚀 Hello Lumina!", style=Style(font_size=24, font_weight="bold")),
        Text("A beautiful Python GUI framework"),
        Button("Click Me!", on_click=on_click),
    ], padding=Padding.all(20))
    
    window = Window(
        title="Hello Lumina",
        width=600,
        height=400,
        theme=themes.default_light,
        children=[content]
    )
    
    app = App()
    app.run(window)

if __name__ == "__main__":
    main()
```

## 🎯 Demo Applications

Run the included demos to see all features in action:

```bash
# Simple demo with basic functionality
python examples/simple_working_demo.py

# Comprehensive demo showcasing all features  
python examples/complete_demo.py

# Minimal demo for testing
python examples/minimal_demo.py
```

## 🏗️ Architecture

### Core Components

- **`App`** - Main application container
- **`Window`** - Top-level window with theme support
- **`Widget`** - Base class for all UI components
- **`Container`** - Layout container for organizing widgets
- **`ScrollableContainer`** - Scrollable content with modern scrollbars

### Available Widgets

- **`Text`** - Text display with emoji support
- **`Button`** - Modern button with animations and variants
- **`Container`** - Basic container for layouts
- **`Row`** - Horizontal layout container
- **`Column`** - Vertical layout container  
- **`ScrollableContainer`** - Scrollable content area

### Themes

6 built-in themes with Material Design 3 colors:

- `themes.default_light` / `themes.default_dark`
- `themes.material_light` / `themes.material_dark` 
- `themes.github_light` / `themes.github_dark`

## 🔧 Key Features Explained

### High-Quality Text Rendering

Lumina uses carefully selected fonts and proper anti-aliasing for crisp text:

```python
# macOS: SF Pro Text, Helvetica fallback
# Windows: Segoe UI, Calibri fallback  
# Linux: Ubuntu, Liberation Sans fallback

text = Text("Crystal clear text ✨", style=Style(font_size=16))
```

### Emoji Support

Emojis are rendered using Unicode symbols that work reliably in pygame:

```python
# 😀 → ☺, 🌟 → ★, ❤️ → ♥, ✅ → ✓
text = Text("Emoji support: 😀 🌟 ❤️ ✅")
```

### Functional Scrollbars

Modern scrollbars with full interaction support:

```python
content = [Text(f"Item {i}") for i in range(20)]
scrollable = ScrollableContainer(
    content,
    scroll_vertical=True,
    scroll_horizontal=False
)
```

### Dynamic Theme Switching

Change themes instantly without recreating windows:

```python
def toggle_theme():
    if window.theme == themes.default_light:
        window.set_theme(themes.default_dark)
    else:
        window.set_theme(themes.default_light)
```

## 🧪 Testing & Validation

Validate that all features work correctly:

```bash
# Test framework components
python validate_fixes.py

# Test demo creation  
python test_demos.py

# Test window lifecycle
python test_window_lifecycle.py
```

## 🖥️ Platform Support

- **macOS** - Full support with Retina display optimization
- **Windows** - Full support with high DPI scaling
- **Linux** - Full support with X11/Wayland

## 🛠️ Development

### Requirements

- Python 3.9+
- pygame 2.0+
- Modern operating system with GUI support

### Project Structure

```
lumina/
├── core/           # Core framework components
│   ├── app.py      # Main application class
│   ├── window.py   # Window management
│   ├── widget.py   # Base widget class
│   └── ...
├── widgets/        # UI widgets
│   ├── text.py     # Text rendering
│   ├── button.py   # Button widget
│   └── ...
├── themes/         # Theme definitions
└── examples/       # Demo applications
```

## 📚 API Reference

### Creating a Window

```python
window = Window(
    title="My App",
    width=800,
    height=600,
    theme=themes.default_light,
    resizable=True,
    children=[content]
)
```

### Widget Styling

```python
# Using Style objects
text = Text("Styled text", style=Style(
    font_size=20,
    font_weight="bold",
    foreground_color="#FF0000"
))

# Using containers with padding
container = Container(
    children=[...],
    padding=Padding.all(20)  # or Padding.symmetric(vertical=10, horizontal=20)
)
```

### Event Handling

```python
def on_button_click():
    print("Button clicked!")

button = Button("Click me", on_click=on_button_click)
```

### Layout Components

```python
# Vertical layout
Column([widget1, widget2, widget3], spacing=10)

# Horizontal layout
Row([widget1, widget2, widget3], spacing=10)

# Scrollable content
ScrollableContainer(
    children=[...],
    scroll_vertical=True,
    scroll_horizontal=False
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pygame](https://www.pygame.org/) for cross-platform graphics
- Inspired by Material Design 3 and modern UI frameworks
- Emoji mapping ensures reliable cross-platform rendering

---

**Made with ❤️ for the Python community**