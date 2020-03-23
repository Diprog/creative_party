class Action:
    def __init__(self, type, payload=''):
        self.type = type
        self.payload = payload


class TextButton(Action):
    def __init__(self, **kwargs):
        super().__init__(self)
        self.type = 'text'


button = TextButton(payload='kek')
print(button.type, button.payload)