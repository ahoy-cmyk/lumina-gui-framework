from typing import TypeVar, Generic, Callable, Any, Optional
from weakref import WeakSet
import asyncio

T = TypeVar("T")


class State(Generic[T]):
    """Reactive state container that notifies observers on change"""
    
    def __init__(self, initial_value: T):
        self._value = initial_value
        self._observers: WeakSet[Callable] = WeakSet()
        self._async_observers: WeakSet[Callable] = WeakSet()
    
    @property
    def value(self) -> T:
        return self._value
    
    @value.setter
    def value(self, new_value: T) -> None:
        if self._value != new_value:
            self._value = new_value
            self._notify_observers()
    
    def subscribe(self, observer: Callable[[], None], async_observer: bool = False) -> Callable[[], None]:
        """Subscribe to state changes. Returns unsubscribe function."""
        if async_observer:
            self._async_observers.add(observer)
        else:
            self._observers.add(observer)
        
        def unsubscribe():
            if async_observer:
                self._async_observers.discard(observer)
            else:
                self._observers.discard(observer)
        
        return unsubscribe
    
    def _notify_observers(self) -> None:
        for observer in list(self._observers):
            try:
                observer()
            except Exception as e:
                print(f"Error in state observer: {e}")
        
        for async_observer in list(self._async_observers):
            asyncio.create_task(self._call_async_observer(async_observer))
    
    async def _call_async_observer(self, observer: Callable) -> None:
        try:
            await observer()
        except Exception as e:
            print(f"Error in async state observer: {e}")
    
    def __repr__(self) -> str:
        return f"State({self._value!r})"


class Computed(Generic[T]):
    """Computed value that updates when dependencies change"""
    
    def __init__(self, compute_fn: Callable[[], T], dependencies: Optional[list[State]] = None):
        self._compute_fn = compute_fn
        self._cached_value: Optional[T] = None
        self._is_dirty = True
        self._observers: WeakSet[Callable] = WeakSet()
        
        if dependencies:
            for dep in dependencies:
                dep.subscribe(self._mark_dirty)
    
    def _mark_dirty(self) -> None:
        self._is_dirty = True
        self._notify_observers()
    
    @property
    def value(self) -> T:
        if self._is_dirty:
            self._cached_value = self._compute_fn()
            self._is_dirty = False
        return self._cached_value
    
    def subscribe(self, observer: Callable[[], None]) -> Callable[[], None]:
        self._observers.add(observer)
        
        def unsubscribe():
            self._observers.discard(observer)
        
        return unsubscribe
    
    def _notify_observers(self) -> None:
        for observer in list(self._observers):
            try:
                observer()
            except Exception as e:
                print(f"Error in computed observer: {e}")