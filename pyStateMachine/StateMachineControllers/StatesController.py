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
import pydot

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
		

	def exportGraph(self, filename='stateMachine.png'):
		currentStates = self.currentStates
		currentEdges  = self.currentEdges

		# this time, in graph_type we specify we want a DIrected GRAPH
		graph = pydot.Dot(graph_type='digraph', fontname='Verdana', ratio='1')

		nodes = {}
		# Draw the nodes
		for nodeName, state in self._states.items():
			
			attrs = {'shape':'circle', 'margin': '0.02px'}

			#If is drawing the EndNode
			if state.__class__.__name__=='EndState': attrs.update({'shape':'point', 'width':'0.2', 'peripheries':'0.2'})
			#If is drawing the first Node, add the Initial Node
			if state==self._initial: startNode = pydot.Node('Start', shape='point', width='0.2' ); graph.add_node(startNode)
			#If the node will be the next to be precessed
			if state in currentStates: attrs.update({'style':'filled'})

			node 			= pydot.Node( nodeName, **attrs ); graph.add_node(node)
			nodes[nodeName] = [state, node]

			#If is drawing the first Node, add an edge from the InitalNode to the first Node.
			if state == self._initial: graph.add_edge( pydot.Edge(startNode, node, **({'penwidth':'3px'} if (None, state) in currentEdges else {}) ) )

		#Draw edges
		endNode = nodes['EndState']
		for state0, node0 in nodes.values():
			#For each Node draw the events edges
			for e in state0.events:

				label = "{0}==True".format(e.label)
				extraComment = self.eventExtraComment(e, True)
				if extraComment: label +='\n' + extraComment

				#Draw the edge when the event result is True
				state1, node1 = nodes[e.go2StateTrue] if e.go2StateTrue!=None else endNode
				attrs = { 'label':label, 'fontsize':'10px' }
				if (state0, state1) in currentEdges: attrs['penwidth']='3px'
				edge = pydot.Edge(node0, node1, **attrs ); graph.add_edge( edge )

				if e.go2StateFalse!=None:

					label = "{0}==False".format(e.label)
					extraComment = self.eventExtraComment(e, False)
					if extraComment: label +='\n' + extraComment

					#Draw the edge when the event result is False
					state1, node1 = nodes[e.go2StateFalse] if e.go2StateFalse!=None else endNode
					attrs = { 'label':label, 'fontsize':'10px' }
					if (state0, state1) in currentEdges: attrs['penwidth']='3px'
					edge = pydot.Edge(node0, node1, **attrs ); graph.add_edge( edge )
	
			
		#Save and show the generated image
		graph.write_png(filename)
		
	def eventExtraComment(self, e, result): return None

		
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


	@property
	def states(self): return self._states
	
		
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

		
		
