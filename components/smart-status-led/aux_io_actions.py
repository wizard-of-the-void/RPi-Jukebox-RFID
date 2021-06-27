#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import i2c_led_driver

def init_AuxController(i2c_driver, parameters):
    i2c_driver.reset_controller()
    i2c_driver.transmit_all_signals()
    i2c_driver.set_all_states(False)

def set_HaltState(i2c_driver, parameters):
    i2c_driver.set_all_states(False)
    i2c_driver.get_signal_by_name("halt").state = True

def set_SignalState(i2c_driver, parameters):
    i2c_driver.get_signal_by_name(parameters[0]).state = parameters[1]

def reset_AuxController(i2c_driver, parameters):
    i2c_driver.reset_controller(bool(parameters[0]))
    i2c_driver.set_all_states(False)
