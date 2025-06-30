from typing import TypeVar, Union, Optional, Callable, Any, Protocol, runtime_checkable
from dataclasses import dataclass
from enum import Enum
import pygame

Color = Union[tuple[int, int, int], tuple[int, int, int, int], str]
Size = Union[int, float, str]
Alignment = Union[str, tuple[str, str]]

T = TypeVar("T")
WidgetType = TypeVar("WidgetType", bound="Widget")


class SizeUnit(Enum):
    PIXELS = "px"
    PERCENT = "%"
    AUTO = "auto"
    FIT_CONTENT = "fit-content"


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float
    
    def to_pygame_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))
    
    def contains(self, x: float, y: float) -> bool:
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)


@dataclass
class Padding:
    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0
    
    @classmethod
    def all(cls, value: float) -> "Padding":
        return cls(value, value, value, value)
    
    @classmethod
    def symmetric(cls, vertical: float = 0, horizontal: float = 0) -> "Padding":
        return cls(vertical, horizontal, vertical, horizontal)


@dataclass
class Margin:
    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0
    
    @classmethod
    def all(cls, value: float) -> "Margin":
        return cls(value, value, value, value)
    
    @classmethod
    def symmetric(cls, vertical: float = 0, horizontal: float = 0) -> "Margin":
        return cls(vertical, horizontal, vertical, horizontal)


class EventType(Enum):
    CLICK = "click"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    CHANGE = "change"
    SUBMIT = "submit"
    MOUNT = "mount"
    UNMOUNT = "unmount"


@runtime_checkable
class Renderable(Protocol):
    def render(self, surface: pygame.Surface, rect: Rect) -> None:
        ...


@runtime_checkable
class Layoutable(Protocol):
    def calculate_size(self, available_width: float, available_height: float) -> tuple[float, float]:
        ...
    
    def layout(self, rect: Rect) -> None:
        ...