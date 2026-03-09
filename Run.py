from threading import Thread
from Utils.State import State
from DirService.DirService import DirService
from DirService.DirServiceServer import Server
from DirService.RouterServer import RouterServer
from DirService.RouterClient import RoutingClient
from DirService.LocalForwarder import Main as LocalForwarder
from Utils.protocol import generate_key_pair
from socket import gethostname, gethostbyname
from Utils.Const import Const
from DirService.BroadCastClient import BroadCastClient

class Program(State):
    def __init__(self):
        super().__init__({"MsgID_db": dict(), "public": "", "private": "", "available_agents": [], "queued_messages": [], "name": "", "chats": {}})
        # in order to save messages, need name (or address)
        self.host = (gethostbyname(gethostname()), Const.DefaultPort)
        self.DirService = DirService(self.fetch, self.update, self.append)
        self.Server = Server(self.fetch)
        self.SRouter = RouterServer(self.host, self.fetch, self.append, self.add)
        self.CRouter = RoutingClient(self.fetch, self.add, self.rmv)
        self.BClient = BroadCastClient(self.fetch)



    def GenerateKeys(self):
        private, public = generate_key_pair()
        self.update('public', public)
        self.update('private', private)

    def Main(self):
        ServiceThread = Thread(target=self.DirService.Main)
        ServiceThread.start()

        ServerThread = Thread(target=self.Server.Main)
        ServerThread.start()

        SRouterThread = Thread(target=self.SRouter.Main)
        SRouterThread.start()

        CRouterThread = Thread(target=self.CRouter.Main)
        CRouterThread.start()

        BClientThread = Thread(target=self.BClient.Main)
        BClientThread.start()

        LocalForwarder(self.fetch, self.update, self.append, self.add)


if __name__ == '__main__':
    app = Program()
    app.Main()

