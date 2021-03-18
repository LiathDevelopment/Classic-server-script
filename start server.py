from subprocess import PIPE
import subprocess
import threading
import schedule
import datetime
import shutil
import os

start_cmd = 'cmd /c java -Xms512M -Xmx512M -Dhttp.proxyHost=betacraft.pl -cp minecraft-server.jar com.mojang.minecraft.server.MinecraftServer'

def logger(string):
    print("     " + getTimeString() + "  " + string)

def getTimeString():
    nowHour = datetime.datetime.now().hour
    nowMinute = datetime.datetime.now().minute
    nowSecond = datetime.datetime.now().second
    if len(str(nowHour)) == 1:
        nowHour = "0"+str(nowHour)
    if len(str(nowMinute)) == 1:
        nowMinute = "0"+str(nowMinute)
    if len(str(nowSecond)) == 1:
        nowSecond = "0"+str(nowSecond)
    return str(nowHour)+":"+str(nowMinute)+":"+str(nowSecond)

def createBackup():
    now = str(datetime.datetime.now())[:19]
    now = now.replace(":","-")
    now = now.replace(" ", "_")

    src_dir="server_level.dat"
    dst_dir=".\\backups\\server_level_backup_"+str(now)+".dat"
    shutil.copy(src_dir,dst_dir)
    logger("Server backup created")

def autoBackupThread():
    i = 1
    threading.Timer(i, autoBackupThread).start()
    schedule.run_pending()

os.system('title Classic Revived 0.0.18a_02 Server')
process = subprocess.Popen(start_cmd,stdin=PIPE,stdout=PIPE)
schedule.every(6).hours.do(createBackup)
autoBackupThread()

while process.poll() is None:
        output = process.stdout.readline()
        print(output)
