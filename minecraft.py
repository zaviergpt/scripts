
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
curl -SsL https://playit-cloud.github.io/ppa/key.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/playit.gpg >/dev/null
echo "deb [signed-by=/etc/apt/trusted.gpg.d/playit.gpg] https://playit-cloud.github.io/ppa/data ./" | sudo tee /etc/apt/sources.list.d/playit-cloud.list
sudo apt update
sudo apt install playit -y
sudo update-alternatives --auto
sudo apt install openjdk-21-jre-headless -y
wget https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar
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
