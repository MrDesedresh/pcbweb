from ..database import Component


class PSU(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "psu"