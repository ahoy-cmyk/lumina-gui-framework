# 🌟 Lumina Framework - Comprehensive Guide

*A modern Python GUI framework that's simple to use, beautiful to behold, and completely standards-compliant.*

---

## 📖 Table of Contents

1. [Quick Start](#-quick-start)
2. [Installation](#-installation)
3. [Core Concepts](#-core-concepts)
4. [Components Guide](#-components-guide)
5. [Theming System](#-theming-system)
6. [Layout Management](#-layout-management)
7. [Event Handling](#-event-handling)
8. [Examples](#-examples)
9. [API Reference](#-api-reference)
10. [Best Practices](#-best-practices)

---

## 🚀 Quick Start

### Your First Lumina App

```python
from lumina import App, Window
from lumina.widgets import Text, Button, Column
from lumina.themes import themes

def say_hello():
    print("Hello from Lumina! 👋")

# Create app
app = App(name="My First Lumina App")

# Create window
window = Window(
    title="Welcome to Lumina",
    width=400,
    height=300,
    theme=themes.material_light,
    children=[
        Column(
            spacing=16,
            children=[
                Text("Welcome to Lumina!", style="heading"),
                Text("The modern Python GUI framework."),
                Button("Say Hello", on_click=say_hello, variant="primary"),
            ]
        )
    ]
)

# Run the app
app.run(window)
```

---

## 💾 Installation

### Prerequisites
- Python 3.10 or higher
- No additional system dependencies required!

### Install Lumina

```bash
# Clone the repository
git clone https://github.com/lumina-framework/lumina.git
cd lumina

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e .[dev]

# Run tests (when available)
pytest

# Format code
black lumina/
ruff lumina/
```

---

## 🧠 Core Concepts

### 1. **Declarative UI**

Lumina uses a declarative approach where you describe *what* your UI should look like, not *how* to create it.

```python
# Declarative - describe the structure
window = Window(
    children=[
        Column([
            Header("My App"),
            Row([
                Button("Save"),
                Button("Cancel"),
            ])
        ])
    ]
)
```

### 2. **Component Hierarchy**

Every UI element is a **Widget** that can contain child widgets:

```
Window
└── Column
    ├── Header (Text widget)
    └── Row
        ├── Button
        └── Button
```

### 3. **Reactive State**

Use `State` containers for reactive updates:

```python
from lumina.core.reactive import State

# Create reactive state
count = State(0)

# Create button that updates
button = Button(f"Count: {count.value}", on_click=lambda: count.value += 1)

# Subscribe to changes
count.subscribe(lambda: button.text = f"Count: {count.value}")
```

### 4. **Modern Styling**

Components are beautiful by default with built-in Material Design 3 styling:

```python
# Automatic modern styling
button = Button("Click Me", variant="primary")

# Custom styling
button = Button(
    "Custom Button",
    style=Style(
        background_color="#FF6B6B",
        border_radius=12,
        font_size=18
    )
)
```

---

## 🧩 Components Guide

### Text Components

#### `Text` - Basic text display
```python
Text("Hello World")
Text("Styled text", style="heading")  # Predefined styles
Text("Custom", color="#FF6B6B")       # Custom color
```

**Predefined Styles:**
- `"heading"` - Large, bold text (32px)
- `"subheading"` - Medium, semi-bold text (24px) 
- `"body"` - Regular text (16px)
- `"caption"` - Small, secondary text (14px)
- `"small"` - Tiny text (12px)

#### `Header` - Semantic headings
```python
Header("Main Title", level=1)    # H1 - 32px
Header("Subtitle", level=2)      # H2 - 28px
Header("Section", level=3)       # H3 - 24px
```

### Button Components

#### `Button` - Interactive buttons with animations

```python
# Basic buttons
Button("Click Me")
Button("Primary", variant="primary")      # Blue filled
Button("Secondary", variant="secondary")  # Blue outlined
Button("Success", variant="success")      # Green filled
Button("Danger", variant="danger")        # Red filled
Button("Text", variant="text")            # No background

# Button sizes
Button("Small", size="small")             # Compact
Button("Medium", size="medium")           # Default
Button("Large", size="large")             # Prominent

# With icons and interactions
Button("Save", icon="check", on_click=save_file)
Button("Disabled", disabled=True)
```

**Button Features:**
- ✅ Smooth hover animations
- ✅ Press feedback with scale
- ✅ Automatic focus management
- ✅ Icon support
- ✅ Multiple variants and sizes

### Form Components

#### `TextInput` - Modern text input with floating labels

```python
# Basic input
TextInput(placeholder="Enter text...")

# With floating label
TextInput(
    label="Email Address",
    placeholder="you@example.com",
    variant="outlined"  # outlined, filled, underlined
)

# Multiline input
TextInput(
    label="Message",
    multiline=True,
    on_change=lambda value: print(f"Text: {value}")
)

# Password input
TextInput(
    label="Password",
    password=True,
    on_submit=lambda value: login(value)
)
```

**Input Features:**
- ✅ Floating label animations
- ✅ Multiple visual variants
- ✅ Focus and hover states
- ✅ Real-time validation ready
- ✅ Keyboard navigation

### Layout Components

#### `Container` - Basic container
```python
Container(
    padding=Padding.all(16),
    children=[widget1, widget2]
)
```

#### `Row` - Horizontal layout
```python
Row(
    spacing=12,           # Space between children
    align="center",       # start, center, end, space-between
    children=[button1, button2, button3]
)
```

#### `Column` - Vertical layout
```python
Column(
    spacing=16,
    align="stretch",      # start, center, end, stretch
    children=[header, content, footer]
)
```

#### `Stack` - Overlapping layout
```python
Stack([
    background_image,     # Bottom layer
    overlay_content,      # Middle layer
    floating_button       # Top layer
])
```

### Card Components

#### `Card` - Elevated content containers

```python
# Basic card
Card(
    title="User Profile",
    children=[
        Text("John Doe"),
        Text("john@example.com"),
        Button("Edit Profile")
    ]
)

# Interactive cards
Card(
    title="Clickable Card",
    elevation=2,          # Shadow depth (1-5)
    hoverable=True,       # Hover animations
    clickable=True,       # Click interactions
    on_click=handle_click
)
```

**Card Features:**
- ✅ Beautiful drop shadows
- ✅ Hover elevation effects
- ✅ Click interactions
- ✅ Customizable elevation

### Modal Components

#### `Modal` - Dialog overlays

```python
# Create modal
modal = Modal(
    title="Confirmation",
    width=400,
    height=200,
    content=[
        Text("Are you sure you want to delete this item?"),
        Row([
            Button("Delete", variant="danger", on_click=confirm_delete),
            Button("Cancel", variant="secondary", on_click=close_modal)
        ])
    ],
    on_close=close_modal
)

# Show modal (add to window children)
window.add_child(modal)
```

**Modal Features:**
- ✅ Smooth fade-in animations
- ✅ Backdrop blur effect
- ✅ Click outside to close
- ✅ Escape key support
- ✅ Focus management

### Data Components

#### `DataTable` - Interactive data tables

```python
# Define columns
columns = [
    {"key": "id", "title": "ID", "width": 80, "sortable": True},
    {"key": "name", "title": "Name", "width": 200, "sortable": True},
    {"key": "email", "title": "Email", "width": 250, "sortable": True},
    {"key": "status", "title": "Status", "width": 100, "sortable": True},
]

# Sample data
data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "status": "Active"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "status": "Inactive"},
    # ... more rows
]

# Create table
table = DataTable(
    columns=columns,
    data=data,
    selectable=True,      # Row selection
    sortable=True,        # Column sorting
    paginated=True,       # Pagination
    rows_per_page=10,     # Page size
    on_row_click=lambda row: print(f"Clicked: {row['name']}"),
    on_selection_change=lambda rows: print(f"Selected: {len(rows)} rows")
)
```

**DataTable Features:**
- ✅ Column sorting with indicators
- ✅ Row selection (single/multi)
- ✅ Pagination controls
- ✅ Hover row highlighting
- ✅ Customizable column widths

---

## 🎨 Theming System

### Built-in Themes

Lumina comes with 6 beautiful themes:

```python
from lumina.themes import themes

# Light themes
themes.default_light      # Clean, professional light theme
themes.material_light     # Material Design 3 light
themes.github_light       # GitHub-inspired light theme

# Dark themes  
themes.default_dark       # Modern dark theme
themes.material_dark      # Material Design 3 dark
themes.github_dark        # GitHub-inspired dark theme
```

### Using Themes

```python
# Apply theme to window
window = Window(
    title="My App",
    theme=themes.material_dark,
    children=[...]
)

# Switch themes dynamically
def switch_to_dark():
    window.theme = themes.material_dark
    window.invalidate()  # Trigger redraw
```

### Custom Themes

```python
from lumina.themes import Theme

# Create custom theme
my_theme = Theme(
    primary_color="#FF6B6B",
    secondary_color="#4ECDC4", 
    background_color="#FFFFFF",
    surface_color="#F8F9FA",
    text_primary="#2C3E50",
    text_secondary="#7F8C8D",
    border_radius=12,
    font_family="SF Pro Display"
)

# Use custom theme
window = Window(theme=my_theme, children=[...])
```

### Theme Properties

| Property | Description | Example |
|----------|-------------|---------|
| `primary_color` | Main brand color | `"#0066CC"` |
| `secondary_color` | Secondary accent | `"#6C757D"` |
| `success_color` | Success states | `"#28A745"` |
| `warning_color` | Warning states | `"#FFC107"` |
| `error_color` | Error states | `"#DC3545"` |
| `background_color` | Main background | `"#FFFFFF"` |
| `surface_color` | Card/surface backgrounds | `"#F8F9FA"` |
| `text_primary` | Primary text color | `"#212529"` |
| `text_secondary` | Secondary text color | `"#6C757D"` |
| `border_color` | Border colors | `"#DEE2E6"` |
| `font_family` | Default font | `"system"` |
| `radius_base` | Border radius | `8` |
| `spacing_base` | Base spacing unit | `16` |

---

## 📐 Layout Management

### Spacing and Padding

```python
from lumina.core.types import Padding, Margin

# Uniform spacing
Padding.all(16)                    # 16px all sides
Margin.all(8)                      # 8px all sides

# Symmetric spacing
Padding.symmetric(vertical=12, horizontal=20)  # 12px top/bottom, 20px left/right

# Custom spacing
Padding(top=10, right=15, bottom=10, left=15)
```

### Responsive Layouts

```python
# Flexible row that adapts to screen size
Row(
    spacing=16,
    align="space-between",     # Distribute space evenly
    children=[
        Button("Left"),
        Button("Center"),  
        Button("Right")
    ]
)

# Column that stretches children
Column(
    align="stretch",           # Children fill width
    children=[
        TextInput("Full width input"),
        Button("Full width button")
    ]
)
```

### Layout Best Practices

1. **Use consistent spacing**: Stick to multiples of 4 or 8
2. **Prefer semantic layouts**: Use Row/Column over absolute positioning
3. **Add padding to containers**: Give content breathing room
4. **Consider mobile**: Test layouts at different sizes

---

## ⚡ Event Handling

### Button Events

```python
def handle_click():
    print("Button clicked!")

def handle_submit(value):
    print(f"Form submitted: {value}")

# Simple click handler
Button("Click Me", on_click=handle_click)

# Input with submit handler
TextInput("Enter text", on_submit=handle_submit)
```

### Custom Events

```python
from lumina.core.types import EventType

class MyWidget(Widget):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Custom logic
            self._emit_event(EventType.CLICK, event.pos)
            return True  # Event consumed
        return False  # Pass to parent
```

### State Management

```python
from lumina.core.reactive import State, Computed

# Reactive state
count = State(0)
name = State("")

# Computed values
greeting = Computed(
    lambda: f"Hello, {name.value}!" if name.value else "Hello!",
    dependencies=[name]
)

# Subscribe to changes
count.subscribe(lambda: print(f"Count changed: {count.value}"))

# Update state
count.value += 1  # Automatically triggers subscribers
```

---

## 📋 Examples

### 1. Contact Form

```python
from lumina import App, Window
from lumina.widgets import *
from lumina.themes import themes
from lumina.core.reactive import State

class ContactForm:
    def __init__(self):
        self.form_data = {
            "name": State(""),
            "email": State(""), 
            "message": State("")
        }
    
    def create_window(self):
        return Window(
            title="Contact Form",
            theme=themes.material_light,
            children=[
                Card(
                    title="Get in Touch",
                    padding=Padding.all(24),
                    children=[
                        Column(
                            spacing=16,
                            children=[
                                TextInput(
                                    label="Your Name",
                                    placeholder="John Doe",
                                    on_change=lambda v: setattr(self.form_data["name"], 'value', v)
                                ),
                                TextInput(
                                    label="Email Address", 
                                    placeholder="john@example.com",
                                    on_change=lambda v: setattr(self.form_data["email"], 'value', v)
                                ),
                                TextInput(
                                    label="Message",
                                    placeholder="Your message here...",
                                    multiline=True,
                                    on_change=lambda v: setattr(self.form_data["message"], 'value', v)
                                ),
                                Row([
                                    Button("Send Message", variant="primary", on_click=self.submit),
                                    Button("Clear", variant="secondary", on_click=self.clear)
                                ])
                            ]
                        )
                    ]
                )
            ]
        )
    
    def submit(self):
        print("Submitting form:")
        print(f"Name: {self.form_data['name'].value}")
        print(f"Email: {self.form_data['email'].value}")
        print(f"Message: {self.form_data['message'].value}")
    
    def clear(self):
        for field in self.form_data.values():
            field.value = ""

# Run the app
app = App()
form = ContactForm()
app.run(form.create_window())
```

### 2. Data Dashboard

```python
# See examples/modern_showcase.py for a complete data dashboard example
```

### 3. Settings Panel

```python
from lumina.core.reactive import State

class SettingsPanel:
    def __init__(self):
        self.settings = {
            "theme": State("light"),
            "notifications": State(True),
            "auto_save": State(False)
        }
    
    def create_window(self):
        return Window(
            title="Settings",
            children=[
                Column([
                    Header("Application Settings"),
                    
                    Card(
                        title="Appearance",
                        children=[
                            Row([
                                Text("Theme:"),
                                Button("Light", 
                                      variant="primary" if self.settings["theme"].value == "light" else "secondary",
                                      on_click=lambda: self.set_setting("theme", "light")),
                                Button("Dark",
                                      variant="primary" if self.settings["theme"].value == "dark" else "secondary", 
                                      on_click=lambda: self.set_setting("theme", "dark"))
                            ])
                        ]
                    ),
                    
                    Card(
                        title="Preferences", 
                        children=[
                            # Add checkboxes, toggles, etc.
                            Button("Save Settings", variant="primary", on_click=self.save_settings)
                        ]
                    )
                ])
            ]
        )
    
    def set_setting(self, key, value):
        self.settings[key].value = value
    
    def save_settings(self):
        print("Settings saved!")
```

---

## 📚 API Reference

### Core Classes

#### `App`
Main application class.

```python
App(name: str = "Lumina App", version: str = "1.0.0", debug: bool = False)
```

**Methods:**
- `run(window)` - Start the application
- `quit()` - Exit the application

#### `Window`  
Main window container.

```python
Window(
    title: str = "Lumina Window",
    width: int = 800,
    height: int = 600,
    theme: Theme = themes.default_light,
    children: list[Widget] = None,
    resizable: bool = True,
    on_close: Callable = None
)
```

**Methods:**
- `add_child(widget)` - Add widget to window
- `remove_child(widget)` - Remove widget from window
- `invalidate()` - Request redraw

#### `Widget`
Base class for all UI components.

```python
Widget(
    id: str = None,
    style: Style = None,
    padding: Padding = None,
    margin: Margin = None,
    visible: bool = True
)
```

**Methods:**
- `calculate_size(width, height)` - Calculate preferred size
- `layout(rect)` - Position widget in rectangle  
- `render(surface)` - Draw widget to surface
- `handle_event(event)` - Process user events
- `invalidate()` - Request redraw

### Styling Classes

#### `Style`
Visual styling properties.

```python
Style(
    background_color: Color = None,
    foreground_color: Color = None,
    border_color: Color = None,
    border_width: float = 0,
    border_radius: float = 0,
    font_family: str = "system",
    font_size: float = 14,
    font_weight: str = "normal",
    # ... many more properties
)
```

#### `Theme`
Complete theme definition.

```python
Theme(
    primary_color: Color = "#0066CC",
    secondary_color: Color = "#6C757D", 
    background_color: Color = "#FFFFFF",
    # ... all theme properties
)
```

### Reactive Classes

#### `State[T]`
Reactive state container.

```python
state = State(initial_value)
state.value = new_value          # Triggers subscribers
state.subscribe(callback)        # Listen for changes
```

#### `Computed[T]`
Computed reactive value.

```python
computed = Computed(
    compute_fn=lambda: state1.value + state2.value,
    dependencies=[state1, state2]
)
computed.value  # Automatically recalculated when dependencies change
```

---

## ✅ Best Practices

### 1. **Project Structure**

```
my_lumina_app/
├── main.py              # App entry point
├── components/          # Custom widgets  
│   ├── __init__.py
│   ├── user_card.py
│   └── nav_bar.py
├── themes/              # Custom themes
│   ├── __init__.py
│   └── company_theme.py
├── utils/               # Helper functions
│   ├── __init__.py
│   └── data_helpers.py
└── requirements.txt     # Dependencies
```

### 2. **Component Design**

```python
# Good: Single responsibility
class UserProfile(Card):
    def __init__(self, user_data):
        super().__init__(
            title=user_data["name"],
            children=[
                Text(user_data["email"]),
                Text(user_data["role"]),
                Button("Edit", on_click=lambda: self.edit_user(user_data))
            ]
        )
    
    def edit_user(self, user_data):
        # Handle edit logic
        pass

# Good: Reusable and configurable
class StatusBadge(Text):
    def __init__(self, status, **kwargs):
        colors = {
            "active": "#28A745",
            "inactive": "#6C757D", 
            "pending": "#FFC107"
        }
        super().__init__(
            status.title(),
            color=colors.get(status, "#6C757D"),
            **kwargs
        )
```

### 3. **State Management**

```python
# Good: Centralized state
class AppState:
    def __init__(self):
        self.user = State(None)
        self.theme = State("light")
        self.notifications = State([])
    
    def login(self, user_data):
        self.user.value = user_data
    
    def add_notification(self, message):
        current = self.notifications.value.copy()
        current.append(message)
        self.notifications.value = current

# Good: State composition
app_state = AppState()

# Components subscribe to relevant state
user_profile = UserProfile(app_state.user)
theme_switcher = ThemeSwitcher(app_state.theme)
```

### 4. **Performance Tips**

```python
# Good: Lazy loading for large datasets
class DataTable(Widget):
    def get_visible_rows(self):
        start = self.current_page * self.rows_per_page
        end = start + self.rows_per_page
        return self.data[start:end]

# Good: Memoization for expensive calculations
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_layout(width, height, children_count):
    # Expensive layout calculation
    pass

# Good: Efficient event handling
def handle_click(self, event):
    if not self.contains_point(*event.pos):
        return False  # Don't process irrelevant events
    
    # Process the event
    return True
```

### 5. **Error Handling**

```python
# Good: Graceful error handling
class SafeTextInput(TextInput):
    def __init__(self, validator=None, **kwargs):
        super().__init__(**kwargs)
        self.validator = validator
    
    def _on_value_changed(self):
        try:
            if self.validator:
                self.validator(self.value)
            super()._on_value_changed()
        except ValueError as e:
            # Show error state
            self.style.border_color = "#DC3545"
            print(f"Validation error: {e}")

# Good: User feedback
def save_data(self):
    try:
        # Save operation
        self.show_success("Data saved successfully!")
    except Exception as e:
        self.show_error(f"Failed to save: {e}")
```

### 6. **Testing**

```python
# Good: Testable components
class CalculatorWidget(Widget):
    def __init__(self):
        self.result = State(0)
        super().__init__()
    
    def add(self, a, b):
        self.result.value = a + b
        return self.result.value

# Test the component
def test_calculator():
    calc = CalculatorWidget()
    result = calc.add(2, 3)
    assert result == 5
    assert calc.result.value == 5
```

---

## 🎯 Conclusion

Lumina provides everything you need to build beautiful, modern GUI applications in Python. With its declarative API, reactive state management, and stunning built-in themes, you can focus on your app's logic while Lumina handles the visual polish.

### Key Benefits:
- ✅ **Easy to Learn**: Intuitive API that feels natural
- ✅ **Beautiful by Default**: Modern design without extra work
- ✅ **Type Safe**: Full type hints for excellent IDE support
- ✅ **Performance**: Efficient rendering and layout system
- ✅ **Flexible**: Customizable themes and components
- ✅ **Small Footprint**: Only ~10MB total dependency size

### Next Steps:
1. 🚀 [Try the examples](#-examples) to see Lumina in action
2. 🎨 [Experiment with themes](#-theming-system) to match your brand
3. 🧩 [Build custom components](#-best-practices) for your specific needs
4. 📚 [Explore the API reference](#-api-reference) for advanced features

**Ready to build something amazing? Start coding with Lumina today!** 🌟

---

*For more examples and advanced usage, check out the `examples/` directory in the repository.*