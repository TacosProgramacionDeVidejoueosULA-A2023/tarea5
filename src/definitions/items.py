"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for items.
"""
from typing import Dict, Any

import random

from gale.timer import Timer

import settings
from src.GameItem import GameItem
from src.Player import Player


def pickup_coin(
    coin: GameItem, player: Player, points: int, color: int, time: float
) -> None:
    if points == 1000000:
        if player.allow_to_grab_key:
            player.won = True
    else:
        if player.score < 200 and player.level == 1 and not player.alarm_went_off:
            settings.SOUNDS["pickup_coin"].stop()
            settings.SOUNDS["pickup_coin"].play()
            player.score += points
            player.coins_counter[color] += 1
            Timer.after(time, lambda: coin.respawn())
        
        if player.level == 2:
            settings.SOUNDS["pickup_coin"].stop()
            settings.SOUNDS["pickup_coin"].play()
            player.score += points
            player.coins_counter[color] += 1
            Timer.after(time, lambda: coin.respawn())

    if player.score >= 200 and player.level == 1 and not player.alarm_went_off:
         player.alarm_went_off = True
         settings.SOUNDS["levelup"].stop()
         settings.SOUNDS["levelup"].play()


def pickup_green_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 1, 62, random.uniform(2, 4))


def pickup_blue_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 5, 61, random.uniform(5, 8))


def pickup_red_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 20, 55, random.uniform(10, 18))


def pickup_yellow_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 50, 54, random.uniform(20, 25))

def pickup_key(coin: GameItem, player: Player):
    pickup_coin(coin, player, 1000000, 68, random.uniform(20, 25))   


ITEMS: Dict[str, Dict[int, Dict[str, Any]]] = {
    "coins": {
        62: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "winner": False,
            "on_consume": pickup_green_coin,
        },
        61: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "winner": False,
            "on_consume": pickup_blue_coin,
        },
        55: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "winner": False,
            "on_consume": pickup_red_coin,
        },
        54: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "winner": False,
            "on_consume": pickup_yellow_coin,
        },
        68: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "winner": True,
            "on_consume": pickup_key,
        },
    }
}
