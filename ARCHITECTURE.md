# Lumina Framework Architecture

## Overview

Lumina is built with a modular, component-based architecture that emphasizes simplicity, performance, and extensibility.

## Core Architecture

### 1. Widget System (`lumina.core.widget`)

All UI elements inherit from the base `Widget` class, which provides:

- **Lifecycle Management**: Mount/unmount events
- **Event Handling**: Mouse, keyboard, and custom events
- **Layout System**: Size calculation and positioning
- **Rendering**: Surface-based drawing with pygame
- **State Management**: Reactive updates and invalidation

### 2. Layout System (`lumina.layouts`)

Flexible layout managers including:

- **Container**: Basic container with vertical stacking
- **Row**: Horizontal layout with spacing and alignment
- **Column**: Vertical layout with spacing and alignment  
- **Stack**: Overlapping widgets (for layered UIs)

Each layout manager implements:
- `calculate_size()`: Determine preferred dimensions
- `layout()`: Position child widgets
- Responsive behavior and constraints

### 3. Theme System (`lumina.themes`)

Comprehensive theming with:

- **Material Design 3** inspired color palettes
- **Dynamic color generation** from brand colors
- **Built-in themes**: Light, dark, GitHub, Material variants
- **CSS-like styling** with the `Style` class
- **Automatic OS theme detection**

### 4. Event System (`lumina.core.reactive`)

Modern reactive programming with:

- **State containers**: Reactive state with observers
- **Computed values**: Derived state that updates automatically  
- **Async support**: Native async/await throughout
- **Event bubbling**: Standard DOM-like event propagation

### 5. Rendering Engine

Built on pygame for:

- **Hardware acceleration** where available
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **High DPI support** with automatic scaling
- **Efficient dirty region updates**

## Design Principles

### 1. Declarative UI

```python
window = Window(
    children=[
        Column([
            Header("Welcome"),
            Button("Click Me", on_click=handler),
        ])
    ]
)
```

### 2. Reactive State Management

```python
count = State(0)

def increment():
    count.value += 1

button = Button("Count: 0", on_click=increment)
count.subscribe(lambda: button.text = f"Count: {count.value}")
```

### 3. Type Safety

Full type hints throughout for excellent IDE support:

```python
def create_button(text: str, handler: Callable[[], None]) -> Button:
    return Button(text, on_click=handler)
```

### 4. Performance Optimizations

- **Dirty checking**: Only redraw when needed
- **Layout caching**: Avoid unnecessary calculations
- **Event batching**: Efficient update cycles
- **Memory management**: Proper widget cleanup

## Extension Points

### Custom Widgets

```python
class MyWidget(Widget):
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        # Calculate preferred size
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        # Render widget content
        pass
```

### Custom Themes

```python
my_theme = Theme(
    primary_color="#FF6B6B",
    background_color="#FFFFFF",
    # ... other properties
)
```

### Custom Layout Managers

```python
class GridLayout(Container):
    def layout(self, rect: Rect) -> None:
        # Implement grid positioning logic
        pass
```

## Future Architecture Considerations

### 1. Plugin System
- Component marketplace
- Third-party widget libraries
- Theme packs

### 2. Web Export
- WebAssembly compilation
- Progressive Web App support
- Shared codebase for desktop/web

### 3. Native Integration
- System notifications
- File system access
- OS-specific features

### 4. Performance Enhancements
- GPU compute shaders
- Multi-threaded rendering
- Advanced caching strategies

## Comparison to Other Frameworks

| Feature | Lumina | Tkinter | PyQt | Kivy |
|---------|--------|---------|------|------|
| Learning Curve | Easy | Easy | Hard | Medium |
| Modern Look | ✅ | ❌ | ✅ | ✅ |
| Type Safety | ✅ | ❌ | Partial | ❌ |
| Async Support | ✅ | ❌ | ✅ | Partial |
| Bundle Size | Small | Tiny | Large | Large |
| Mobile Support | Future | ❌ | ❌ | ✅ |

## Getting Started

See the `examples/` directory for complete applications demonstrating the framework's capabilities.