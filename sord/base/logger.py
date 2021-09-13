#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all logging functions.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
import time, re

class sordLogger():
	""" S.O.R.D. Logger class """
	def __init__(self):
		""" Inialize a new logger """
		self.__mainLogger = list()
		self.__activePeers = 0
		self.__totalPeers = 0
		
	def add(self, value):
		"""Add *arg to log"""
		tmptime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
		value = re.sub('`.', '', value)
		self.__mainLogger.append(tmptime+" :: "+value)
		self.__mainLogger = self.__mainLogger[-100:]
		
	def write(self, value):
		""" Intercept for webserver stderr logging """
		lines = value.splitlines()
		for line in lines:
			if ( line.find("favicon") > -1 ):
				pass
			elif ( line.find("code ") > -1 ):
				pass
			elif ( line.find("drag.png") > -1 ):
				pass
			else:
				self.add(" -w- "+line)
		
	def show(self, value):
		""" Show *arg log items """
		return self.__mainLogger[(value * -1):]
		
	def addcon(self):
		""" Increment connection """
		self.__activePeers += 1
		self.__totalPeers += 1
		
	def remcon(self):
		""" Remove connection from active """
		self.__activePeers -= 1
		
	def getactive(self):
		""" Get active peers """
		return self.__activePeers
		
	def gettotal(self):
		""" Get total peers """
		return self.__totalPeers

