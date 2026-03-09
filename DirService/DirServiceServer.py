from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from Utils.protocol import send_vanilla
from Utils.Const import Const
from select import select


class Server:
    def __init__(self, _FetchCallback: callable):
        self.FetchCallback = _FetchCallback
        self.socket = socket()  # the server socket, using tcp
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', 55555))   # binding to port 5555
        self.clients: list[socket] = [self.socket]  # a list of all currently connected clients

    def Main(self):
        try:
            self.socket.listen(Const.MaxConcurrentClients)
            while 1:
                client: socket
                for client in select(self.clients, [], [])[0]:  # for each ready-to-read socket
                    if client is self.socket:   # ready to accept a client
                        _con, _adr = self.socket.accept()  # accept a client connection
                        print(f"new client: {_adr}")
                        self.clients.append(_con)   # add the client to the client list
                    else:   # a message from a client
                        action = client.recv(1)
                        match action:
                            case Const.DisconnectSignal:
                                print(f"client disconnecting")
                                self.clients.remove(client)

                            case Const.DirServiceEntry:
                                available_agents = self.FetchCallback("available_agents")[1]
                                print(f"dir service plz {available_agents}")
                                available_agents = [agent.address for agent in available_agents]
                                client.send(send_vanilla(f"{available_agents}"))
                                # use new protocol

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    # app = Server()
    # app.Main()
    pass
