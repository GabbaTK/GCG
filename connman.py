import socket

class DoubleSocketTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)

class NoSocketTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)

class WrongSocketTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)

class NoConnectionException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Socket:
    def __init__(self, client=False, server=False):
        self.format = "utf-8"
        self.header = 512
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = client
        self.server = server

        if not client and not server:
            raise NoSocketTypeException("The socket has to be set to either a client or a server, not none.")
        if client and server:
            raise DoubleSocketTypeException("The socket cannot be set to both client and server.")
        
    def createServer(self, port, overrideIp=None):
        if self.client: raise WrongSocketTypeException("The socket is set to be a client, the socket has to be a server for this function to run.")

        #ip = socket.gethostbyname(socket.gethostname())
        ip = "0.0.0.0"
        if overrideIp: ip = overrideIp
        self.socket.bind((ip, port))
        self.socket.listen()

    def acceptConnection(self):
        if self.client: raise WrongSocketTypeException("The socket is set to be a client, the socket has to be a server for this function to run.")

        # connection (address, port)
        return self.socket.accept()
    
    def connect(self, ip, port, timeout):
        if self.server: raise WrongSocketTypeException("The socket is set to be a server, the socket has to be a client for this function to run.")

        # If ip is a local computer name
        ip = socket.gethostbyname(ip)
        addr = (ip, port)

        try:
            self.socket.settimeout(timeout)
            self.socket.connect(addr)
            self.socket.settimeout(None)

            return True
        except:
            return False
        
    def send(self, msg, connection=None):
        if self.server:
            if connection == None: raise NoConnectionException("The connection variable is None.")

            try:
                msg = msg.encode(self.format)
                msgLength = str(len(msg)).encode(self.format) + b"\x00" * (self.header - (len(str(len(msg)).encode(self.format))))
                connection.send(msgLength)
                connection.send(msg)

                return True
            except:
                return False
        else:
            try:
                msg = msg.encode(self.format)
                msgLength = str(len(msg)).encode(self.format) + b"\x00" * (self.header - (len(str(len(msg)).encode(self.format))))
                self.socket.send(msgLength)
                self.socket.send(msg)

                return True
            except:
                return False

            
    def receive(self, timeout, connection=None):
        if self.server:
            if connection == None: raise NoConnectionException("The connection variable is None.")

            try:
                connection.settimeout(timeout)
                length = connection.recv(self.header).decode(self.format)
                length = str(length).replace("\x00", "")
                data = connection.recv(int(length)).decode(self.format)
                connection.settimeout(None)

                return data
            except:
                return None
        else:
            try:
                self.socket.settimeout(timeout)
                legnth = self.socket.recv(self.header).decode(self.format)
                legnth = str(legnth).replace('\x00', '')
                data = self.socket.recv(int(legnth)).decode(self.format)
                self.socket.settimeout(None)

                return data
            except:
                return None
            
    def disconnect(self, connection=None):
        if self.server:
            if connection == None: raise NoConnectionException("The connection variable is None.")

            connection.close()
        else:
            self.socket.shutdown(socket.SHUT_RDWR)

    def sync(self, connection=None):
        if self.server:
            if connection == None: raise NoConnectionException("The connection variable is None.")

            self.send("SYNC", connection)
            self.receive(None, connection)
        else:
            self.send("SYNC")
            self.receive(None)
