from ..database import Component


class RAM(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "ram"