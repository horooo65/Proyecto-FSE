# !/usr/bin/env python3
# ## ###############################################
#
# Autores: 
# Acosta Hernández Horacio Emmanuel
# Juárez Munguía Brandon Jesús
# Medina Cruz Josué Emanuel
# License: MIT
#
# ## ###############################################
#
# virtualboard.py
# Manejo del simulador
#
## ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from atexit import register
from threading import Thread
from board import Board
from tkinter import mainloop
import RPi.GPIO as GPIO

def exit_handler():
	print('Shutting down board GUI')
	if _async_board_thread:
		_async_board_thread.join()

def _async_board_worker():
	global _async_board_thread
	board = Board()
	board.connect(GPIO._io_pins)
	try:
		mainloop()
	except:
		pass
	_async_board_thread = None

_async_board_thread = Thread(target=_async_board_worker)
register(exit_handler)
_async_board_thread.start()
