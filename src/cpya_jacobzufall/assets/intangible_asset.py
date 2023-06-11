# intangible_asset.py

from asset import Asset


class IntangibleAsset(Asset):
    def __init__(self, name: str, life: float, value: float):
        super().__init__(name=name, life=life, value=value)

    def amortize(self):
        pass
