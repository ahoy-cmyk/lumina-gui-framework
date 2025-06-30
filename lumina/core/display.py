"""
Display utilities for high DPI support and platform-specific optimizations
"""
import sys
import os
from typing import Tuple


class DisplayManager:
    """Manages display settings and high DPI support"""
    
    _scale_factor = None
    _is_retina = None
    
    @classmethod
    def get_scale_factor(cls) -> float:
        """Get the display scale factor"""
        if cls._scale_factor is None:
            cls._detect_display_properties()
        return cls._scale_factor
    
    @classmethod
    def is_retina_display(cls) -> bool:
        """Check if running on a Retina/high DPI display"""
        if cls._is_retina is None:
            cls._detect_display_properties()
        return cls._is_retina
    
    @classmethod
    def _detect_display_properties(cls):
        """Detect display properties once and cache them"""
        cls._scale_factor = 1.0
        cls._is_retina = False
        
        if sys.platform == "darwin":
            # macOS detection
            try:
                # Try using Objective-C to get actual scale factor
                try:
                    import objc
                    from AppKit import NSScreen
                    screen = NSScreen.mainScreen()
                    if screen:
                        cls._scale_factor = screen.backingScaleFactor()
                        cls._is_retina = cls._scale_factor > 1.0
                        return
                except ImportError:
                    pass
                
                # Fallback: check system_profiler
                import subprocess
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                      capture_output=True, text=True, timeout=2)
                if 'Retina' in result.stdout or 'Resolution:' in result.stdout:
                    # Look for high resolution indicators
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'Resolution:' in line and ('2560' in line or '2880' in line or '3840' in line):
                            cls._scale_factor = 2.0
                            cls._is_retina = True
                            break
                        elif 'Retina' in line:
                            cls._scale_factor = 2.0
                            cls._is_retina = True
                            break
            except:
                pass
        
        elif sys.platform == "win32":
            # Windows high DPI detection
            try:
                import ctypes
                from ctypes import wintypes
                
                # Get DPI awareness
                user32 = ctypes.windll.user32
                dpi = user32.GetDpiForSystem()
                if dpi > 96:  # Standard DPI is 96
                    cls._scale_factor = dpi / 96.0
                    cls._is_retina = cls._scale_factor > 1.5
            except:
                pass
        
        # Linux and other platforms can be added here
    
    @classmethod
    def setup_high_dpi_support(cls):
        """Setup environment for high DPI support"""
        if sys.platform == "darwin":
            # macOS settings
            os.environ['SDL_VIDEO_HIGHDPI_DISABLED'] = '0'
            # Enable high quality scaling
            os.environ['SDL_VIDEO_MAC_FULLSCREEN_SPACES'] = '1'
        
        elif sys.platform == "win32":
            # Windows settings
            try:
                import ctypes
                # Set DPI awareness
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
    
    @classmethod
    def scale_font_size(cls, base_size: float) -> float:
        """Scale font size for current display"""
        # For now, disable auto-scaling to ensure crisp text
        # Users can manually adjust font sizes if needed
        return base_size
    
    @classmethod
    def scale_window_size(cls, width: int, height: int) -> Tuple[int, int]:
        """Scale window size for current display"""
        scale = cls.get_scale_factor()
        if scale > 1.0:
            # For high DPI, we might want to keep logical size the same
            # but pygame will automatically scale the content
            return width, height
        return width, height