from time import sleep, time
import threading
import json
import RPi.GPIO as GPIO
from model.Sala import Sala


class ControllerSala(threading.Thread):
    pressionou: bool
    cronometro: float

    def __init__(self, sala: Sala) -> None:
        super().__init__()
        self.sala = sala

    def liga_luzes(self):
        self.sala.set_high("L_01")
        self.sala.set_high("L_02")
        self.cronometro = time()
        self.pressionou = True

    def liga_luzes_por_tempo(self):
        if time() - self.cronometro > 15.0:
            self.sala.set_low("L_01")
            self.sala.set_low("L_02")
            self.cronometro = None
            self.pressionou = False

    def get_atual(self) -> dict:
        dic = {}

        for item in self.sala.states:
            if item == "L_01":
                dic["Lâmpada 01"] = self.sala.states["L_01"]
            elif item == "L_02":
                dic["Lâmpada 02"] = self.sala.states["L_02"]
            elif item == "PR":
                dic["Projetor"] = self.sala.states["PR"]
            elif item == "AC":
                dic["Ar-Con"] = self.sala.states["AC"]
            elif item == "AL_BZ":
                dic["Sirene"] = self.sala.states["AL_BZ"]
        return dic

    def verifica_sensores(self) -> bool:
        for sensor in self.sala.sensors:
            if GPIO.input(self.sala.inp[sensor]):
                return True

    def get_sensores(self) -> dict:
        dic = {}

        for sensor in self.sala.sensors:
            if sensor == "SPres":
                name = "S. Presença"
            elif sensor == "SFum":
                name = "S. Fumaça"
            elif sensor == "SJan":
                name = "S. Janela"
            elif sensor == "SPor":
                name = "S. Porta"

            if GPIO.input(self.sala.inp[sensor]):
                dic[name] = "Ligado"
            else:
                dic[name] = "Desligado"
        return dic

    def get_qtde_pessoas(self) -> dict:
        dic = {"Pessoas": self.sala.ppl_qty}
        return dic

    def get_temperatura_humdidade(self) -> dict:
        dic = {
            "Temperatura": f"{self.sala.temp} ºC",
            "Umidade": f"{self.sala.humd}%",
        }
        return dic

    def get_json_dump(self) -> str:
        dic = {"Placa": self.sala.name}
        dic = (
            dic
            | self.get_atual()
            | self.get_sensores()
            | self.get_qtde_pessoas()
            | self.get_temperatura_humdidade()
        )
        return json.dumps(dic)

    def run(self):
        self.pressionou = False
        self.cronometro = 0

        while True:
            self.sala.count_ppl()
            self.sala.check_temp()
            if self.verifica_sensores():
                if self.sala.alarm_on:
                    self.sala.set_high("AL_BZ")
                else:
                    if GPIO.input(self.sala.inp["SPres"]):
                        self.liga_luzes()

                    if GPIO.input(self.sala.inp["SFum"]):
                        self.sala.set_high("AL_BZ")

            elif self.sala.states["AL_BZ"]:
                self.sala.set_low("AL_BZ")

            if self.pressionou:
                self.liga_luzes_por_tempo()
            sleep(0.1)
