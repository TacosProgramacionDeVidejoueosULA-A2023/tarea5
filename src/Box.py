from typing import Dict

from src.GameObject import GameObject

class Box(GameObject):
    def __init__(
        self,
        i: int,
        j: int,
        width: int,
        height: int,
        frame_index: int,
        soliness: Dict[str, bool],
    ) -> None:
        self.i = i
        self.j = j
        self.spawned_key = False
        super().__init__(
            self.j * width,
            self.i * height,
            width,
            height,
            "tiles",
            frame_index,
            soliness,
        )
