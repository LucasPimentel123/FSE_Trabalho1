class Client:
    def send_message(self, socket, message):
        socket.central_soc.send(bytes(message, encoding="utf-8"))
