#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

def init_AuxController(i2c_driver, parameters):
    i2c_driver.reset_controller()
    i2c_driver.transmit_all_signals()

def set_HaltState(i2c_driver, parameters):
    i2c_driver.reset_controller(True)
    i2c_driver.transmit_all_signals()
    i2c_driver.get_signal_by_name("halt", True)

def set_SignalState(i2c_driver, parameters):
    i2c_driver.get_signal_by_name(parameters[0], parameters[1])

def reset_AuxController(i2c_driver, parameters):
    i2c_driver.reset_controller()
