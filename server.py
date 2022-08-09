import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"  # fixed ip addr and port number for sever - localhost
port = 9999  # regstered/privileged ports<1024 - already in use

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, tcp socket is assigned for server

try:
    s.bind((server, port))
except socket.error as e:  # if port 5555 is being used elsewhere
    str(e)

s.listen()  # listening to client requesting for connections - unlimited connections
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))              # go to network.py

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()  # 4096 buts of information at a time

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data == "score":
                        print("no problem")
                        print("game.done_bat[0] = ", game.done_bat[0], "and game.done_bat[1] =", game.done_bat[1])
                        if game.done_bat[0] == 1 and game.bothWent():
                            print("2nd player as batsman")
                            game.score[1] = game.batsman(1, 0, game.score[1])
                            print("completed1")
                        elif game.bothWent():
                            print("1nd player as batsman")
                            game.score[0] = game.batsman(0, 1, game.score[0])
                            print("completed2")
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:                                     # loop to add multiple clients to games till server terminated
    conn, addr = s.accept()                     # go to network.py -> connect.py -> client socket accepted here
    print("Connected to:", addr)                # accepting connection, and adding multiple clients
    idCount += 1                                # idCount = total number of active players
    p = 0
    gameId = (idCount - 1) // 2                 # 1 game -> 2 clients
    print(idCount)
    if idCount % 2 == 1:                        # multiple clients in odd number. one has to wait
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        print("2nd connected")                  # 2 clients have started playing
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))      # start new thread for each client
