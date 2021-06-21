#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import weakref
import smbus
import RPi.GPIO as GPIO
from time import sleep

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1
# Spark Address
ADDRESS = 0x08
# Level shifter pin
ENABLE_PIN = 23


class signal_definition:
   def __init__(self, controller, slotId, red = 0, green = 0, blue = 0 , fade_in = 7, hold = 10, fade_out = 7, state = False):
      self.controller = weakref.ref(controller)
      self.slotId = slotId
      self.red = red
      self.green = green
      self.blue = blue
      self.fade_in = fade_in
      self.fade_out = fade_out
      self.hold = hold
      self.__state = state

   def update(self):
         self.controller.transmit_signal_to_controller(self.slotId)

   @property
   def state(self):
      return self.__state

   @state.setter
   def state(self, aState):
      self.__state = bool(aState)
      self.controller.transmit_states()

   def data(self):
      return bytes([self.red, self.green, self.blue, self.fade_in, self.hold, self.fade_out])

class aux_io_controller:
   # register addresses
   STATE_ADDR =  0
   ZERO_ADDR =  1
   CONTROL_ADDR  =  2
   BLK_A_ADDR = 3
   BLK_COUNT = 8
   BLK_SIZE = 6
   RESET_FLAG = 0x80

   def __init__(self, addr=ADDRESS, port=I2CBUS, a_enable_pin=ENABLE_PIN):
      self.addr = addr
      self.bus = smbus.SMBus(port)
      self.enable_pin = a_enable_pin

      GPIO.setmode(GPIO.BCM)
      GPIO.setup(self.enable_pin, GPIO.OUT)
      self.enable_com()

      self.slots = [None] * self.BLK_COUNT
      for slotId in range(self.BLK_COUNT):
         self.assign_signal_to_slot(signal_definition(self, slotId), slotId)

   def assign_signal_to_slot(self, signal, slotId):
      signal.controller = self
      self.slots[slotId] = signal

   def get_slot_address(self, slotId):
      return self.BLK_A_ADDR + self.BLK_SIZE * slotId

   def get_signal(self, slotId):
      return self.slots[slotId]

   def transmit_signal_to_controller(self, slotId):
      signal_bytes = self.slots[slotId].data
      register_address = self.get_slot_address(slotId)
      self.bus.write_i2c_block_data(self.addr, register_address, signal_bytes)
      sleep(0.0001)

   def transmit_all_signals(self):
      for slotId in range(self.BLK_COUNT):
         self.transmit_signal_to_controller(slotId)

   def byte(self, bits):
      for i in range(0, len(bits)):
         byte = byte | (bits[i] << i)
      return bytes(byte)[0]

   def enable_com(self):
      GPIO.output(self.enable_pin, True)

   def disable_com(self):
      GPIO.output(self.enable_pin, False)

   def transmit_states(self):
      slot_states = [None] * self.BLK_COUNT
      for slotId in range(self.BLK_COUNT):
         slot_states[slotId] = self.slots[slotId].state()

      self.bus.write_byte_data(self.addr, self.STATE_ADDR, self.byte(slot_states))
      sleep(0.0001)

   def reset_controller(self):
      self.bus.write_byte(self.addr, self.RESET_FLAG)
      sleep(0.0001)

   def __del__(self):
      GPIO.cleanup()
