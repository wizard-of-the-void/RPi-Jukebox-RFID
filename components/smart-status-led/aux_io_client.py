#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import configparser

BaseConfigPath = "../../settings/aux-io.BaseConfig.ini"
BaseConfig = configparser.ConfigParser()
BaseConfig.read(BaseConfigPath)


def sendAuxIoCommand(parameters):
    HOST, PORT = BaseConfig["connection"]["host"], BaseConfig["connection"].getint("port")
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(";".join(map(str, parameters)) + "\n", "utf-8"), (HOST, PORT))

if __name__ == "__main__":
    sendAuxIoCommand(["init_AuxController"])