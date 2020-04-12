import socket
import time


class ClientError(Exception):
    """
    User Exception class ClientError would raise when
    problems with connection to server, putting and getting data from it
    are detected
    """
    pass


class Client:
    """
    Client that send different metrics to server.
    It has incapsulated connection with server, creating client socket,
    and put and get methods.
    """
    def __init__(self, host, port, timeout=None):
        # constuctor takes adress (host, port) that we need to make connection
        # with and optional timeout argument
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout) # noqa
        except socket.error as err:
            raise ClientError("error creatig connection", err)

    def _read(self):
        # method that reads response from server and
        # split it by response status and response itself
        data = b""

        while not data.endswith(b'\n\n'):
            try:
                # getting data from server socket
                data += self.sock.recv(1024)
            except socket.error as err:
                raise ClientError("failed reading data from server", err)

        data = data.decode()

        status, response = data.split('\n', 1)
        response = str(response)
        response = response.strip()

        if status == "error":
            raise ClientError("error with getting data. Check your inquiry")

        return response, status

    def put(self, metric, value, timestamp=None):
        # Client method that takes metric name, its value and timestamp
        # and tries to put it to the server
        timestamp = timestamp or int(time.time())
        try:
            self.sock.sendall(
                f"put {metric} {value} {timestamp}\n".encode()
            )
        except socket.error as err:
            raise ClientError("error putting the data", err)

        self._read()

    def get(self, metric):
        # Client method that takes metric name as argument and return
        # all data about this metric from server. Can get * as argument and
        # return all data found in server.
        try:
            self.sock.sendall(
                f"get {metric}\n".encode()
            )
        except socket.error as err:
            raise ClientError("error getting the data", err)

        response, status = self._read()

        if status != "ok":
            raise ClientError(status)

        data = {}

        if response == "":
            return data

        for line in response.split("\n"):
            words = line.split()
            if len(words) != 3:
                raise ClientError
            metric, value, timestamp = words[0], words[1], words[2]
            if metric not in data:
                data[metric] = []
            data[metric].append((int(timestamp), float(value)))
            data[metric].sort(key=lambda lin: lin[0])
        return data
