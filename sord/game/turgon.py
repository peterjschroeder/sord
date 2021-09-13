#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains Turgon's Warrior Taining

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "19 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import random
from ..base import func
from . import menu
from . import data
from . import util

class turgon():
	""" S.O.R.D. Turgons Warrior Training """
	def __init__(self, user):
		""" Initialize Turgons Training """
		self.user = user
		
	def run(self):
		""" Turgons run logic """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.turgon())
				user.write(menu.turgon(user))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == '?' ):
				user.write("?\r\n")
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("Q\r\n")
				if ( user.level < 12 ):
					thisUserLevel = user.level
					thisUserExp   = user.exp
					thisNeedExp   = data.masters[thisUserLevel][2] - thisUserExp
					for thisWisdom in data.masters[thisUserLevel][3]:
						user.write("\r\n  `2"+thisWisdom+"`0")
					user.write("\r\n\r\n  `%"+data.masters[thisUserLevel][0]+"`2 looks at you closely and says...\r\n")
					if ( thisNeedExp < 1 ):
						user.write("\r\n  `2"+data.masters[thisUserLevel][4]+"`.\r\n")
					else:
						user.write("\r\n  `2You need about `%"+str(thisNeedExp)+"`2 experience before you'll be as good as me.`.\r\n")
				else:
					user.write("\r\n  `2You have learned all that you can.  This place holds nothing more for you!`.\r\n")
				user.pause()
			elif ( key[0] == 'v' or key[0] == 'V' ):
				user.write('V')
				db = user.dbcon.cursor()
				db.execute("SELECT fullname, dkill FROM users WHERE dkill > 0 ORDER by dkill DESC")
				user.write("\r\n\r\n  `2Users who have slain the dragon:`.\r\n")
				for row in db.fetchall():
					if not row:
						user.write("\r\n\r\n  `2What a sad thing - there are no heroes in this realm.`.\r\n")
						break
					else:
						for (nombre, xdata) in row:
							user.write("  `2"+nombre+func.padnumcol(nombre, 25)+" `0"+str(xdata)+"`.\r\n")
				user.write("\r\n")
				db.close()
				user.pause()
			elif ( key[0] == 'y' or key[0] == 'Y' ):
				user.write('Y')
				user.write(util.viewstats(user))
				user.pause()
			elif ( key[0] == 'a' or key[0] == 'A' ):
				user.write('A')
				if ( user.level > 11 ):
					user.write("\r\n\r\n  `2There is no master for you to attack stoopid!`.\r\n")
				elif ( user.master ):
					user.write("\r\n\r\n  `2I'm sorry my son, you may only fight me once per game-day`.\r\n")
				else:
					self.fight()
			else:
				skipDisp = True

	def menu(self, user, ehp, ename) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  `2Your Hitpoints : `0"+str(user.hp)+"`.\r\n"
		thismenu += "  `2"+ename+"'s Hitpoints : `0"+str(ehp)+"`.\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n  `2Your command, `0"+user.thisFullname+"`2? [`#A`2] `0:`2-`0: `."
		return thismenu

	def fight(self):
		""" Master Fight System """
		user = self.user
		thisUserLevel = user.level
		thisUserDefense = user.defence
		thisUserHit     = user.str / 2
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		thisEnemyHit     = data.masters[thisUserLevel][7] / 2
		thisEnemyDefense = data.masters[thisUserLevel][8]
		thisEnemyHP      = data.masters[thisUserLevel][6]
		thisEnemyName    = data.masters[thisUserLevel][0]
		thisEnemyWeapon  = data.masters[thisUserLevel][1]
		
		user.write("\r\n\r\n  `2**`%FIGHT`2**\r\n")
		user.write("\r\n  `2You have encountered "+thisEnemyName+"!!`.\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.menu(user, thisEnemyHP, thisEnemyName))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( key[0] == 'a' or key[0] == 'A' ): # Attack!
				user.write("A\r\n")
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) - thisEnemyDefense
				if ( False ): # We Hit First (always)
					if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage`.\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  `2"+thisEnemyName+" misses you completely`.\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  `2You hit "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  `1"+data.masters[thisUserLevel][5]+"`.\r\n")
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
				user.write("\r\n  `2You retire from the field before getting yourself killed.`.\r\n")
				user.hp = user.hpmax
				user.master = 1
				ctrlRan = True
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("\r\n  `1You are in Combat!  Try Running!`.\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write("\r\n  `2You are in combat, and they don't make house calls!`.\r\n")
			else:
				skipDisp = True
	
		if ( ctrlWin ) :
			addExp = data.masters[thisUserLevel][2] / 10
			user.exp += addExp
			user.level += 1
			user.defence += data.masterwin[thisUserLevel][2]
			user.str += data.masterwin[thisUserLevel][1]
			user.hpmax += data.masterwin[thisUserLevel][0]
			user.updateSkillPoint(user.cls, 1)
			user.updateSkillUse(user.cls, 1)
			user.hp = user.hpmax
			user.write("\r\n  `2You have receieved `0+"+str(data.masterwin[thisUserLevel][2])+"`2 vitality, `0+"+str(data.masterwin[thisUserLevel][1])+"`2 strength, and `0+"+str(data.masterwin[thisUserLevel][0])+"`2 hitpoints.`.\r\n")
			user.write("  `2You have gained `0"+str(addExp)+"`2 experience, and are now level `0"+str(user.level)+"`2.`.\r\n")
			user.pause()
		if ( ctrlDead ) :
			user.master = 1
			user.hp = user.hpmax
			user.write("\r\n  `1Tragically, you are horribly disfigured....  oh wait...`.\r\n")
			user.write("  `1You always looked like that you say?...  That's unfortunate...`.\r\n")
			user.write("  `2Anyway, you lost.  Being the gracious master "+thisEnemyName+" is, he heals\r\n  you and sends you away for the day.`.\r\n")
			user.pause()
		
