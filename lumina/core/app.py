from typing import Optional, Union
import asyncio
import sys
from lumina.core.window import Window


class App:
    """Main application class for Lumina applications"""
    
    def __init__(
        self,
        name: str = "Lumina App",
        version: str = "1.0.0",
        debug: bool = False,
    ):
        self.name = name
        self.version = version
        self.debug = debug
        self._windows: list[Window] = []
        self._main_window: Optional[Window] = None
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
    
    def run(self, window: Union[Window, list[Window]]) -> None:
        """Run the application with the given window(s)"""
        if isinstance(window, Window):
            self._windows = [window]
            self._main_window = window
        else:
            self._windows = window
            self._main_window = window[0] if window else None
        
        if not self._main_window:
            raise ValueError("At least one window must be provided")
        
        try:
            # Setup event loop for async support
            self._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._event_loop)
            
            # Run the main window
            self._main_window.run()
            
        except KeyboardInterrupt:
            if self.debug:
                print("\nApplication interrupted by user")
        except Exception as e:
            if self.debug:
                print(f"Application error: {e}")
                raise
            else:
                sys.exit(1)
        finally:
            # Cleanup
            if self._event_loop:
                self._event_loop.close()
    
    def quit(self) -> None:
        """Quit the application"""
        for window in self._windows:
            if hasattr(window, '_running'):
                window._running = False
    
    @property
    def windows(self) -> list[Window]:
        """Get all application windows"""
        return self._windows.copy()