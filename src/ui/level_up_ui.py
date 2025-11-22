"""
level_up_ui.py
-------------
Level-up notification UI component that displays when player gains a level.

Responsibilities
----------------
- Show "LEVEL UP!" notification with level number
- Auto-dismiss after a short duration
- Handle rendering and visibility lifecycle
"""

import pygame
import time
from src.ui.base_ui import BaseUI
from src.core.debug.debug_logger import DebugLogger


class LevelUpUI(BaseUI):
    """Animated level-up notification that appears when player levels up."""

    def __init__(self, display_manager, layer=150):
        """
        Initialize level-up UI element.

        Args:
            display_manager: Provides screen resolution for centering
            layer: Rendering layer (high to appear on top)
        """
        # Calculate center position for level-up text
        screen_width = display_manager.get_width()
        screen_height = display_manager.get_height()

        # Large centered area for the notification
        width, height = 400, 100
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50  # Slightly above center

        super().__init__(x, y, width, height, layer)

        # Animation and timing
        self.show_duration = 3.0  # Show for 3 seconds
        self.start_time = None
        self.is_active = False

        # Level information
        self.current_level = 1

        # Visual settings
        self.font = None
        self.background_color = (50, 50, 50, 200)  # Semi-transparent dark
        self.text_color = (255, 255, 100)  # Golden yellow
        self.border_color = (255, 200, 50)  # Golden

        DebugLogger.init("LevelUpUI")

    def show_level_up(self, level: int):
        """
        Activate the level-up notification.

        Args:
            level: The new level the player achieved
        """
        self.current_level = level
        self.start_time = time.time()
        self.is_active = True
        self.visible = True

        # Initialize font if not done yet
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 48)
                DebugLogger.state("LevelUpUI font initialized")
            except:
                self.font = pygame.font.Font(None, 48)

        DebugLogger.action(f"LevelUpUI showing for level {level}")

    def update(self, mouse_pos):
        """
        Update animation and check if display duration has elapsed.

        Args:
            mouse_pos: Current mouse position (not used for this UI)
        """
        if not self.is_active:
            return

        # Check if display duration has elapsed
        if self.start_time and (time.time() - self.start_time) >= self.show_duration:
            self.hide()

    def hide(self):
        """Hide the level-up notification."""
        self.visible = False
        self.is_active = False
        DebugLogger.state("LevelUpUI hidden")

    def render_surface(self):
        """
        Create and return the level-up notification surface.

        Returns:
            pygame.Surface: The rendered notification
        """
        if not self.visible or not self.font:
            # Return empty surface if not visible
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        # Create transparent surface
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Draw semi-transparent background
        pygame.draw.rect(surface, self.background_color, surface.get_rect(), border_radius=10)

        # Draw border
        pygame.draw.rect(surface, self.border_color, surface.get_rect(), 3, border_radius=10)

        # Render "LEVEL UP!" text
        level_up_text = self.font.render("LEVEL UP!", True, self.text_color)
        level_up_rect = level_up_text.get_rect(centerx=surface.get_width()//2, y=20)
        surface.blit(level_up_text, level_up_rect)

        # Render level number
        level_font = pygame.font.Font(None, 36)
        level_text = level_font.render(f"Level {self.current_level}", True, self.text_color)
        level_rect = level_text.get_rect(centerx=surface.get_width()//2, y=60)
        surface.blit(level_text, level_rect)

        return surface