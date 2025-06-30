"""
Lumina - A modern Python GUI framework
Simple to use, beautiful to behold, completely standards-compliant
"""

__version__ = "0.1.0"
__author__ = "Lumina Contributors"
__license__ = "MIT"

from lumina.core.app import App
from lumina.core.window import Window
from lumina.widgets import *
from lumina.layouts import *
from lumina.themes import Theme, themes

__all__ = [
    "App",
    "Window",
    "Theme",
    "themes",
]