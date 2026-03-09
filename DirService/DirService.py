from socket import SOCK_DGRAM, socket, AF_INET, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR
from time import sleep
from Utils.Const import Const
from Utils.AvailableConnection import AvailableConnection
from json import dumps
from Utils.Message import Message
from Utils.protocol import receive_vanilla


class DirService:
    def __init__(self, _FetchCallback: callable, _UpdateCallback: callable, _ap: callable):
        self.FetchCallback = _FetchCallback
        self.ap = _ap
        self.UpdateCallback = _UpdateCallback
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)  # the server socket, using udp
        self.socket.settimeout(Const.SocketTimeOut)     # setting the timeout of the socket
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)     # setting the socket to broadcast mode
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    @staticmethod
    def recv_vanilla_broadcast(_sock: socket):  # add to protocol
        length, address = _sock.recvfrom(8)
        length = int(length.decode())
        print(f"length: {length}")
        return _sock.recvfrom(length)[0].decode(), address

    def Main(self):
        try:
            while 1:
                self.Broadcast()  # broadcast
                sleep(Const.BroadCastFreq)  # wait <BroadCastFreq> seconds

        except KeyboardInterrupt:
            pass

    # returns the output for the DirService service
    def Output(self):
        available_agents = self.FetchCallback("available_agents")[1]
        formatted_list = [agent.address for agent in available_agents]
        return dumps({"host": 'DirServiceIpAddress', "agents": formatted_list})

    # given an address, checks if it's in the agent list, if so, returns its index
    # return: (bool, int) -> (did work, index)
    @staticmethod
    def LookupAvailableAgents(_addr: tuple, _available_agents: list[AvailableConnection]) -> tuple:
        for i in range(len(_available_agents)):
            if _addr == _available_agents[i].address:
                return True, i
        return False, None

    # the main method, broadcasts a message, gets a response, and updates the agent list
    def Broadcast(self):
        self.socket.sendto(Const.BroadCastEntry, ('<broadcast>', Const.DefaultPort))   # broadcast the 'BroadCastEntry' char
        available_agents = self.FetchCallback("available_agents")[1]
        try:
            # message, _address = self.socket.recvfrom(1)     # receive a bit (1 bit long message)
            message, _address = self.recv_vanilla_broadcast(self.socket)
            print(f"mseesk: {message}")
            name, public_key = message[1:].split(',')
            print(f"name: {name}, key: {public_key}")
            if message[0] == Const.BroadCastResponse.decode():      # if received a 'BroadCastResponse' char
                is_in, index = self.LookupAvailableAgents(_address, available_agents)   # is the current agent already in the list
                if is_in:   # if it is, increase its expiration by 1
                    available_agents[index].expiration += 1
                    if len(name) > 1:
                        available_agents[index].name = name
                    if len(public_key) > 1:
                        available_agents[index].public_key = public_key
                else:
                    available_agents.append(AvailableConnection(_address, 3, name, public_key))  # new client, default expiration is 3
                    self.UpdateCallback("available_agents", available_agents)
                # print(f"agents: {available_agents}")

        except TimeoutError:
            pass

        finally:
            for i in range(len(available_agents)):
                agent = available_agents[i]
                if agent.expiration == 0:   # if agent expired, remove it from the list
                    available_agents.remove(agent)
                    self.UpdateCallback("available_agents", available_agents)
                    continue

                available_agents[i].expiration -= 1    # if agent not expired, decrease its expiration by 1
            # print(f"agents: {available_agents}")


if __name__ == '__main__':
    # app = DirService()
    # app.Main()
    pass
