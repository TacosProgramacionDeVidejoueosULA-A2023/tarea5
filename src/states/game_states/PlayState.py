"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""
from typing import Dict, Any

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Camera import Camera
from src.GameLevel import GameLevel
from src.Player import Player


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.camera = enter_params.get(
            "camera", Camera(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level, self.camera)
            pygame.mixer.music.load(settings.BASE_DIR / "sounds/music_grassland.ogg")
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            self.player = Player(0, settings.VIRTUAL_HEIGHT - 66, self.game_level, self.level)
            self.player.change_state("idle")

        self.timer = enter_params.get("timer", 30)

        def countdown_timer():
            if self.player.score < 200 and self.player.level == 1:
                self.timer -= 1

                if 0 < self.timer <= 5:
                    settings.SOUNDS["timer"].play()

            if self.player.level == 2:
                self.timer -= 1

                if 0 < self.timer <= 5:
                    settings.SOUNDS["timer"].play()

            if self.timer == 0:
                self.player.change_state("dead")

        Timer.every(1, countdown_timer)
        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)
        Timer.clear()

    def allow_to_grab_key(self):
        self.player.allow_to_grab_key = True
        self.winner_item.y = self.key_y_end
        Timer.clear()

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)
    
        if self.player.y >= self.player.tilemap.height:
            self.player.change_state("dead")

        self.camera.x = max(
            0,
            min(
                self.player.x + 8 - settings.VIRTUAL_WIDTH // 2,
                self.tilemap.width - settings.VIRTUAL_WIDTH,
            ),
        )
        self.camera.y = max(
            0,
            min(
                self.player.y + 10 - settings.VIRTUAL_HEIGHT // 2,
                self.tilemap.height - settings.VIRTUAL_HEIGHT,
            ),
        )

        self.game_level.update(dt)

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if item.is_winner and self.player.score >= 200 and self.player.next_level_enabled:
                    if not self.player.allow_to_grab_key:
                        self.winner_item = item
                        self.key_y_end = item.y - 16
                        Timer.tween(
                            0.1,
                            [
                                (item, {"y": self.key_y_end}),
                            ],
                            on_finish=self.allow_to_grab_key,
                        )
                        item.in_play = True
                    
            if not item.in_play or not item.collidable:
                continue

            if self.player.collides(item):
                item.on_collide(self.player)
                item.on_consume(self.player)

        if self.player.won:
            if self.player.won and self.level == 2:
                self.state_machine.change("game_over", self.player)
                return
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.state_machine.change(
                "victory", 
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
            )

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.timer}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                timer=self.timer,
            )
