
import datetime
from Client import device
from switch import Switch as switch #import class switch from file switch
import pickle #saving object for other sessions
import dill as pickle
import os.path
import time
import glob
import shutil
import os
import ntpath
from pathlib import Path
myClient = None

while True:
    folder = ""
    ip = ""
    folder = input("enter folder name: ")
    if folder != "":
        print("folder name: " + folder)
        ip = input("enter IP: ")
        if ip != "":
            print("IP: " + ip)
            myClient = device(folder, ip)
            break


while(True):
    option = None
    print("menu:\n"
          "(0):new folder\t"
          "(1):files list\t"
          "(2):search\t"
          "(3):download\t"
          "(4):go to\t"
          "(5):up load\t"
          "(6):delete\t"
          "(7):memory\t"
          "(8):back\t"
          "(9):exit")

    option = input("enter chosen number: \n")

    if option == "0":
        option = "new folder"
    elif option == "1":
        option = "files list"
    elif option == "2":
        option = "search"
    elif option == "3":
        option = "download"
    elif option == "4":
        option = "go to"
    elif option == "5":
        option = "up load"
    elif option == "6":
        option = "delete"
    elif option == "7":
        option = "memory"
    elif option == "8":
        option = "back"
    elif option == "9":
        option = "exit"

    with switch(option) as case:
        if case("new folder"):
            myClient.sendCommand(option)

        if case("files list"):
            print(myClient.sendCommand(option))

        if case("search"):
           print(myClient.sendCommand(option))

        if case("download"):
            myClient.sendCommand(option)

        if case("go to"):
            myClient.sendCommand(option)

        if case("up load"):
            myClient.sendCommand(option)

        if case("delete"):
            myClient.sendCommand(option)

        if case("memory"):
            myClient.sendCommand(option)

        if case("back"):
            myClient.sendCommand(option)

        if case("exit"):
            myClient.sendCommand(option)
            break

print("eoc")

