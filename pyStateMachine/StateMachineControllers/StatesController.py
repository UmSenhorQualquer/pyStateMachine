#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"

from pyStateMachine.States.State import EndState


class StatesController(object):

	def __init__(self, states, sharedVar=None):
		states += [EndState()] #Add the last state
		for s in states: s.shared = sharedVar

		#Dictionary with all the states
		self._states 	= dict([ (x.__class__.__name__, x) for x in states])

		initialState = states[0].__class__.__name__
		#First state
		self._initial 	= self._states[initialState]
		#Store the next states to be iterate
		self._waitingStates = [ (None, initialState, None) ] 
		


		
	def iterateStates(self):
		"""
		Iterate states - each call go to another level
		"""

		if len(self._waitingStates)>0:
			statesOutputs = []

			#First run all the pending states
			for fromStateName, toStateName, inputParam in self._waitingStates:
				state 		  = self._states[toStateName]
				statesOutputs.append( (toStateName ,state, state.run(inputParam) ) )

			#Check the events of each exectuted state:
			for stateName, state, output in statesOutputs:
				#Remove the exectued state from the waiting queue
				self._waitingStates.pop(0) 

				#Check each event
				for e in state.events:
					#Select the next state to go
					go2State = e.go2StateTrue if e(state, output) else e.go2StateFalse
					#In case the state is None, it stops the state execution
					if go2State!=None: 
						self._waitingStates.append( [stateName, go2State, output] )
					else:
						self._waitingStates.append( [stateName, 'EndState', output] )

		else:
			print "State machine ended"

		#print self.currentStatesNames
		
	@property 
	def currentStatesNames(self): return [toState for fromState, toState, stateOutput in self._waitingStates]

	@property 
	def currentStates(self): return [self._states[toState] for fromState, toState, stateOutput in self._waitingStates]

	@property 
	def currentEdges(self): return [ (self._states[fromState] if fromState!=None else None ,self._states[toState]) for fromState, toState, stateOutput in self._waitingStates]


	@property 
	def ended(self): 
		"""
		Indicate if state machine has ended or not
		"""
		return len(self._waitingStates)==0

		
		
