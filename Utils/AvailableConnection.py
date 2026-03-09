class AvailableConnection:
    def __init__(self, _addr: tuple, _expiration: int, _name: str, _public_key: str):
        self.address = _addr
        self.expiration = _expiration
        self.name = _name
        self.public_key = _public_key

    def __str__(self):
        return f"{self.name} @{self.expiration}-{self.address[0]}:{self.address[1]} with {self.public_key}"

    __repr__ = __str__
