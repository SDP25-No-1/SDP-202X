"""
level_up_ui.py
-------------
Level-up notification UI component that displays when player gains a level.

Responsibilities
----------------
- Show "LEVEL UP!" notification with level number
- Display upgrade choices (Health +1, Damage +50%, Speed +10%)
- Handle user selection and apply chosen upgrade
- Pause game while waiting for user choice
- Handle rendering and visibility lifecycle
"""

import pygame
import time
from typing import List, Tuple, Callable, Optional
from src.ui.base_ui import BaseUI
from src.core.debug.debug_logger import DebugLogger


class LevelUpUI(BaseUI):
    """Interactive level-up UI that appears when player levels up with upgrade choices."""

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

        # Larger area to accommodate upgrade choices
        width, height = 500, 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        super().__init__(x, y, width, height, layer)

        # State management
        self.is_active = False
        self.choice_made = False
        self.selected_choice = None

        # Level information
        self.current_level = 1

        # Upgrade choices
        self.upgrade_choices = [
            {
                "name": "Health +1",
                "description": "Increase max health by 1",
                "color": (255, 100, 100),  # Red
                "effect": "health"
            },
            {
                "name": "Damage +50%",
                "description": "Increase damage by 50%",
                "color": (100, 255, 100),  # Green
                "effect": "damage"
            },
            {
                "name": "Speed +10%",
                "description": "Increase movement speed by 10%",
                "color": (100, 150, 255),  # Blue
                "effect": "speed"
            }
        ]

        # Button rectangles for each choice
        self.choice_buttons = []

        # Visual settings
        self.font = None
        self.button_font = None
        self.background_color = (30, 30, 30, 230)  # Darker semi-transparent
        self.text_color = (255, 255, 100)  # Golden yellow
        self.border_color = (255, 200, 50)  # Golden
        self.hover_color = (80, 80, 80, 200)  # Hover state

        DebugLogger.init("LevelUpUI")

    def show_level_up(self, level: int):
        """
        Activate the level-up notification with upgrade choices.

        Args:
            level: The new level the player achieved
        """
        self.current_level = level
        self.is_active = True
        self.choice_made = False
        self.selected_choice = None
        self.visible = True

        # Initialize fonts if not done yet
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 48)
                self.button_font = pygame.font.Font(None, 24)
                DebugLogger.state("LevelUpUI fonts initialized")
            except:
                self.font = pygame.font.Font(None, 48)
                self.button_font = pygame.font.Font(None, 24)

        # Calculate button positions
        self._calculate_button_positions()

        DebugLogger.action(f"LevelUpUI showing for level {level}")

    def _calculate_button_positions(self):
        """Calculate positions for upgrade choice buttons."""
        button_width = 140
        button_height = 80
        button_spacing = 20
        total_width = len(self.upgrade_choices) * button_width + (len(self.upgrade_choices) - 1) * button_spacing
        start_x = (self.rect.width - total_width) // 2
        button_y = 150

        self.choice_buttons = []
        for i, choice in enumerate(self.upgrade_choices):
            button_x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.choice_buttons.append(button_rect)

    def update(self, mouse_pos):
        """
        Update UI state based on mouse position.

        Args:
            mouse_pos: Current mouse position
        """
        if not self.is_active or self.choice_made:
            return

        # Check for hover on buttons (visual feedback handled in render)
        self.hover_index = None
        for i, button_rect in enumerate(self.choice_buttons):
            if button_rect.collidepoint(mouse_pos):
                self.hover_index = i
                break

    def handle_click(self, mouse_pos) -> Optional[str]:
        """
        Handle mouse click on upgrade choices.

        Args:
            mouse_pos: Current mouse position

        Returns:
            The selected upgrade effect or None if no choice made
        """
        if not self.is_active or self.choice_made:
            return None

        for i, button_rect in enumerate(self.choice_buttons):
            if button_rect.collidepoint(mouse_pos):
                self.choice_made = True
                self.selected_choice = self.upgrade_choices[i]["effect"]
                DebugLogger.action(f"LevelUpUI choice selected: {self.selected_choice}")

                # Auto-hide after selection
                pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Hide after 500ms
                return self.selected_choice

        return None

    def hide(self):
        """Hide the level-up notification."""
        self.visible = False
        self.is_active = False
        self.choice_made = False
        self.selected_choice = None
        DebugLogger.state("LevelUpUI hidden")

    def render_surface(self):
        """
        Create and return the level-up notification surface with upgrade choices.

        Returns:
            pygame.Surface: The rendered notification
        """
        if not self.visible or not self.font:
            # Return empty surface if not visible
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        # Create transparent surface
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Draw semi-transparent background
        pygame.draw.rect(surface, self.background_color, surface.get_rect(), border_radius=15)

        # Draw border
        pygame.draw.rect(surface, self.border_color, surface.get_rect(), 3, border_radius=15)

        # Render "LEVEL UP!" text
        level_up_text = self.font.render("LEVEL UP!", True, self.text_color)
        level_up_rect = level_up_text.get_rect(centerx=surface.get_width()//2, y=20)
        surface.blit(level_up_text, level_up_rect)

        # Render level number
        level_font = pygame.font.Font(None, 32)
        level_text = level_font.render(f"Reached Level {self.current_level}", True, self.text_color)
        level_rect = level_text.get_rect(centerx=surface.get_width()//2, y=70)
        surface.blit(level_text, level_rect)

        # Render instruction text
        if not self.choice_made:
            instruction_font = pygame.font.Font(None, 20)
            instruction_text = instruction_font.render("Choose an upgrade:", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(centerx=surface.get_width()//2, y=110)
            surface.blit(instruction_text, instruction_rect)

        # Render upgrade choice buttons
        if self.choice_buttons and self.button_font:
            for i, (choice, button_rect) in enumerate(zip(self.upgrade_choices, self.choice_buttons)):
                # Determine button color (hover effect)
                if hasattr(self, 'hover_index') and i == self.hover_index:
                    button_color = self.hover_color
                else:
                    button_color = (*choice["color"], 150)  # Semi-transparent version

                # Draw button background
                pygame.draw.rect(surface, button_color, button_rect, border_radius=8)
                pygame.draw.rect(surface, choice["color"], button_rect, 2, border_radius=8)

                # Draw upgrade name
                name_text = self.button_font.render(choice["name"], True, (255, 255, 255))
                name_rect = name_text.get_rect(centerx=button_rect.centerx, y=button_rect.y + 15)
                surface.blit(name_text, name_rect)

                # Draw upgrade description (smaller font)
                desc_font = pygame.font.Font(None, 16)
                desc_text = desc_font.render(choice["description"], True, (200, 200, 200))
                desc_rect = desc_text.get_rect(centerx=button_rect.centerx, y=button_rect.y + 40)
                surface.blit(desc_text, desc_rect)

        # Show selection confirmation
        if self.choice_made and self.selected_choice:
            confirmation_font = pygame.font.Font(None, 24)
            selected_choice_name = next((c["name"] for c in self.upgrade_choices if c["effect"] == self.selected_choice), "Unknown")
            confirmation_text = confirmation_font.render(f"Selected: {selected_choice_name}", True, (100, 255, 100))
            confirmation_rect = confirmation_text.get_rect(centerx=surface.get_width()//2, y=250)
            surface.blit(confirmation_text, confirmation_rect)

        return surface

    def is_choice_pending(self) -> bool:
        """Return True if UI is active and waiting for user choice."""
        return self.is_active and not self.choice_made