from ..database import Component


class CPU(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "cpu"