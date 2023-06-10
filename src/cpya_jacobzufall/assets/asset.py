# asset.py

class Asset:
    def __init__(self, name: str, life: float, value: float, s_value: float = 0.0):
        self.name = name
        self.life = life
        self.value = value
        self.s_value = s_value
