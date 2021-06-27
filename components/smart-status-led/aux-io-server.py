#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import socketserver
import aux_io_actions
from i2c_led_driver import signal_definition, aux_io_controller

BaseConfigPath = "../../settings/aux-io.BaseConfig.ini"

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename="../../logs/aux-io-server.log",level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")
#logging.basicConfig(filename="/home/pi/RPi-Jukebox-RFID/logs/aux-io-server.log", encoding='utf-8',level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

BaseConfig = configparser.ConfigParser()
BaseConfig.read(BaseConfigPath)
logging.debug("Base configuration loaded from %s", BaseConfigPath)
logging.debug(BaseConfig.sections())

i2c_driver = aux_io_controller()
logging.debug("i2c-Driver instanciated")

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class receives the request packets (UPD) and calls the requested
    actions from the actions module if thes should exist. The request is
    sent as a utf8-string of values separated by semicolons.
    """

    def handle(self):
        data = self.request[0].decode("utf8").strip()
        socket = self.request[1]
        parameter = data.strip().split(";")
        command = parameter.pop(0)

        logging.debug("{} requested:".format(self.client_address[0]))
        logging.debug("Action: %s", command)
        logging.debug("With parameters: %s", parameter)

        if hasattr(aux_io_actions, command):
            try:
                logging.debug("Calling the command %s", command)
                action = getattr(aux_io_actions, command)
                action(i2c_driver, parameter)
            except:
                logging.exception("Calling the command %s failed!", command)
        else:
            logging.error("Unknown command %s requested!", command)


if __name__ == "__main__":
    HOST, PORT = BaseConfig["connection"]["host"], BaseConfig["connection"].getint("port")
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
