class Const:
    # Broadcast consts
    BroadCastEntry = chr(7).encode()   # bell
    BroadCastResponse = chr(64).encode()    # @

    # Tcp protocol
    DisconnectSignal = chr(68).encode()    # D
    InComingMessageSignal = chr(62).encode()   # >
    DepartingMessageSignal = chr(60).encode()   # <
    DirServiceEntry = chr(63).encode()  # ?
    DirServiceResponse = chr(65).encode()  # !

    # Misc
    MsgIDLength = 5
    LoopBackMsgID = 'lorem'.encode()    # takes 5 letters
    AsciiRange = (30, 141)
    MaxMsgLength = 8    # bytes
    SocketTimeOut = 0.5     # sec
    DefaultPort = 12000
    BroadCastFreq = 0.5  # seconds
    MaxConcurrentClients = 5
    MessagePathLength = 3
    PublicKeySize = 1024
    CorrectDecryptionChar = chr(38).encode()  # Start of Heading 1
    
    def LoadSettings(self):
        pass
