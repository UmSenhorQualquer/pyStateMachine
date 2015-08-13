#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


from types import FunctionType


def goto(true=None, false=None):
	def go2decorator(func):
		def func_wrapper(self, inVar): return func(self, inVar)

		func_wrapper.go2StateTrue  = true
		func_wrapper.go2StateFalse = false
		func_wrapper.label = func.__name__ if func.__doc__==None else '\n'.join([x for x in func.__doc__.replace('\t','').split('\n') if len(x)>0])
		return func_wrapper
	return go2decorator



class State(object):

	def __init__(self, *args, **kargs): self.shared = None

	def run(self, input=None):
		print "Run State", self.__class__.__name__
		return None

	@property
	def events(self): 
		return [y for x,y in self.__class__.__dict__.items() if type(y) == FunctionType and hasattr(y,'go2StateTrue')]

class EndState(State): pass