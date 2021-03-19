from subprocess import PIPE, Popen
from datetime import datetime
from threading import Timer
from shutil import copy
from os import system
import schedule

start_cmd = "java -Xms512M -Xmx512M -Dhttp.proxyHost=betacraft.pl -cp minecraft-server.jar com.mojang.minecraft.server.MinecraftServer"
server_config = {}


def logger(string):
    now_hour = datetime.now().hour
    now_minute = datetime.now().minute
    now_second = datetime.now().second
    if len(str(now_hour)) == 1: now_hour = "0" + str(now_hour)
    if len(str(now_minute)) == 1: now_minute = "0" + str(now_minute)
    if len(str(now_second)) == 1: now_second = "0" + str(now_second)
    time = str(now_hour) + ":" + str(now_minute) + ":" + str(now_second)

    print("     " + time + "  " + string)


def getServerConfig():
    with open('server.properties') as f:
        for line in f:
            if "=" in line:
                name, value = line.split("=", 1)
                server_config[name.strip()] = value.strip()


def createBackup():
    now = str(datetime.now())[:19]
    now = now.replace(":", "-")
    now = now.replace(" ", "_")

    copy("server_level.dat", ".\\backups\\server_level_backup_" + str(now) + ".dat")
    logger("Level backup created")


def autoBackupThread():
    i = 1
    Timer(i, autoBackupThread).start()
    schedule.run_pending()


def serverConsoleThread():
    i = 1
    Timer(i, serverConsoleThread).start()
    while process.poll() is None:
        server_output = process.stdout.readline()
        print(server_output)


getServerConfig()
system("title Classic Revived 0.0.18a_02 - Server Port: " + server_config["port"])
process = Popen("cmd /c " + start_cmd, stdin=PIPE, stdout=PIPE)
schedule.every(6).hours.do(createBackup)
# schedule.every(15).seconds.do(createBackup)
logger("Scheduling backups")
autoBackupThread()
createBackup()
