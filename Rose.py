# borrows class client, and overwrites the specifics

from Utils.Const import Const
from Utils.protocol import encrypt, receive_vanilla
from random import choice
from socket import socket
from Client import Client


class Rose(Client):
    def GetDirService(self):
        self.socket.connect(('127.0.0.1', 5555))
        self.socket.send(Const.DirServiceEntry)
        self.available_agents = receive_vanilla(self.socket)[0]

    def LoadImmediateContacts(self):
        pass

