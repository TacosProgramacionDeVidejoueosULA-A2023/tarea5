import pygame
from typing import Dict, Any

from gale.input_handler import InputHandler, InputData, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings


class VictoryState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        settings.SOUNDS["level_complete"].play()
        self.level=enter_params["level"]
        self.camera=enter_params["camera"]
        self.game_level=enter_params["game_level"]
        self.player=enter_params["player"]
        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change(
                "play",
                level=self.level + 1,
                camera=self.camera,
                game_level=None,
                player=None,
            )

    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            f"Level {self.level} completed!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 30,
            (255, 255, 255),
            center=True,
        )
