import interface.Constants as Constants


class Controller_Lampada:
    def controla_lampadas(self, interfaceThread, board):
        interfaceThread.fecha()
        interfaceThread.print_dict(interfaceThread.st.states[board])
        choice = input(Constants.LAMPADAS)

        if choice == "0":
            return ""
        elif choice == "1":
            msg = "L_01"
            log = f"{board},{msg} acionado"
            interfaceThread.registra_log(log)
            return msg
        elif choice == "2":
            msg = "L_02"
            log = f"{board},{msg} acionado"
            interfaceThread.registra_log(log)
            return msg
        elif choice == "3":
            msg = "L_ON"
            log = f"{board},lampadas ligadas"
            interfaceThread.registra_log(log)
            return msg
        elif choice == "4":
            msg = "L_OFF"
            log = f"{board},lampadas desligadas"
            interfaceThread.registra_log(log)
            return msg
