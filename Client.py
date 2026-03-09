# does everyting
from Utils.Const import Const
from Utils.protocol import encrypt
from random import choice, randint
from socket import socket
from Utils.Message import Message
from Utils.AvailableConnection import AvailableConnection
from Utils.MsgID import MsgID

class Client:
    def __init__(self):
        self.available_agents = []
        self.socket = socket()
        self.public_key = '?'
        self.private_key = '?'
        self.name = "eyal"
        self.ids = dict() # temp

    def CreateMessagePath(self):
        path_length = min(Const.MessagePathLength, len(self.available_agents))
        path = [choice(list(self.available_agents)) for _ in range(path_length)]
        while len(set(path)) < path_length:
            path.append(choice(list(self.available_agents)))

        return tuple(path)



    def OnionizeMessage(self, _contents: bytes):
        keys = []
        path = list(self.CreateMessagePath()) # make sure to revese it
        address: AvailableConnection
        for address in path:
            # self.socket.sendto(Const.PublicKeyRequest, address.address[0])
            # received, _ = self.socket.recvfrom(Const.PublicKeySize)
            keys.append(address.address[1])
        # message = _contents + Const.LoopBackMsgID + Const.EndOfMessage     # ? + lengths?
        message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, path[-1].address[0], _contents) #----
        for i in range(len(keys)):
            payload = encrypt(message.Export(), keys[i])
            message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, path[len(path)-1-i].address[0], payload)
            print(f"message: {message}")
        
        current_id = self.GenerateMsgID()
        self.ids.update({current_id: MsgID('127.0.0.1', Const.LoopBackMsgID)})
        message.SetMsgID(current_id)
        print(f"message: {message}")
        print(f"dict: {self.ids}")
        

    def SendMessage(self, _msg: str):
        self.OnionizeMessage(_msg.encode())
        # send it steal from router

    def Replay(self, _contents: str):
        pass

    def GenerateEncryptionKeys(self):
        pass

    def populate_agents(self, _num: int):
        for i in range(_num):
            agent = AvailableConnection((f"127.0.0.{i}", i+80), 3, f"Agent-{str(i).zfill(3)}")
            self.available_agents.append(agent)

    def SendAgents(self):
        return [{"name":agent.name, "expiration": agent.expiration, "address": agent.address} for agent in self.available_agents]

"☺>^ZW⌂p127.0.0.5☺>lorem127.0.0.25☺>lorem127.0.0.4↔☺>lorem127.0.0.4♣hello"

if __name__ == '__main__':
    app = Client()
    app.populate_agents(7)
    print(app.SendAgents())
    app.OnionizeMessage('hello'.encode())
