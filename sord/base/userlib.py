#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all user specific functions

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import time, socket, random, re

class sorduser(object):
	""" S.O.R.D. User object """
	expert = False # Expert mode enabled
	quick = False # No modem pause
	skills = ['', 'd', 'm', 't' ] # Enumerated skill names (db)
	directsql = [ # Direct SQL name access
		'level', 'armor', 'weapon', 'gold', 'bank', 'defence', 
		'str', 'hp', 'hpmax', 'exp', 'gems', 'charm', 'pkill', 
		'fuck', 'ffight', 'pfight', 'dkill', 'cls', 'sex', 
		'sung', 'flirt', 'atinn', 'master', 'horse', 'fairy', 
		'dragon', 'alive', 'used', 'uset', 'usem',
		'spcld', 'spclt', 'spclm']
	
	def __init__(self, loginname, dbcon, ntcon, art, config = 0, log = 0, speed = 0, noise=0):
		""" Initialize S.O.R.D User Object """
		self.dbcon = dbcon
		self.ntcon = ntcon
		self.art = art
		self.jennielevel = 0
		self.jennieused = False
		self.linespeed = speed
		self.noise = noise
		self.config = config
		self.log = log
		
		if ( speed == 0 ):
			self.ppause = 0.001
		elif ( speed == 1 ):
			self.ppause = 0.002
		elif ( speed == 2 ):
			self.ppause = 0.0005
		elif ( speed == 3 ):
			self.ppause = 0.00001
		
		thisSQL = "SELECT userid,password,fullname FROM users WHERE username = '"+loginname+"'"
		self.thisUserName = loginname
		
		db = dbcon.cursor()
		db.execute(thisSQL)
		
		row = db.fetchone()
		if not row:
			self.thisUserID = 0
			self.thisPassword = ""
			self.thisFullname = "unregistered"
		else:
			userid, password, fullname = row
			self.thisUserID = userid
			self.thisPassword = password
			self.thisFullname = fullname
		db.close()
		
	def __getattr__(self,name):
		""" Get object attribute - hijack sql attributes for lookup from sqlite """
		if name in self.directsql :
			db = self.dbcon.cursor()
			db.execute("SELECT "+name+" FROM users WHERE userid = ?", (self.thisUserID,))
			return db.fetchone()[0]
			db.close()
		else: 
			return object.__getattr__(self,name)
			
	def __setattr__(self,name,value):
		""" Set object attribute - hijack sql attributes - set immediatly in sqlite """
		if name in self.directsql :
			self.dbcon.execute("UPDATE users SET "+name+"=? WHERE userid=?", (value, self.thisUserID))
			self.dbcon.commit()
		else:
			object.__setattr__(self,name,value)

	def isOnline(self):
		""" Check if user is online """
		db = self.dbcon.cursor()
		db.execute("SELECT * FROM online WHERE userid = ?", (self.thisUserID,))
		row = db.fetchone()
		if not row:
			return False
		else:
			return True

	def getSkillUse(self, skill):
		""" Get skill use points """
		return getattr(self, 'use'+self.skills[skill])

		
	def getSkillPoint(self, skill):
		""" Get skill experience points """
		return getattr(self, 'spcl'+self.skills[skill])


	def updateSkillUse(self, skill, value):
		""" Update skill use points """
		setattr(self, 'use'+self.skills[skill], (getattr(self, 'use'+self.skills[skill]) + value))
		
	def updateSkillPoint(self, skill, value):
		""" Update skill experience points """
		setattr(self, 'spcl'+self.skills[skill], (getattr(self, 'spcl'+self.skills[skill]) + value))
		
	def toggleXprt(self):
		""" Toggle expert mode """
		if self.expert == False:
			self.expert = True
		else:
			self.expert = False
		
	def toggleQuick(self):
		""" Toggle quick (no modem pause) mode """
		if ( self.quick ):
			self.quick = False
		else:
			self.quick = True
			
	def write(self, data):
		""" Send data to connected client """
		for cpair in self.config.ldcolors:
			data = re.sub(cpair[0], '\x1b[0m'+cpair[1], data)
		if ( self.quick ): 
			self.ntcon.send(data)
		else:
			for thisData in list(data):
				if ( self.noise ):
					if ( random.randint(1, 2000) == 3 ):
						thisData = ''
				time.sleep(self.ppause)
				self.ntcon.send(thisData)

	def pause(self):
		""" Send pause string and wait for input """
		self.write("\r\n    `0:`2-`0: P`2ress `0A`2ny `0K`2ey `0:`2-`0:")
		pauser_quit = False
		while ( not pauser_quit ):
			data = self.ntcon.recv(5)
			if not data: break
			pauser_quit = True
			for i in xrange(1, 23):
				self.write("\x1b[1D \x1b[1D")
			self.ntcon.send("\r\n")
	
	def getgday(self):
		db = self.dbcon.cursor()
		db.execute("SELECT value FROM sord WHERE name = ?", ('gdays',))
		gday = db.fetchone()[0]
		db.close()
		return gday
		
	def login(self):
		""" Process user login """
		self.dbcon.execute("UPDATE users SET last = ?, atinn = 0 WHERE userid = ?", (time.strftime('%Y%j', time.localtime()),self.thisUserID))
		self.dbcon.execute("INSERT INTO online ( userid, whence ) VALUES ( ?, ? )", (self.thisUserID, time.ctime(time.time())))
		self.logontime = time.time()
		self.dbcon.commit()
		
	def logout(self):
		""" Process user logout """
		self.dbcon.execute("DELETE FROM online WHERE userid = ?", (self.thisUserID,))
		self.dbcon.commit()

	def userExist(self, value):
		""" Check is user (fullname) exists.  Return userid on true """
		db = self.dbcon.cursor()
		db.execute("SELECT userid FROM users WHERE fullname = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
	
	def userLoginExist(self, value):
		""" Check is user (login name) exists.  Return userid on true """
		db = self.dbcon.cursor()
		db.execute("SELECT userid FROM users WHERE username = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = False
		else:
			retrn = row[0]
		db.close()
		return retrn
	
	def userGetName(self, value):
		""" Get user fullname from userid """
		db = self.dbcon.cursor()
		db.execute("SELECT fullname FROM users WHERE userid = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
			
	def userGetLogin(self, value):
		""" Get user login name from userid """
		db = self.dbcon.cursor()
		db.execute("SELECT username FROM users WHERE userid = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
