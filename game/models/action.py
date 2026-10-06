from dataclasses import dataclass

@dataclass
class Action:
    id: str
    title: str
    cost: dict  # {"homework": 7}
    self_effects: dict
    target_effects: dict
    description: str = ""
