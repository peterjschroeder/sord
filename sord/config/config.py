#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * S.O.R.D. Server Configuration Details

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

from random import randint
from os import getcwd

class sordConfig():
	""" Master S.O.R.D. Config Class """
	
	def __init__(self, testing=0):
		""" Initalize configuration.  In 'testing' mode, randomized port number """
		self.sqlitefile = "sord.db"
		
		self.gameadmin = "jtsage"
		self.gameadminpass = "legend"
		
		self.host = "sord.jtsage.com"
		self.admin = "J.T.Sage"
		
		self.daylength = 24
		self.bankinterest = 10
		self.delinactive = 256
		self.ffight = 30
		self.pfight = 5
		
		self.version = "2.0-pysqlite"

		self.port = 6969
		self.webport = 6980 # Set to False to disable web server.

		self.useunicode = False # When False, use ascii.
		
		self.fulldebug = False
		self.ansiskip = False
		self.forcenewday = False
		
		self.progpath = getcwd()
		
		if ( testing ):
			self.port += randint(1, 10)
			
		self.ldcolors = [
			( '`1', '\x1b[31m'), ( '`2', '\x1b[32m'), ( '`3', '\x1b[33m'), ( '`4', '\x1b[34m'),
			( '`5', '\x1b[35m'), ( '`6', '\x1b[36m'), ( '`7', '\x1b[37m'), ( '`8', '\x1b[1;30m'),
			( '`9', '\x1b[1;31m'), ( '`0', '\x1b[1;32m'), ( '`!', '\x1b[1;33m'), ( '`@', '\x1b[1;34m'), 
			( '`#', '\x1b[1;35m'), ( '`\$', '\x1b[1;36m'), ( '`%', '\x1b[1;37m'), ( '`\.', '')]

			
if ( __name__ == "__main__" ):
	cc = sordConfig()
	print "SORD Version: ", cc.version
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print cc.host, " :: ", cc.port
	print "Admin: ", cc.admin
	print "Day is ", cc.daylength, " hours"
	print "Inactive deletes after ", cc.delinactive, " days"
	print "Forest fights ", cc.ffight, "/day"
	print "Player fights ", cc.pfight, "/day"
	print "Game admin: ", cc.gameadmin, "/", cc.gameadminpass
	
