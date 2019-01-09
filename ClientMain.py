
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

while True:
    folder = None
    folder = input("enter folder name: ")
    if folder != None:
        print("folder name: " + folder)
        break

while(True):
    option = None
    print("menu:\n"
          "0 : new folder\n"
          "1 : files list\n"
          "2 : search\n"
          "3 : download\n"
          "4 : go to\n"
          "5 : up load\n"
          "6 : delete\n"
          "7 : memory\n"
          "8 : back\n"
          "9 : exit")

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
            print("0  new folder ;-)")

        if case("files list"):
            print("1  files list ;-)")

        if case("search"):
            print("2  search ;-)")

        if case("download"):
            print("3  download ;-)")

        if case("go to"):
            print("4  go to ;-)")

        if case("up load"):
            print("5  up load ;-)")

        if case("delete"):
            print("6  memory ;-)")

        if case("memory"):
            print("7  delete ;-)")

        if case("back"):
            print("8 back;-)")

        if case("exit"):
            print("9 exit")
            break

print("eoc")

