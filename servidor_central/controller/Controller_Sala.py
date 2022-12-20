import interface.Constants as Constants


class Controller_Sala:
    def controla_sala(self, interfaceThread, board):
        while True:
            interfaceThread.print_dict(interfaceThread.st.states[board])
            choice = input(Constants.CONTROLE_SALA)

            if choice == "0":
                interfaceThread.fecha()
                return
            elif choice == "1":
                msg = interfaceThread.controla_lampada(board)
            elif choice == "2":
                msg = "AC"
                log = f"{board},{msg} acionado"
                interfaceThread.registra_log(log)
            elif choice == "3":
                msg = "PR"
                log = f"{board},{msg} acionado"
                interfaceThread.registra_log(log)
            elif choice == "4":
                msg = "all_off"
                log = f"{board},tudo desligado"
                interfaceThread.registra_log(log)
            if choice == "":
                interfaceThread.fecha()
            else:
                interfaceThread.request(board, msg)
                interfaceThread.fecha()
                interfaceThread.response(board)
                interfaceThread.atualiza_estados(board)
