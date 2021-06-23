#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import socketserver
#from i2c_led_driver import signal_definition, aux_io_controller

BaseConfigPath = "../../settings/aux-io.BaseConfig.ini"
#SignalConfigPath = "../setting/aux-io.SignalConfig.ini"

BaseConfig = configparser.ConfigParser()
BaseConfig.read(BaseConfigPath)

#SignalConfig = configparser.ConfigParser()
#SignalConfig.read(SignalConfigPath)

#i2c_driver = aux_io_controller()


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].decode('utf8').strip()
        socket = self.request[1]
        command = data[0:3].lower()
        parameter = data[3:128].strip().split(";")
        print("{} requested:".format(self.client_address[0]))
        print(command)
        print(parameter)
        socket.sendto(data.upper().encode('utf8'), self.client_address)

if __name__ == "__main__":
    HOST, PORT = BaseConfig['connection']['host'], BaseConfig['connection'].getint('port')
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()