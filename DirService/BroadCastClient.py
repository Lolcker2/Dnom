from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR
from time import sleep
from Utils.Const import Const
from Utils.AvailableConnection import AvailableConnection
from json import dumps
from Utils.Message import Message
from Utils.protocol import receive_vanilla


class BroadCastClient:
    def __init__(self, _FetchCallback: callable):
        self.FetchCallback = _FetchCallback
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)  # the server socket, using udp
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # setting the socket to broadcast mode
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', Const.DefaultPort))
        self.name = ""
        self.public = ""

    @staticmethod
    def vanilla_broadcast(_sock: socket, _msg: str, _address: tuple):
        msg = str(len(_msg)).zfill(8).encode()
        print(f"brod: {msg}")
        _sock.sendto(msg, _address)
        _sock.sendto(_msg.encode(), _address)

    def respond_to_broadcast(self):
        message, address = self.socket.recvfrom(1)  # receive a bit (1 bit long message)
        print(f"message{message}")
        if message == Const.BroadCastEntry:  # if received a 'BroadCastEntry' char
            # self.socket.sendto(Const.BroadCastResponse, address)
            self.vanilla_broadcast(self.socket, Const.BroadCastResponse.decode() + self.name + ',' + self.public, address)
            print("sent")

    def Main(self):
        while 1:
            _name = self.FetchCallback("name")[1]
            print(f"name: {_name}, {len(_name) > 1} ----------------------------------------")
            self.name = _name if len(_name) > 1 else self.name
            _public = self.FetchCallback("public")[1]
            self.public = _public if len(_public) > 1 else self.public
            self.respond_to_broadcast()
            sleep(Const.BroadCastFreq)



if __name__ == '__main__':
    # app = DirService()
    # app.Main()
    pass
