# tangible_asset.py

from asset import Asset


class TangibleAsset(Asset):
    def __init__(self, name: str, life: float, value: float, s_value: float):
        super().__init__(name=name, life=life, value=value, s_value=s_value)
