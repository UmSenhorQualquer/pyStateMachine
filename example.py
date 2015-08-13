#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


from pyStateMachine.States.State import State, goto
from pyStateMachine.StateMachineControllers.StatesController import StatesController
from pyStateMachine.StateMachineControllers.StatesControllerDebug import StatesControllerDebug

#########################################################################
#########################################################################
#########################################################################
class InitialState(State):

	def run(self, inVar):
		print "### InitialState"
		return self.shared

	@goto('AState', 'BState')
	def LedActive(self, inVar): return False


	@goto('CState')
	def LeverActivated(self, inVar): return False

#########################################################################
#########################################################################
#########################################################################
class AState(State):
	
	def run(self, inVar):
		print '+++ AState'
		inVar._passedA=True
		return inVar

	@goto('InitialState')
	def MotorOn(self, inVar): return True

	@goto()
	def MotorOff(self, inVar): return True

#########################################################################
#########################################################################
#########################################################################
class BState(State):
	
	def run(self, inVar):
		print '--- BState'
		inVar._passedB=True
		return inVar

	@goto(false='InitialState', true='CState')
	def Reset(self, inVar): return True

#########################################################################
#########################################################################
#########################################################################
class CState(State):
	
	def run(self, inVar):
		print '--- CState'
		inVar._passedB=True
		return inVar

	@goto(true='InitialState', false='AState')
	def Reset(self, inVar): 
		"""
		Check if is True
		"""
		return False







#########################################################################
#########################################################################
#########################################################################



class StatesVariables(object):
	def __init__(self): self._passedA = False; self._passedB = False

#controller = StatesController([InitialState(), AState(), BState(), CState()], sharedVar=StatesVariables() )
controller = StatesControllerDebug([InitialState(), AState(), BState(), CState()], sharedVar=StatesVariables(), size=(800,600) )
while not controller.ended:  controller.iterateStates()
