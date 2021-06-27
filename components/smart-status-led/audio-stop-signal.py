#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aux_io_client

aux_io_client.sendAuxIoCommand(["set_SignalState", "pause", False])
aux_io_client.sendAuxIoCommand(["set_SignalState", "stop", True])
aux_io_client.sendAuxIoCommand(["set_SignalState", "play", False])