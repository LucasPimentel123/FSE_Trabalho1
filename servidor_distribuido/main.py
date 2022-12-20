from model.Sala import Sala
from connections.ListenConnections import ListenConnection
import sys


def main():
    json = sys.argv[1]
    server = ListenConnection(Sala(json))
    server.start()


if __name__ == "__main__":
    main()
