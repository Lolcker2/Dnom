from flask import Flask, request
from flask_cors import CORS 
from json import dumps
from Client import Client
from Utils.Message import Message
from Utils.MsgID import MsgID
from Utils.Const import Const
from Utils.protocol import encrypt, GenerateMsgID
from Utils.AvailableConnection import AvailableConnection
from random import choice

cors = CORS()
app = Flask(__name__)


cors.init_app(app)
FetchCallback: callable
UpdateCallback: callable
AppendCallback: callable
AddCallback: callable

def Main(_FetchCallback: callable, _UpdateCallback: callable, _AppendCallback: callable, _AddCallback: callable):
    global FetchCallback, UpdateCallback, AppendCallback, AddCallback
    FetchCallback = _FetchCallback
    UpdateCallback = _UpdateCallback
    AppendCallback = _AppendCallback
    AddCallback = _AddCallback
    app.run(debug=True)

@app.route("/connect", methods=["GET"], strict_slashes=False)
def Name() -> str:
    name = request.args.get("name")
    print(f"name: {name}")
    UpdateCallback('name', name)
    print(f"result of update: {FetchCallback('name')}")
    return dumps({"status": "200 ok"})

@app.route("/chat", methods=["GET"], strict_slashes=False)
def GetChat() -> str:
    address = request.args.get("addr")
    chats = FetchCallback('chats')[1]
    print(f"address: {address}, chats: {chats}")
    try: 
        return dumps({"data": chats[address]})
    except KeyError:
        return dumps({"data": []})  # length 0

def CreateMessagePath() -> list[AvailableConnection]:
    available_agents = FetchCallback("available_agents")[1]
    path_length = min(Const.MessagePathLength, len(available_agents))
    path = [choice(list(available_agents)) for _ in range(path_length)]
    while len(set(path)) < path_length:
        path.append(choice(list(available_agents)))

    return list(set(path))

def OnionizeMessage(_contents: bytes, _address: tuple):
    path = CreateMessagePath()
    prev_address = _address
    message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, str(_address), _contents)  # ----
    for agent in path:
        print("hey")
        payload = encrypt(message.Export(), agent.public_key)
        print("hey2")
        message = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, str(prev_address), payload)
        prev_address = agent.address    # should include port

    current_id = GenerateMsgID()
    AddCallback('MsgID_db', current_id, MsgID('127.0.0.1', Const.LoopBackMsgID))
    AddCallback('chats', str(_address), {"payload": _contents.decode(), "was_sent": 1, "id": current_id})
    message.SetMsgID(current_id)
    return message, _address


@app.route("/send", methods=["GET"], strict_slashes=False)
def SendMsg() -> str:
    address = request.args.get("addr").split(',')
    address_tuple = (address[0], int(address[1]))
    message = request.args.get("msg")
    print(f"text of message: {message}")
    true_message = OnionizeMessage(message.encode(), address_tuple)
    print(f"msg: {true_message}")
    # print(f"msg: {message}, addr: {address_tuple}")
    # m_s_g = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, '127.0.0.1', message.encode())

    AppendCallback('queued_messages', [address_tuple, true_message])
    return dumps({"status": "200 ok"})


@app.route("/replay", methods=["GET"], strict_slashes=False)
def ReplayMsg() -> str:
    msg_id = FetchCallback('MsgID_db')[1][request.args.get("id")]   # prev_host, prev_id
    message = request.args.get("msg")

    # print(f"msg: {message}, addr: {address_tuple}")
    # m_s_g = Message(Const.InComingMessageSignal, Const.LoopBackMsgID, '127.0.0.1', message.encode())
    # AppendCallback('queued_messages', [address_tuple, m_s_g])
    return dumps({"status": "200 ok"})


@app.route("/dirservice", methods=["GET"], strict_slashes=False)
def DirService() -> str:
    available_agents = FetchCallback("available_agents")[1]
    data = [{"name": agent.name, "expiration": agent.expiration, "address": agent.address} for agent in available_agents]
    data.append({"name": "Inbox", "expiration": 3, "address": "Inbox"})
    print(f"data: {data}")
    return dumps({"data": data})



