from interface.Interface import Interface


def main():
    host = "164.41.98.15"
    port = 10681

    interface = Interface(host, port)
    interface.start()


if __name__ == "__main__":
    main()
