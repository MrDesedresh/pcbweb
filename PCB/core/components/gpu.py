from ..database import Component


class GPU(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "gpu"