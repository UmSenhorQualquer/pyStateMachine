#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


import pydot, cv2
from pyStateMachine.StateMachineControllers.StatesController import StatesController
from pyStateMachine.States.State import EndState

class StatesControllerDebug(StatesController):
	"""
	Implements a debug vision of the state machine.
	"""

	def showGraph(self):
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

				#Draw the edge when the event result is True
				state1, node1 = nodes[e.go2StateTrue] if e.go2StateTrue!=None else endNode
				attrs = { 'label':"{0}    \n(True)".format(e.label), 'fontsize':'10px' }
				if (state0, state1) in currentEdges: attrs['penwidth']='3px'
				edge = pydot.Edge(node0, node1, **attrs ); graph.add_edge( edge )

				if e.go2StateFalse!=None:
				
					#Draw the edge when the event result is False
					state1, node1 = nodes[e.go2StateFalse] if e.go2StateFalse!=None else endNode
					attrs = { 'label':"{0}    \n(False)".format(e.label), 'fontsize':'10px' }
					if (state0, state1) in currentEdges: attrs['penwidth']='3px'
					edge = pydot.Edge(node0, node1, **attrs ); graph.add_edge( edge )
	
			
		#Save and show the generated image
		graph.write_png('stateMachine.png')
		img = cv2.imread('stateMachine.png')
		#raw_input('please press a key...')
		#print dd
		#print img
		#print '<img src="./stateMachine.png" />'
		cv2.imshow('State machine', img)
		key = cv2.waitKey(10)
		if key==27: exit() #Exit in case ESC is pressed
		#import time
		#time.sleep(1) 


	def iterateStates(self):
		self.showGraph() #Show the graph before processing the Nodes
		super(StatesControllerDebug, self).iterateStates()
		if self.ended: self.showGraph() #Show the last iteration when the State machine end