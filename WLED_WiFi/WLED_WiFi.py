import lightpack, socket, configparser, os
from time import sleep
import sys

class WLED_WiFi:
    def __init__(self):
        self.loadConfig()
        self.lp = lightpack.Lightpack()
        self.status = False
        try:
            self.lp.connect()
        except lightpack.CannotConnectError as e:
            print(repr(e))
            sys.exit(1)
    
    def loadConfig(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.config = configparser.ConfigParser()
        self.config.read(self.scriptDir + '/WLED_WiFi.ini')
        self.fps = self.config.getint('WLED', 'FPS')
        self.udpBroadcastIp = self.config.get('WLED', 'UDP_IP_ADDRESS')
        self.udpPort = self.config.getint('WLED', 'UDP_PORT_NO')
        self.originnumled = self.config.getint('WLED', 'ORIGINNUMLED')
        self.numled = self.config.getint('WLED', 'NUMLED')

    def run(self):
        counter = 0
        leddiff=abs(self.numled-self.originnumled)
        half = int(round(self.originnumled/2))
        while(True):
            d = self.lp.getColoursFromAll()
            v = [2, 2]
            for i in d:
                v.append(d[i][0])
                v.append(d[i][1])
                v.append(d[i][2])
                if (counter % 2) == 0:
                    v.append(d[i][0])
                    v.append(d[i][1])
                    v.append(d[i][2])
                if (counter % 9) == 0:
                    v.append(d[i][0])
                    v.append(d[i][1])
                    v.append(d[i][2])
                counter = counter + 1
                """if counter == (half):
                    for x in range(int(leddiff/2)):
                        v.append(d[i][0])
                        v.append(d[i][1])
                        v.append(d[i][2])
                        counter = counter + 1
                else:
                    counter = counter + 1
                """
                if counter == (self.numled-1):
                        counter = 0
            Message = bytes(v)
            clientSock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
            clientSock.sendto (Message, (self.udpBroadcastIp, self.udpPort))
            sleep(1/self.fps)

warls = WLED_WiFi()
warls.run()
