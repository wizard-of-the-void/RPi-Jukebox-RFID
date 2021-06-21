#! /usr/bin/python3
import configparser
import logging
from i2c_led_driver import signal_definition, aux_io_controller

i2c_driver = aux_io_controller()
