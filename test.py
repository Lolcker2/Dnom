"""from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST
sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.bind(('', 1200))
while 1:
    signal, address = sock.recvfrom(1)
    if signal == chr(7).encode():
        sock.sendto(chr(64).encode(), address)"""

from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST, IPPROTO_TCP, SO_REUSEADDR


class Const:
    # Broadcast consts
    BroadCastEntry = chr(7).encode()   # bell
    BroadCastResponse = chr(64).encode()    # @

    # Tcp protocol
    DisconnectSignal = 'D'.encode()    # D
    InComingMessageSignal = 'M'.encode()    # M
    DirServiceEntry = chr(63).encode()  # ?

    # Misc
    SocketTimeOut = 0.5     # sec
    DefaultPort = 12000
    BroadCastFreq = 1   # seconds


def receive(_sock: socket) -> tuple:
    data = b''
    while b'~' not in data:
        res = _sock.recvfrom(1)[0]
        data += res
    result = _sock.recvfrom(int(data[0:-1].decode()))
    return result[0].decode(), result[1]


server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)    # the client socket, using udp
server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)   # setting the socket to broadcast mode
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('', Const.DefaultPort))     # binding the socket to the address

tcp_socket = socket(AF_INET, SOCK_DGRAM)
name = 'hello world!'




def send_vanilla(_msg:str) -> bytes:
    return f"{str(len(_msg)).zfill(8)}{_msg}".encode()

def respond_to_broadcast():
    message, address = server_socket.recvfrom(1)     # receive a bit (1 bit long message)
    print(f"message{message}")
    if message == Const.BroadCastEntry:     # if received a 'BroadCastEntry' char
        server_socket.sendto(str(len(name)).zfill(8).encode(), address)
        server_socket.sendto(name.encode(), address)      # send back 'BroadCastResponse' char
       # server_socket.sendto(send_vanilla('hello world!'), address)
        print("sent")

        # tcp_socket.connect(address)
        # tcp_socket.send(Const.DirServiceEntry)
        # result = receive(tcp_socket)
        # print(f"result: {result}")


if __name__ == '__main__':
    while 1:
        respond_to_broadcast()


