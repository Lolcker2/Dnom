class State:
    def __init__(self, _state: dict):
        self.state = _state

    def set(self, _state: dict):
        self.state = _state

    def update(self, _key: str, _value) -> bool:
        try:
            self.state[_key] = _value
            return True
        except KeyError:
            return False

    def append(self, _key: str, _value) -> bool:
        try:
            self.state[_key].append(_value)
            return True
        except KeyError:
            return False

    def add(self, _key: str, _second_key: str, _value) -> bool:
        try:
            self.state[_key][_second_key].append(_value)
            return True
        except KeyError:
            self.state[_key].update({_second_key: _value})
            return True

    def remove(self, _key: str, _value) -> bool:
        try:
            self.state[_key].remove(_value)
            return True
        except KeyError:
            return False

    def rmv(self, _key: str, _lst: list) -> bool:
        try:
            [self.state[_key].remove(_value) for _value in _lst]
            return True
        except KeyError:
            return False

    def fetch(self, _key: str) -> tuple:
        try:
            return True, self.state[_key]
        except KeyError:
            return False, None

    def get(self) -> dict:
        return self.state
