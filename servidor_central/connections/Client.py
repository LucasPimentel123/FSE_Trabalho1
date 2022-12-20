from time import sleep
import threading
import json
from connections.ListenConnection import ListenConnection


class Client(threading.Thread):
    states: dict
    sockets: dict

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.server = ListenConnection(host, port)
        self.server.daemon = True
        self.states = {}
        self.sockets = {}

    def send_message(self, destiny, message) -> None:
        self.sockets[destiny].send(bytes(message, encoding="utf-8"))

    def run(self) -> None:
        self.server.start()
        while True:
            self.sockets = self.server.sockets
            for board in self.sockets:
                self.send_message(board, "update")
                self.states[board] = json.loads(
                    self.sockets[board].recv(4096).decode("utf-8")
                )
            sleep(2)
