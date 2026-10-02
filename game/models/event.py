from dataclasses import dataclass

@dataclass
class RandomEvent:
    id: str
    title: str
    effects_1: dict
    effects_2: dict