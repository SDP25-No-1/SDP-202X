from src.core.debug.debug_logger import DebugLogger

class ExpManager:
    """
    Manages all EXP-related logic for the player.

    Responsibilities
    ----------------
    - Receive EXP rewards when enemies are defeated
    - Track current EXP and required EXP for next level
    - Determine when a level-up occurs
    - Apply EXP growth curve
    - Trigger level-up UI and pause gameplay
    """

    def __init__(self, game_state):
        self.game_state = game_state
        self.level_up_ui = None  # Will be set by game initialization
        self.pending_upgrade = None


    # Exp Up
    def exp_up(self, amount: int):
        """
        Called when an enemy is defeated.
        Adds EXP and checks for level-up.
        """
        self.game_state.exp += amount

        DebugLogger.state(
        f"[ExpManager][Exp Up] +{amount} ({self.game_state.exp}/{self.game_state.level_exp})"
        )

        if self.is_level_up():
            self.level_up()


    def is_level_up(self):
        """Return True if current EXP >= required EXP."""
        return self.game_state.exp >= self.game_state.level_exp

    def set_level_up_ui(self, level_up_ui):
        """Set reference to LevelUpUI component."""
        self.level_up_ui = level_up_ui
        DebugLogger.state("ExpManager LevelUpUI reference set")

    def level_up(self):
        """
        1. Reset EXP
        2. Increase level
        3. Calculate next level EXP
        4. Show LevelUp UI and pause gameplay
        """
        self.game_state.exp = 0
        self.game_state.level += 1
        self.game_state.level_exp = self.calculate_next_exp(self.game_state.level)

        DebugLogger.state(
            f"[ExpManager][LEVEL UP] Level : {self.game_state.level} "
            f"(Next Required EXP: {self.game_state.level_exp})"
        )

        # Show level-up UI if available
        if self.level_up_ui:
            self.level_up_ui.show_level_up(self.game_state.level)
            DebugLogger.action(f"ExpManager triggered LevelUpUI for level {self.game_state.level}")
        else:
            DebugLogger.warning("ExpManager: No LevelUpUI reference available")

    def handle_upgrade_choice(self, upgrade_type: str):
        """
        Apply the selected upgrade to the player.

        Args:
            upgrade_type: The type of upgrade chosen ("health", "damage", or "speed")
        """
        if not self.game_state.player:
            DebugLogger.warning("ExpManager: No player reference available for upgrade")
            return

        player = self.game_state.player

        if upgrade_type == "health":
            # Increase max health by 1 and heal to full
            player.max_health += 1
            player.health = player.max_health
            DebugLogger.action(f"Applied health upgrade: +1 max health (new: {player.max_health})")

        elif upgrade_type == "damage":
            # Increase damage by 10%
            if hasattr(player, 'damage'):
                player.damage = int(player.damage * 1.1)
                DebugLogger.action(f"Applied damage upgrade: +10% (new: {player.damage})")
            else:
                DebugLogger.warning("Player has no damage attribute to upgrade")

        elif upgrade_type == "speed":
            # Increase speed by 10% permanently
            if hasattr(player, 'base_speed'):
                player.base_speed = player.base_speed * 1.1
                DebugLogger.action(f"Applied speed upgrade: +10% (new base_speed: {player.base_speed:.2f})")
            else:
                DebugLogger.warning("Player has no base_speed attribute to upgrade")

        else:
            DebugLogger.warning(f"Unknown upgrade type: {upgrade_type}")

    def is_level_up_ui_active(self) -> bool:
        """Check if level-up UI is currently active and waiting for user choice."""
        return self.level_up_ui is not None and self.level_up_ui.is_choice_pending()

    def calculate_next_exp(self, lv: int) -> int:
        """Smooth exponential EXP curve."""
        return int(30 * (1.15 ** (lv - 1)))

