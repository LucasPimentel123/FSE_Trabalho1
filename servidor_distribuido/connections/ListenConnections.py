import threading
import socket
import sys
from controller.ControllerSala import ControllerSala
from model.Sala import Sala
from connections.Client import Client


class ListenConnection(threading.Thread):
    def __init__(self, sala: Sala) -> None:
        super().__init__()
        self.controller_sala = ControllerSala(sala)
        self.controller_sala.daemon = True
        self.host = self.controller_sala.sala.central_address
        self.port = self.controller_sala.sala.central_port

    def create_socket(self):
        self.central_soc = socket.create_connection((self.host, self.port))
        Client().send_message(self, self.controller_sala.sala.name)
        print(f"connected to {self.host}")

    def run(self):
        self.create_socket()
        self.controller_sala.start()
        print("\naguardando conexão...")
        while True:
            request = self.central_soc.recv(1024).decode("utf-8")

            if request == "kys NOW":
                print("servidor caiu")
                sys.exit()

            elif request == "update":
                message = self.controller_sala.get_json_dump()
                Client().send_message(self, message)
                print("informação enviada")

            elif request == "L_ON":
                self.controller_sala.sala.set_high("L_01")
                self.controller_sala.sala.set_high("L_02")
                Client().send_message(self, "sucess")
                print("Todas as luzes estão ligadas")

            elif request == "L_OFF":
                self.controller_sala.sala.set_low("L_01")
                self.controller_sala.sala.set_low("L_02")
                Client().send_message(self, "sucess")
                print("Todas as luzes estão desligadas")

            elif (
                request == "AC"
                or request == "PR"
                or request == "L_01"
                or request == "L_02"
            ):
                self.controller_sala.sala.switch(request)
                Client().send_message(self, "sucess")
                print(f"{request} switched")

            elif request == "all_off":
                self.controller_sala.sala.all_off()
                Client().send_message(self, "sucess")
                print("Todas as cargas estão desligadas")

            elif request == "switch_alarm":
                if self.controller_sala.sala.alarm_on:
                    self.controller_sala.sala.alarm_on = False
                    Client().send_message(self, "sucess")
                else:
                    self.controller_sala.sala.alarm_on = True
                    Client().send_message(self, "sucess")
                    print("Alarme acionado")
