#!/usr/bin/python
# -*- coding: utf-8 -*-
# interface

import datetime
import glob
from abc import ABC, abstractmethod
import pickle  # saving object for other sessions
from time import sleep
import dill as pickle
import socket
import os
import time
from pathlib import Path
from switch import Switch as switch

#flags
FAILED = b'00'
SUCCCESS = b'01'
LOGGED = b'11'

#incoming buffer
MAX_BUFFER = 4096

class device(ABC):

    # device constructor
    def __init__(self,  ID, IP):
        self.ID = ID
        self.masterIP = IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((self.masterIP, 5000))
                break
            except:
                print("Failed to connect, auto try again after 10sec")
                time.sleep(10)
                continue
        self.sendName(self.ID)
        x = self.respond()
        print(x)
        if x[1] == b'01':
            self.sock.sendall(bin(int(input("hello new user, enter folder capacity: ")))[2:].zfill(16).encode('utf8'))
            x = self.respond()
        if x[1] == b'11':
            print("user connected")


    def save(self, path):
        with open(path, 'wb') as f:
            return pickle.dump(self, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.__dict__.update(pickle.load(f).__dict__)

    def printDetails(self):
        print("ID:", self.ID)

    # path to folder fo files to get
    def getDataFromInputFolder(self, path):
        # print("Searching for files in input directory...")
        files = glob.glob(path + "/*.*")  # create list of files in directory
        try:
            while not files:
                sleep(10)
                files = glob.glob(path + "/*.*")
            else:  # then list (actually the directory) isn't empty
                # print("File detected!") #todo Filedetected message is duplicate because its also says it in the standby mode.
                return (files)
        except KeyboardInterrupt:
            print("Exit Stand By mode")
            pass


    def respond(self):
        size = 0
        buffer = ""
        a = self.sock.recv(2)
        if a == FAILED:
            self.sock.recv(2)
            size = self.sock.recv(16)
            size = int(size.decode('utf8'))
            buffer += self.sock.recv(size).decode('utf8')
            return (False,buffer)
        elif a == SUCCCESS or a == LOGGED:
            return (True,a)
        else:
            print (a)
            return (False,"something went wrong")

    def sendCommand(self, option):
        with switch(option) as case:
            if case("new folder"):
                self.sock.sendall(b'0000')
                self.sendName()
                self.respond()

            if case("files list"):
                self.sock.sendall(b'0001')
                self.respond()
                return self.resiveData(0)

            if case("search"):
                self.sock.sendall(b'0010')
                self.sendName()
                x = self.respond()
                if not x[0]:
                    return x[1]
                return self.resiveData(0)

            if case("download"):
                self.sock.sendall(b'0011')
                file = input("enter folder full path:")
                self.sendName(file)
                x = self.respond()
                if x[0]:
                    self.resiveData(1,file)
                else:
                    return x[1]

            if case("go to"):
                self.sock.sendall(b'0100')
                self.sendName()
                return self.respond()[1]

            if case("up load"):
                self.sock.sendall(b'0101')
                for file in os.listdir('sendFiles'):
                    self.sendName(file)
                    with open("sendFiles/"+file, 'rb') as f:
                        x = f.read()
                        self.sock.sendall(bin(len(x))[2:].encode('utf8').zfill(32))
                        y = self.respond()
                        if y[0]:
                            self.sock.sendall(x)
                            self.respond()
                        else:
                            return y[1]
                self.sendName('')

            if case("delete"):
                self.sock.sendall(b'0110')
                self.sendName()
                return self.respond()[1]

            if case("memory"):
                self.sock.sendall(b'0111')
                self.respond()
                return self.resiveData(0)

            if case("back"):
            	self.sock.sendall(b'1000')
            	x = self.respond()
            	if not x[0]:
            	     return x[1]

            if case("exit"):
                self.sock.sendall(b'1001')
                self.sock.close()

    def sendName(self, arg = None):
        if arg == None:
            arg = input("enter folder full path:")
        size = bin(len(arg))[2:].zfill(16).encode('utf8')
        print(size,type(size))
        self.sock.sendall(size)
        self.sock.sendall(arg.encode('utf8'))

    def resiveData(self, type ,data = None):       #type 0 - encode, type 1 - file
        buffer = ''
        if type:
            size = int(self.sock.recv(16).decode('utf8'))
            left = size

            with open("Received/" + data, 'wb+') as f:
                while left > 0:
                    if left < MAX_BUFFER:
                        f.write(self.sock.recv(left))
                    else:
                        f.write(self.sock.recv(MAX_BUFFER))
                    left -= MAX_BUFFER

        else:
            size = self.sock.recv(16).decode('utf8')
            size = int(size)
            buffer += self.sock.recv(size).decode('utf8')
        return buffer



