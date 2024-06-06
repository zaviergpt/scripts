
import os
import time
import threading

class Minecraft:

    def __init__(self):
        if os.path.isfile("server.properties"):
            self.start()
        else:
            self.install()

    def install(self):
        os.system("""
clear
sudo apt install openjdk-21-jdk -y
curl -SsL https://playit-cloud.github.io/ppa/key.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/playit.gpg >/dev/null
echo "deb [signed-by=/etc/apt/trusted.gpg.d/playit.gpg] https://playit-cloud.github.io/ppa/data ./" | sudo tee /etc/apt/sources.list.d/playit-cloud.list
sudo apt update && sudo apt upgrade -y
sudo apt install playit -y
sudo update-alternatives --auto
wget https://download.oracle.com/java/21/archive/jdk-21.0.2_linux-x64_bin.deb
sudo dpkg -i jdk-21.0.2_linux-x64_bin.deb
wget https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar
java -Xmx3G -Xms3G -jar server.jar nogui
        """)
        while True:
            if os.path.isfile("server.properties"):
                break
            time.sleep(10)
        if os.path.isfile("eula.txt"):
            eula = open("eula.txt", "r").read().split("\n")
            for index, line in enumerate(eula):
                if "=" in line:
                    if line.split("=")[0] == "eula":
                        param = line.split("=")
                        param[1] = "true"
                        eula[index] = "=".join(param)
            open("eula.txt", "w").write("\n".join(eula))
        print("\nServer Installed.\nRun Script Again to Start Server.\n")

    def server(self):
        print("\n==========[ Starting Server ... ]==========\n")
        os.system("java -Xmx3G -Xms3G -jar server.jar nogui")
    
    def tunnel(self):
        while True:
            if os.path.isfile("./logs/latest.log"):
                if "Done" in open("./logs/latest.log", "r").read():
                    break
            time.sleep(5)
        os.system("clear && playit")

    def start(self):
        if os.path.isfile("./world/session.lock"):
            os.system("""sudo netstat -ntlp | awk '$4~/:*25565$/{gsub(/\/.*/,"",$NF);cmd="kill -9 "$NF;system(cmd)}'""")
            os.remove("./world/session.lock")
        os.system("clear")
        server = threading.Thread(target=self.server, args=())
        tunnel = threading.Thread(target=self.tunnel, args=())
        server.start()
        time.sleep(10)
        tunnel.start()

Minecraft()
