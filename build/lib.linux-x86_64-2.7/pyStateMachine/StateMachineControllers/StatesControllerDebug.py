#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


import cv2
from pyStateMachine.StateMachineControllers.StatesController import StatesController
from pyStateMachine.States.State import EndState

class StatesControllerDebug(StatesController):
	"""
	Implements a debug vision of the state machine.
	"""
	def __init__(self, states, sharedVar=None, size=None, idleFunction=None):
		super(StatesControllerDebug, self).__init__(states, sharedVar)

		self._size = size
		self._idleFunction = idleFunction


	def showGraph(self):
		self.exportGraph()
		img = cv2.imread('stateMachine.png')
		
		if self._idleFunction: self._idleFunction(img.copy())
		if self._size: img = cv2.resize(img, self._size)


		cv2.imshow('State machine', img)
		key = cv2.waitKey(300)
		if key==27: exit() #Exit in case ESC is pressed
		#import time
		#time.sleep(1) 


	def iterateStates(self):
		self.showGraph() #Show the graph before processing the Nodes
		super(StatesControllerDebug, self).iterateStates()
		if self.ended: self.showGraph() #Show the last iteration when the State machine end