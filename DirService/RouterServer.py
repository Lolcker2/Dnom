from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from Utils.protocol import receive_protocol, ImportMessage, decrypt, GenerateMsgID
from Utils.Const import Const
from select import select
from Utils.Message import Message
from Utils.MsgID import MsgID


class RouterServer:
    def __init__(self, _host: tuple, _FetchCallback: callable, _UpdateCallback: callable, _AddCallback: callable):
        self.FetchCallback = _FetchCallback
        self.AddCallback = _AddCallback
        self.UpdateCallback = _UpdateCallback
        self.MsgID_db = dict()
        self.host = _host
        self.socket = socket()  # the server socket, using tcp
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(self.host)
        self.clients: list[socket] = [self.socket]  # a list of all currently connected clients
        self.addresses = dict()

    def forward(self, _message: Message, _address: tuple):
        self.UpdateCallback('queued_messages', [_address, _message])

    def peal(self, _msg) -> Message:
        # try with old keys, if wrong, try with new keys
        key = self.FetchCallback('private')
        decrypted_message = decrypt(_msg, key)
        return ImportMessage(decrypted_message)

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
                        self.addresses.update({_con: _adr})
                    else:   # a message from a client
                        msg = receive_protocol(client)
                        match msg.action:
                            case Const.InComingMessageSignal:
                                print(f"Hello!")
                                new_msg = self.peal(msg.payload)
                                if self.host == new_msg.nextIP:
                                    text = new_msg.payload.decode()
                                    self.UpdateCallback('chats', 'Inbox',
                                                        {"payload": text, "was_sent": 0, "id": msg.msgID})
                                else:
                                    prev_host = self.addresses[client]
                                    self.AddCallback("MsgID_db", GenerateMsgID(), MsgID(prev_host, msg.msgID))
                                    self.forward(ImportMessage(msg.payload), prev_host)

                                self.addresses.pop(client, None)
                                self.clients.remove(client)

                            case Const.DepartingMessageSignal:  # should know who sent it based on the key
                                print(f"Bye!")
                                MsgID_db = self.FetchCallback("MsgID_db")[1]
                                if msg.msgID == Const.LoopBackMsgID:
                                    pass # mine
                                elif msg.msgID in MsgID_db.keys():
                                    portalInfo: MsgID = MsgID_db[msg.msgID]
                                    new_msg = Message(msg.action, portalInfo.prevID, portalInfo.prevHost, msg.payload)
                                    self.forward(new_msg, (msg.nextIP, 5550))
                                self.addresses.pop(client, None)
                                self.clients.remove(client)

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    # app = Server()
    # app.main()
    pass
