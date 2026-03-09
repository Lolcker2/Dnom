from socket import socket
from Utils.Const import Const
from Utils.Message import Message, hexify as hxfy
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from rsa import newkeys, encrypt as ncrypt, decrypt as dcrypt, PublicKey, PrivateKey
from base64 import b64decode
from random import randint


def generate_key_pair():
    public, private = newkeys(Const.PublicKeySize)
    return public.save_pkcs1(), private.save_pkcs1()

def encrypt(message, public_key):
    print(f"encryption fun {public_key}")
    # actual_key = PublicKey.load_pkcs1_openssl_der(b64decode(public_key))
    return ncrypt(message, PublicKey.load_pkcs1(public_key))

def decrypt(message, private_key):
    print(f"encryption fun2 {private_key}")
    return dcrypt(message, PrivateKey.load_pkcs1(private_key))


def GenerateMsgID() -> bytes:
    msg_id = ""
    for _ in range(Const.MsgIDLength):
        msg_id += chr(randint(*Const.AsciiRange))
    return msg_id.encode()


def send_vanilla(_msg: str) -> bytes:
    return f"{str(len(_msg)).zfill(8)}{_msg}".encode()


def receive_vanilla(_sock: socket) -> tuple:
    length, addr = _sock.recvfrom(1)[0]
    data = b''
    while b'~' not in data:
        res = _sock.recvfrom(1)[0]
        data += res
    result = _sock.recvfrom(int(data[0:-1].decode()))
    return result[0].decode(), result[1]


hexify = hxfy
dehexify = list


def ImportMessage(_msg: bytes):
    _msg = _msg.decode()
    return Message(_msg[1].encode(), _msg[2:7].encode(), '.'.join(dehexify(_msg[7:11])), _msg[11:].encode())


def receive_protocol(_sock: socket) -> Message:
    _action = _sock.recv(1)
    _msgID = _sock.recv(5)
    _nextIP = dehexify(_sock.recv(4))
    _port = int(_sock.recv(5).decode())
    _length = int.from_bytes(_sock.recv(8))
    print(f"a: {_action}, m: {_msgID}, n: {_nextIP}, l: {_length}")
    return Message(_action, _msgID, str((_nextIP, _port)), "")  # placeholder


if __name__ == '__main__':
    pass

"""
protocol

header
    action 1 byte
    msgID 5 bytes (const)
    nextIP  4 bytes
    body length 8 bytes
body
    payload
"""
