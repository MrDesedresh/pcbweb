from ..database import Component


class Motherboard(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "motherboard"