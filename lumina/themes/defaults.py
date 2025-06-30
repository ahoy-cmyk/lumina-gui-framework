from lumina.themes.theme import Theme


class ThemeCollection:
    """Collection of default themes"""
    
    @property
    def default_light(self) -> Theme:
        """Default light theme"""
        return Theme()
    
    @property
    def default_dark(self) -> Theme:
        """Default dark theme"""
        return Theme(
            # Core colors
            primary_color="#4D9FFF",
            secondary_color="#868E96",
            success_color="#51CF66",
            warning_color="#FFD43B",
            error_color="#FF6B6B",
            info_color="#339AF0",
            
            # Surface colors
            background_color="#0D1117",
            surface_color="#161B22",
            overlay_color="rgba(255, 255, 255, 0.1)",
            
            # Text colors
            text_primary="#E6EDF3",
            text_secondary="#7D8590",
            text_disabled="#484F58",
            text_hint="#7D8590",
            
            # State colors
            hover_overlay="rgba(255, 255, 255, 0.06)",
            focus_overlay="rgba(77, 159, 255, 0.15)",
            pressed_overlay="rgba(255, 255, 255, 0.1)",
            selected_overlay="rgba(77, 159, 255, 0.1)",
            
            # Border colors
            border_color="#30363D",
            divider_color="#21262D",
            
            # Shadows
            shadow_color="rgba(0, 0, 0, 0.3)",
        )
    
    @property
    def material_light(self) -> Theme:
        """Material Design 3 inspired light theme"""
        return Theme(
            primary_color="#6750A4",
            secondary_color="#625B71",
            success_color="#00C853",
            warning_color="#FFB300",
            error_color="#F44336",
            info_color="#2196F3",
            
            background_color="#FEF7FF",
            surface_color="#FFFBFE",
            text_primary="#1C1B1F",
            text_secondary="#49454F",
            
            border_color="#E8DEF8",
            radius_base=12,
            radius_lg=16,
            radius_xl=28,
        )
    
    @property
    def material_dark(self) -> Theme:
        """Material Design 3 inspired dark theme"""
        return Theme(
            primary_color="#D0BCFF",
            secondary_color="#CCC2DC",
            success_color="#69F0AE",
            warning_color="#FFD54F",
            error_color="#EF5350",
            info_color="#64B5F6",
            
            background_color="#1C1B1F",
            surface_color="#201F24",
            text_primary="#E6E1E5",
            text_secondary="#CAC4D0",
            
            border_color="#49454F",
            radius_base=12,
            radius_lg=16,
            radius_xl=28,
        )
    
    @property
    def github_light(self) -> Theme:
        """GitHub-inspired light theme"""
        return Theme(
            primary_color="#0969DA",
            secondary_color="#6E7781",
            success_color="#1A7F37",
            warning_color="#9A6700",
            error_color="#CF222E",
            info_color="#0969DA",
            
            background_color="#FFFFFF",
            surface_color="#F6F8FA",
            text_primary="#1F2328",
            text_secondary="#656D76",
            
            border_color="#D1D9E0",
            font_family="SF Pro Display, Segoe UI, sans-serif",
        )
    
    @property
    def github_dark(self) -> Theme:
        """GitHub-inspired dark theme"""
        return Theme(
            primary_color="#58A6FF",
            secondary_color="#8B949E",
            success_color="#3FB950",
            warning_color="#D29922",
            error_color="#F85149",
            info_color="#58A6FF",
            
            background_color="#0D1117",
            surface_color="#161B22",
            text_primary="#E6EDF3",
            text_secondary="#7D8590",
            
            border_color="#30363D",
            font_family="SF Pro Display, Segoe UI, sans-serif",
        )


# Global theme collection instance
themes = ThemeCollection()