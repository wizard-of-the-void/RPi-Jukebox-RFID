#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import socketserver
import aux_io_actions
from i2c_led_driver import signal_definition, aux_io_controller

BaseConfigPath = "../../settings/aux-io.BaseConfig.ini"
SignalConfigPath = "../setting/aux-io.SignalConfig.ini"

logging.basicConfig(filename="../../logs/aux-io-server.log", level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

BaseConfig = configparser.ConfigParser()
BaseConfig.read(BaseConfigPath)
logging.debug("Base configuration loaded from %s", BaseConfigPath)

#i2c_driver = aux_io_controller()
#logging.debug("i2c-Driver instanciated")

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].decode("utf8").strip()
        socket = self.request[1]
        parameter = data[0:128].strip().split(";")
        command = parameter.pop(0)

        if hasattr(aux_io_actions, command):
            try:
                logging.debug("Calling the command %s", command)
                action = getattr(aux_io_actions, command)
                action(i2c_driver, parameter)
            except:
                logging.exception("Calling the command %s failed!", command)
        else:
            logging.error("Unknown command %s requested!", command)

        print("{} requested:".format(self.client_address[0]))
        print(command)
        print(parameter)
        socket.sendto(data.upper().encode("utf8"), self.client_address)

if __name__ == "__main__":
    HOST, PORT = BaseConfig["connection"]["host"], BaseConfig["connection"].getint("port")
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()