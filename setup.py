#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


from setuptools import setup

setup(

	name				='pyStateMachine',
	version 			='1.0',
	description 		="""pyStateMachine is a Python 2.7 framework to implement and visualise state machines.""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	download_urlname	='https://github.com/UmSenhorQualquer/pyStateMachine',
	url 				='https://github.com/UmSenhorQualquer/pyStateMachine',
	
	packages=[
		'pyStateMachine',
		'pyStateMachine.StateMachineControllers', 
		'pyStateMachine.States'],
	
	install_requires=[
		"pydot",
		"cv2",
	],
)