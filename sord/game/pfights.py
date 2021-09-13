#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains player fighting code.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "19 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import random, re
from ..base import func
from ..base import userlib
from . import menu
from . import data
from . import util

class killer():
	""" S.O.R.D. Killing Fields """
	def __init__(self, user):
		""" Initialize Killing Fields Instance """
		self.user = user
		
	def run(self):
		""" Slaughter Run Logic """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.killer())
				user.write(menu.slaughter(user))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == 'e' or key[0] == 'E' ):
				user.write('E')
				util.dirt(user)
			elif ( key[0] == 'w' or key[0] == 'W' ):
				user.write('W')
				if ( user.pkill > 0 ):
					user.write(func.casebold("\r\n  Carve what in the soft dirt? :-: ", 2))
					ann = func.getLine(user.ntcon, True)
					user.dbcon.execute("INSERT INTO dirt ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
					user.dbcon.commit()
					user.write(func.casebold("\r\n  Carving Added!\r\n", 2))
					user.pause()
				else:
					user.write("\r\n  `2You have to accomplish something here before you can trash talk!`.\r\n")
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write('L')
				user.write(self.list())
				user.pause()
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write("S\r\n")
				tokillID = util.finduser(user, "\r\n  `2Kill Who ?")
				if ( tokillID > 0 ):
					tokillName = user.userGetLogin(tokillID)
					usertoKill = userlib.sorduser(tokillName, user.dbcon, user.ntcon, user.art)
					if ( not usertoKill.alive ):
						user.write("\r\n  `2Already dead your holiness...`.\r\n")
						user.pause()
					elif ( usertoKill.isOnline() ):
						user.write("\r\n  `2They are online right now!  (and real time player fights are not yet supported.  sorry)`.\r\n")
						user.pause()
					else:
						self.fight(user, usertoKill)
				else:
					user.write("\r\n  `2No user by that name found.`.\r\n")
			else:
				skipDisp = True

	def list(self):
		""" Player List """
		user = self.user
		db = user.dbcon.cursor()
		db.execute("SELECT userid, fullname, exp, level, cls, sex, alive, pkill FROM users WHERE atinn = 0 AND userid <> ? AND userid NOT IN ( SELECT userid FROM online ) ORDER BY exp DESC", (user.thisUserID,))
		output = "\r\n\r\n`2     Name                    Experience    Level     Kills    Status`0\r\n";
		output += user.art.line()
		for line in db.fetchall():
			if ( line[5] == 2 ):
				lineSex = " `#F "
			else:
				lineSex = "   "
				
			if ( line[4] == 1 ):
				lineClass = "`9D "
			elif ( line[4] == 2 ):
				lineClass = "`9M "
			else:
				lineClass = "`9T "
	
			if ( line[6] == 1 ):
				lineStatus = "`0Alive"
			else:
				lineStatus = "`1 Dead"
	
			output += lineSex + lineClass + "`2" + line[1] + func.padnumcol(str(line[1]), 23) + "`2" + func.padright(str(line[2]), 11)
			output += func.padright(str(line[3]), 9) + "     " + func.padright(str(line[7]), 5) + "     " + lineStatus + "\r\n"
		db.close()
		return output + "\r\n"
		
	def menu(self, user, ehp, ename) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  `2Your Hitpoints : `0"+str(user.hp)+"`.\r\n"
		thismenu += "  `2"+ename+"`2's Hitpoints : `0"+str(ehp)+"`.\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n  `2Your command, `0"+user.thisFullname+"`2? `8[`#A`8] `0:`2-`0: `."
		return thismenu

	def fight(self, user, usertokill):
		""" Master Fight System """
		user.pfight -= 1
		thisUserDefense = user.defence
		thisUserHit     = user.str / 2
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		thisEnemyHit     = usertokill.str / 2
		thisEnemyDefense = usertokill.defence
		thisEnemyWeapon  = data.weapon[usertokill.weapon]
		
		user.write("\r\n\r\n  `2**`%FIGHT`2**\r\n")
		user.write("\r\n  `2You have encountered "+usertokill.thisFullname+"`2!!`.\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and usertokill.hp > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.menu(user, usertokill.hp, usertokill.thisFullname))
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
				if ( True ): # We Hit First (always)
					if ( myAttack >= usertokill.hp ): # If he's dead, he didn't hit us at all - also, set our attack to zero him
						myAttack = usertokill.hp
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  `2"+usertokill.thisFullname+" `2hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage`.\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  `2"+usertokill.thisFullname+" `2misses you completely`.\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  `2You hit "+usertokill.thisFullname+" `2for `9"+str(myAttack)+"`2 damage\r\n")
					usertokill.hp -= myAttack
					if ( usertokill.hp < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  `1"+usertokill.thisFullname+" `2lies dead at your feet!`.\r\n")
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
				user.write('R')
				if ( random.randint(1, 10) == 4 ): # Hit in the back.
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+usertokill.thisFullname+" `2hits you in the back with it's "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage\r\n")
						user.hp -= hisAttack
				else:
					user.write("\r\n  `2You narrowly escape harm.`.\r\n")
					ctrlRan = True
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("Q\r\n  `1You are in Combat!  Try Running!`.\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write("H\r\n  `2You are in combat, and they don't make house calls!`.\r\n")
			else:
				skipDisp = True
	
		if ( ctrlWin ) :
			user.pkill += 1
			addExp = usertokill.exp / 2
			delExp = usertokill.exp / 10
			addGems = usertokill.gems / 2
			if ( addGems < 1 ):
				addGems = 0
			else:
				user.gems += addGems
				usertokill.gems -= addGems
			addGold = usertokill.gold
			if ( addGold > 0 ):
				user.gold += addGold
				usertokill.gold -= addGold
			user.exp += addExp
			usertokill.exp -= delExp
			usertokill.alive = 0
			user.write("\r\n  `2You have gained `0"+str(addExp)+"`2 experience, `0"+str(addGems)+"`2 gems, and `0"+str(addGold)+"`2 gold.`.\r\n")
			lamentTop = len(data.killerwin) - 1
			lamentThis = data.killerwin[random.randint(0, lamentTop)]
			lamentThis = re.sub("`n", "\r\n    ", lamentThis)
			lamentThis = re.sub("`g", user.thisFullname, lamentThis)
			lamentThis = re.sub("`e", usertokill.thisFullname, lamentThis)
			user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (lamentThis,user.getgday()))
			user.dbcon.commit()
			user.pause()
		if ( ctrlDead ) :
			usertokill.pkill += 1
			usertokill.hp = usertokill.hpmax #Heal the undead other player (he won)
			addExp = user.exp / 2
			delExp = user.exp / 10
			addGems = user.gems / 2
			if ( addGems < 1 ):
				addGems = 0
			else:
				user.gems -= addGems
				usertokill.gems += addGems
			addGold = user.gold
			if ( addGold > 0 ):
				user.gold -= addGold
				usertokill.gold += addGold
			user.exp -= delExp
			usertokill.exp += addExp
			user.alive = 0
			#exception handles, do it later. user.logout()
			lamentTop = len(data.killerlose) - 1
			lamentThis = data.killerlose[random.randint(0, lamentTop)]
			lamentThis = re.sub("`n", "\r\n    ", lamentThis)
			lamentThis = re.sub("`g", user.thisFullname, lamentThis)
			lamentThis = re.sub("`e", usertokill.thisFullname, lamentThis)
			user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (lamentThis,user.getgday()))
			user.dbcon.commit()
			user.write(func.casebold("  Tragically, you died.  Returning to the mundane world for the day...\r\n", 1))
			raise Exception('normal', "User is DOA.  Bummer.")


