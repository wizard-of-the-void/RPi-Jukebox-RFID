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

def toggle_SignalState(i2c_driver, parameters):
    if  i2c_driver.get_signal_by_name(parameters[0]).state == i2c_driver.get_signal_by_name(parameters[1]).state:
         i2c_driver.get_signal_by_name(parameters[0]).state = parameters[2]
         i2c_driver.get_signal_by_name(parameters[1]).state = parameters[3]
    else:
        i2c_driver.get_signal_by_name(parameters[0]).state = not i2c_driver.get_signal_by_name(parameters[0]).state 

def reset_AuxController(i2c_driver, parameters):
    i2c_driver.reset_controller(bool(parameters[0]))
    i2c_driver.set_all_states(False)

