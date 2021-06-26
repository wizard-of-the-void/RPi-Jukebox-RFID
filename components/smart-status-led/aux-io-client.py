#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import configparser
import sys

BaseConfigPath = "../../settings/aux-io.BaseConfig.ini"
BaseConfig = configparser.ConfigParser()
BaseConfig.read(BaseConfigPath)

#data = " ".join(sys.argv[1:])

def sendAuxIoCommand(parameters):
    HOST, PORT = BaseConfig["connection"]["host"], BaseConfig["connection"].getint("port")
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(";".join(map(str, parameters)) + "\n", "utf-8"), (HOST, PORT))


#print("Sent:     {}".format(data))
#print("Received: {}".format(received))
sendAuxIoCommand(["init_AuxController"])