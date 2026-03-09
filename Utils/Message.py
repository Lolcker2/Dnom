from Utils.Const import Const


hexify = lambda _field: b''.join([int(item).to_bytes() for item in _field])

class Message:
    def __init__(self, _action: bytes, _msgID: bytes, _nextIP: str, _payload: bytes):
        self.action = _action
        self.msgID = _msgID
        _nextIP = str(_nextIP)
        print(f"nextIP: {_nextIP}, length: {len(_nextIP)}")
        self.nextIP = (_nextIP.split(',')[0].replace('(', '').replace(')', '').replace("'", '')).strip()
        self.payload = _payload
        self.port =  _nextIP.split(',')[1]

    def Export(self) -> bytes:
        print(f"text: {self.payload}, length: {len(self.payload)}")
        header = (Const.CorrectDecryptionChar + self.action + self.msgID + hexify(self.nextIP.split('.'))
                + self.port.encode() + len(self.payload).to_bytes().rjust(Const.MaxMsgLength, b'\0'))
        return header + self.payload

    def __repr__(self) -> str:
        return Const.CorrectDecryptionChar.decode() + self.action.decode() + self.msgID.decode() + self.nextIP + self.payload.decode()
    
    def SetMsgID(self, _msgID: bytes) -> None:
        self.msgID = _msgID

