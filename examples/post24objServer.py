##Test 4 integers (1-10) and
##Determine if target/24 can be an outcome after applying +,-,*,+ on these
##4 numbers (each is used one and only one time).
##Use post-order representation to avoid parentheses
##
#!/usr/bin/python3

#server
import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = "Server"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################


    ####Lee: Modify this for the project
    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})

    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()
    ####Lee:

#server

#24
import itertools

class Post24Server(Server):
    num_boxes=4
    N=['2','5','9','3']
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()  #This seems storing all players
        print('Server launched')

    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = True
        self.SendPlayers()
        print("players", [p for p in self.players])

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]
        self.SendPlayers()

    def SendPlayers(self):
        self.SendToAll({"action": "players",
                        "players": [p.nickname for p in self.players]})

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = Post24Server(localaddr=(host, int(port)))
    s.Launch()
