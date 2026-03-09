from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from Utils.protocol import receive_protocol, encrypt, GenerateMsgID
from Utils.Const import Const
from select import select
from Utils.Message import Message
from Utils.MsgID import MsgID
from random import choice
from Utils.AvailableConnection import AvailableConnection


class RoutingClient:
    def __init__(self, _FetchCallback: callable, _UpdateCallback: callable, _RmvCallback: callable):
        self.FetchCallback = _FetchCallback
        self.UpdateCallback = _UpdateCallback
        self.RemoveCallback = _RmvCallback
        self.socket = socket()
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # queued_messages holds [address, message] objects

    def send(self, _queued_element: list): # forward message (will also be used to send the initial message)
        print(f"elem: {_queued_element}")
        self.socket.connect(_queued_element[0])
        sending = _queued_element[1].Export()
        print(f"sending: {sending}")
        self.socket.send(sending)

    def CreateMessagePath(self) -> list[AvailableConnection]:
        available_agents = self.FetchCallback("available_agents")[1]
        path_length = min(Const.MessagePathLength, len(available_agents))
        path = [choice(list(available_agents)) for _ in range(path_length)]
        while len(set(path)) < path_length:
            path.append(choice(list(available_agents)))

        return list(set(path))

    def OnionizeMessage(self, _contents: bytes, _address: str):
        path = self.CreateMessagePath()
        prev_address = _address
        message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, _address, _contents)  # ----
        for agent in path:
            payload = encrypt(message.Export(), agent.public_key)
            message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, prev_address, payload)
            prev_address = agent.address    # should include port

        current_id = GenerateMsgID()
        self.UpdateCallback('MsgID_db', current_id, MsgID('127.0.0.1', Const.LoopBackMsgID))
        self.UpdateCallback('chats', str(_address), {"payload": _contents.decode(), "was_sent": 1, "id": current_id})
        message.SetMsgID(current_id)
        self.send([_address, message])  # problematic cuz _address is a string and not a tuple

    def CheckNSend(self):
        queued_messages = self.FetchCallback("queued_messages")[1]  # make sure there is a message to
        for msg in queued_messages:
            print(f"sending {msg}")
            self.send(msg)
        self.RemoveCallback('queued_messages', queued_messages)

    def Main(self):
        while 1:
            self.CheckNSend()
