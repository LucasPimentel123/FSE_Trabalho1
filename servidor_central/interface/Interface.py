import threading
import json
import os
import sys
from datetime import datetime
import interface.Constants as Constants
from connections.Client import Client
from controller.Controller_Sala import Controller_Sala
from controller.Controller_Lampada import Controller_Lampada
import socket


class Interface(threading.Thread):
    sockets: dict
    alarme: bool
    contador: int

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.st = Client(host, port)
        self.st.daemon = True
        self.alarme = False
        self.sockets = {}
        self.contador = 0

    def controla_lampada(self, board) -> str:
        return Controller_Lampada().controla_lampadas(self, board)

    def controla_sala(self, board) -> None:
        Controller_Sala().controla_sala(self, board)

    def print_dict(self, dic: dict) -> None:
        print()
        for item in dic:
            if item == "Placa":
                print(f"{item}: \t\t{dic[item]}")
            else:
                print(f"{item}: \t{dic[item]}")

    def print_boards(self, sockets) -> None:
        print(Constants.SALAS)
        for board in sockets:
            print(board)
        print(Constants.CONTROLE)

    def fecha(self) -> None:
        os.system("clear")

    def atualiza_estados(self, board) -> None:
        self.request(board, "update")
        self.st.states[board] = json.loads(
            self.sockets[board].recv(4096).decode("utf-8")
        )

    def verifica_sensores(self, board) -> bool:
        dic = self.st.states[board]

        if (
            dic["S. Presença"] == "Ligado"
            or dic["S. Fumaça"] == "Ligado"
            or dic["S. Janela"] == "Ligado"
            or dic["S. Porta"] == "Ligado"
        ):
            return True
        else:
            return False

    def print_contador_pessoas(self, sockets) -> None:
        self.contador = 0
        for board in sockets:
            self.contador += int(self.st.states[board]["Pessoas"])
        print(f"Qtd de pessoas no prédio: {self.contador}\n")

    def registra_log(self, event: str) -> None:
        with open("registro_log.csv", "a", encoding="UTF8") as f:
            f.write(f'{event},{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')

    def request(self, destiny, message) -> None:
        self.sockets[destiny].send(bytes(message, encoding="utf-8"))

    def response(self, board) -> str:
        response = self.sockets[board].recv(4096).decode("utf-8")
        print(response)
        return response

    def run(self):
        self.st.start()
        log = f"central,servidor iniciado"
        self.registra_log(log)
        self.fecha()
        while True:
            self.sockets = self.st.sockets
            if self.sockets:
                for board in self.sockets:
                    self.atualiza_estados(board)

                self.print_boards(self.sockets)
                if self.alarme:
                    print("Alarme: Ligado")
                else:
                    print("Alarme: Desligado")
                self.print_contador_pessoas(self.sockets)

                choice = input()

                if choice == "0":
                    for board in self.sockets:
                        self.request(board, "kys NOW")
                    log = f"central,servidor terminado"
                    self.registra_log(log)
                    sys.exit()
                elif choice == "1":
                    for board in self.sockets:
                        if self.verifica_sensores(board):
                            self.fecha()
                            print("há sensores ativos, alarme não pode ser acionado")
                        else:
                            self.request(board, "switch_alarm")
                            self.fecha()
                            self.response(board)
                    if self.st.states:
                        if self.alarme:
                            self.alarme = False
                            log = f"central,sistema de alarme desligado"
                            self.registra_log(log)
                        else:
                            self.alarme = True
                            log = f"central,sistema de alarme ligado"
                            self.registra_log(log)
                elif choice == "2":  # all lights on
                    for board in self.sockets:
                        self.request(board, "L_ON")
                        self.fecha()
                        self.response(board)
                        log = f"{board},luzes acionadas"
                        self.registra_log(log)
                elif choice == "3":  # all charges off
                    for board in self.sockets:
                        self.request(board, "all_off")
                        self.fecha()
                        self.response(board)
                        log = f"{board},cargas desligadas"
                        self.registra_log(log)
                else:
                    self.fecha()
                    for board in self.sockets:
                        if choice == board:
                            self.controla_sala(board)
