#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all online player editor.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import re
from . import func
from . import userlib
from ..game import data

class editor():
	""" S.O.R.D. Player editor """

	def __init__(self, user):
		""" Initialize new editor instance """
		self.cuser = user
		self.euser = userlib.sorduser(user.config.gameadmin, user.dbcon, user.ntcon, user.art, user.config, user.log, user.linespeed, user.noise)
	
	def main_menu(self):
		""" Main Menu """
		if ( self.euser.sex == 1 ):
			sexo = "Male"
		else:
			sexo = "Female"
		thismsg =  "\r\n" + self.makecenter("** Saga Of The Red Dragon - User Editor v."+self.cuser.config.version+" **", 1) + "\r\n"
		thismsg += self.makecenter("Account Number: "+str(self.euser.thisUserID), 7) + "\r\n\r\n"
		thismsg += self.makeentry(1, 'Name', 1, self.euser.thisFullname) + self.makeentry(2, 'Level', 2, self.euser.level) + "\r\n"
		thismsg += self.makeentry(3, 'Login Name', 1, self.euser.thisUserName) + self.makeentry(4, 'Hit Points', 2, self.euser.hp) + "\r\n"
		thismsg += self.makeentry(5, 'Experience', 1, self.euser.exp) + self.makeentry(6, 'Hit Max', 2, self.euser.hpmax) + "\r\n"
		thismsg += self.makeentry(7, 'Weapon', 1, data.weapon[self.euser.weapon], False) + self.makeentry(8, 'Weapon Number', 2, self.euser.weapon) + "\r\n"
		thismsg += self.makeentry(9, 'Armor', 1, data.armor[self.euser.armor], False) + self.makeentry(0, 'Armor Number', 2, self.euser.armor) + "\r\n"
		thismsg += self.makeentry('A', 'Seen Master', 1, self.euser.master) + self.makeentry('B', 'Forest Fights', 2, self.euser.ffight) + "\r\n"
		thismsg += self.makeentry('C', 'Player Fights', 1, self.euser.pfight) + self.makeentry('D', 'Sex', 2, sexo) + "\r\n"
		thismsg += self.makeentry('E', 'Defence', 1, self.euser.defence) + self.makeentry('F', 'Gems', 2, self.euser.gems) + "\r\n"
		thismsg += self.makeentry('G', 'Strength', 1, self.euser.str) + self.makeentry('H', 'Charm', 2, self.euser.charm) + "\r\n"
		thismsg += self.makeentry('I', 'Seen Flirt', 1, self.euser.flirt) + self.makeentry('J', 'Seen Bard', 2, self.euser.sung) + "\r\n"
		thismsg += self.makeentry('K', 'Class', 1, '('+str(self.euser.cls)+') '+data.classes[self.euser.cls]) + self.makeentry('L', 'Dragon Kills', 2, self.euser.dragon) + "\r\n"
		thismsg += self.makeentry('M', 'Gold in Hand', 1, self.euser.gold) + self.makeentry('N', 'Player Kills', 2, self.euser.pkill) + "\r\n"
		thismsg += self.makeentry('O', 'Gold in Bank', 1, self.euser.bank) + self.makeentry('P', 'At The Inn', 2, self.euser.atinn) + "\r\n"
		thismsg += self.makeentry('R', 'Has Horse', 1, self.euser.horse) + self.makeentry('S', 'Has Fairy', 2, self.euser.fairy) + "\r\n"
		thismsg += self.makeentry('T', 'Player Alive', 1, self.euser.alive) + self.makeentry('U', 'Times Laid', 2, self.euser.fuck) + "\r\n"
		thismsg += "\r\n  `2(`#$`2) Edit Skills   (`#[`2) Previous Player   (`#]`2) Next Player   (`##`2) Jump to Player\r\n"
		thismsg += self.makecenter("Input key to change / toggle, 'Q' to Quit", 7) + "\r\n"
		return thismsg

	def skill_menu(self):
		""" Skills Menu """
		thismsg  = "\r\n" + self.makecenter("** Saga Of The Red Dragon - Skills Editor v."+self.cuser.config.version+" **", 1) + "\r\n"
		thismsg += self.makecenter("Account Number: "+str(self.euser.thisUserID)+" / "+self.euser.thisFullname, 7) + "\r\n\r\n"
		thismsg += self.makecenter("*** Death Knight Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(1, 'Skill Points', 1, self.euser.getSkillPoint(1)) + self.makeentry('A', 'Uses Today', 2, self.euser.getSkillUse(1)) + "\r\n\r\n"
		thismsg += self.makecenter("*** Magical Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(2, 'Skill Points', 1, self.euser.getSkillPoint(2)) + self.makeentry('B', 'Uses Today', 2, self.euser.getSkillUse(2)) + "\r\n\r\n"
		thismsg += self.makecenter("*** Thief Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(3, 'Skill Points', 1, self.euser.getSkillPoint(3)) + self.makeentry('C', 'Uses Today', 2, self.euser.getSkillUse(3)) + "\r\n\r\n"
		thismsg += self.makecenter("Input key to change, 'R' to Return to main", 7) + "\r\n"
		return thismsg

	def skill_logic(self):
		""" Skills Run Logic """
		thisQuit = False
		skipDisp = False
		while ( not thisQuit):
			if ( not skipDisp ):
				self.cuser.write(self.skill_menu())
			skipDisp = False
			choice = self.cuser.ntcon.recv(2)
			if not choice: break
			elif ( choice[0] == 'r' or choice[0] == 'R' or choice[0] == 'q' or choice[0] == 'Q' ):
				thisQuit = True
			elif ( choice[0] == '1' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillPoint(1)
						self.euser.updateSkillPoint(1,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '2' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillPoint(2)
						self.euser.updateSkillPoint(2,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '3' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillPoint(3)
						self.euser.updateSkillPoint(3,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'a' or choice[0] == 'A' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillUse(1)
						self.euser.updateSkillUse(1,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'b' or choice[0] == 'B' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillUse(2)
						self.euser.updateSkillUse(2,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'c' or choice[0] == 'C' ):
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - self.euser.getSkillUse(3)
						self.euser.updateSkillUse(3,hptoadd)
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			else:
				skipDisp = True

	def run(self):
		""" Main run logic """
		thisQuit = False
		skipDisp = False
		while ( not thisQuit):
			if ( not skipDisp ):
				self.cuser.write(self.main_menu())
			skipDisp = False
			choice = self.cuser.ntcon.recv(2)
			if not choice: break
			elif ( choice[0] == 'q' or choice[0] == 'Q' ): # Quit
				thisQuit = True
			elif ( choice[0] == '1' ): # Full Name
				thisIn = func.getLine(self.cuser.ntcon, True, func.casebold("New Full Name :-:", 2))
				if not thisIn: break
				else:
					self.cuser.dbcon.execute("UPDATE users SET fullname = ? WHERE userid = ?", (thisIn, self.euser.thisUserID))
					self.cuser.dbcon.commit()
					self.euser.thisFullname = thisIn
			elif ( choice[0] == '2' ): # Level
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Level :-:", 2)))
					if ( thisIn > 0 and thisIn < 13 ):
						self.euser.level = thisIn
					else:
						self.cuser.write(func.casebold("\r\nNot a valid level!", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid level", 1))
					self.cuser.pause()
			elif ( choice[0] == '3' ): # Login Name
				thisIn = func.getLine(self.cuser.ntcon, True, func.casebold("New Login Name :-:", 2))
				if not thisIn: break
				else:
					self.cuser.dbcon.execute("UPDATE users SET username = ? WHERE userid = ?", (thisIn, self.euser.thisUserID))
					self.cuser.dbcon.commit()
					self.euser.thisUserName = thisIn
			elif ( choice[0] == '4' ): # HP
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Hit Points :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.hp = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '5' ): # Experience
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Experience Points :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.exp = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '6' ): # Max HP
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Max Hit Points :-:", 2)))
					if ( thisIn > 0 ):
						self.euser.hpmax = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '8' or choice[0] == '7' ): # Weapon
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Weapon Number :-:", 2)))
					if ( thisIn >= 0 and thisIn < 16 ):
						self.euser.weapon = thisIn
					else:
						self.cuser.write(func.casebold("\r\nNot a valid choice", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '0' or choice[0] == '9' ): # Armor
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Armor Number :-:", 2)))
					if ( thisIn >= 0 and thisIn < 16 ):
						self.euser.armor = thisIn
					else:
						self.cuser.write(func.casebold("\r\nNot a valid choice", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'a' or choice[0] == 'A' ): # Seen Master
				if ( self.euser.master ):
					self.euser.master = 0
				else:
					self.euser.master = 1
			elif ( choice[0] == 'b' or choice[0] == 'B' ): # Forest Fights
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Forest Fights :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.ffight = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'c' or choice[0] == 'C' ): # Player Fights
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Player Fights :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.pfight = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'd' or choice[0] == 'D' ): # Sex
				if ( self.euser.sex == 1 ):
					self.euser.sex = 2
				else:
					self.euser.sex = 1
			elif ( choice[0] == 'e' or choice[0] == 'E' ): # Defense
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Defence :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.defence = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'f' or choice[0] == 'F' ): # Gems
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Gems :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.gems = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'g' or choice[0] == 'G' ): # Strength
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Strength :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.str = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'h' or choice[0] == 'H' ): # Charm
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Charm :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.charm = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'i' or choice[0] == 'I' ): # Flirt
				if ( self.euser.flirt ):
					self.euser.flirt = 0
				else:
					self.euser.flirt = 1
			elif ( choice[0] == 'j' or choice[0] == 'J' ): # Bard
				if ( self.euser.sung ):
					self.euser.sung = 0
				else:
					self.euser.sung = 1
			elif ( choice[0] == 'k' or choice[0] == 'K' ): # Class
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Class Number :-:", 2)))
					if ( thisIn > 0 and thisIn < 4 ):
						self.euser.cls = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be 1, 2, or 3", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'l' or choice[0] == 'L' ): # Dragon
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Dragon Kills :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.dkill = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'm' or choice[0] == 'M' ): # Gold
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Gold in Hand :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.gold = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'n' or choice[0] == 'N' ): # Player Kills
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Player Kills :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.pkill = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'o' or choice[0] == 'O' ): # Bank
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Gold in Bank :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.bank = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == 'p' or choice[0] == 'P' ): # Inn
				if ( self.euser.atinn ):
					self.euser.atinn = 0
				else:
					self.euser.atinn = 1
			elif ( choice[0] == 'r' or choice[0] == 'R' ): # Horse
				if ( self.euser.horse ):
					self.euser.horse = 0
				else:
					self.euser.horse = 1
			elif ( choice[0] == 's' or choice[0] == 'S' ): # Fairy
				if ( self.euser.fairy ):
					self.euser.fairy = 0
				else:
					self.euser.fairy = 1
			elif ( choice[0] == 't' or choice[0] == 'T' ): # Dead
				if ( self.euser.alive ):
					self.euser.alive = 0
				else:
					self.euser.alive = 1
			elif ( choice[0] == 'u' or choice[0] == 'U' ): # Fucks
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("New Times Laid :-:", 2)))
					if ( thisIn >= 0 ):
						self.euser.fuck = thisIn
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == ']' ): # Next
				newLogin = self.cuser.userGetLogin(self.euser.thisUserID + 1)
				try:
					if ( newLogin == 0 ):
						self.cuser.write(func.casebold("\r\nLast Record Reached", 1))
						self.cuser.pause()
					else:
						self.euser = userlib.sorduser(newLogin, self.cuser.dbcon, self.cuser.ntcon, self.cuser.art, self.cuser.config, self.cuser.log, self.cuser.linespeed, self.cuser.noise)
				except ValueError:
					pass
			elif ( choice[0] == '[' ): # Prev
				newLogin = self.cuser.userGetLogin(self.euser.thisUserID - 1)
				try:
					if ( newLogin == 0 ):
						self.cuser.write(func.casebold("\r\nFirst Record Reached", 1))
						self.cuser.pause()
					else:
						self.euser = userlib.sorduser(newLogin, self.cuser.dbcon, self.cuser.ntcon, self.cuser.art, self.cuser.config, self.cuser.log, self.cuser.linespeed, self.cuser.noise)
				except ValueError:
					pass
			elif ( choice[0] == '#' ): # By Rec Num
				try:
					thisIn = int(func.getLine(self.cuser.ntcon, True, func.casebold("Jump to User Number :-:", 2)))
					if ( thisIn >= 0 ):
						newLogin = self.cuser.userGetLogin(thisIn)
						try:
							if ( newLogin == 0 ):
								self.cuser.write(func.casebold("\r\nNon-valid Record", 1))
								self.cuser.pause()
							else:
								self.euser = userlib.sorduser(newLogin, self.cuser.dbcon, self.cuser.ntcon, self.cuser.art, self.cuser.config, self.cuser.log, self.cuser.linespeed, self.cuser.noise)
						except ValueError:
							pass
					else:
						self.cuser.write(func.casebold("\r\nMust be positive", 1))
						self.cuser.pause()
				except ValueError:
					self.cuser.write(func.casebold("\r\nNot a valid number", 1))
					self.cuser.pause()
			elif ( choice[0] == '$' ): # Edit Skills
				self.skill_logic()
			else:
				skipDisp = True

	def makecenter(self, text, color):
		""" Center a string of text """
		col = 40 - (len(text) / 2)
		ittr = 0
		retval = ""
		while ( ittr < col ):
			retval += " "
			ittr += 1
		return retval + func.casebold(text, color)
	
	def makeentry(self, option, text, col, value, editable = True):
		""" Make an editor menu entry """
		thisentry = ""
		if ( col == 1 ):
			thisentry += "  "
		fcol = 14 - len(text)
		ittr = 0
		retval = ""
		while ( ittr < fcol ):
			retval += " "
			ittr += 1
		thisentry += "`2(`#"+str(option)+"`2) "+text+retval+":\x1b[1"
		if ( not editable ):
			thisentry += ";30"
		thisentry += "m"+str(value)
		if ( col == 1 ):
			try:
				lvalue = re.sub('`.', '', value)
			except:
				lvalue = value
			xcol = 25 - len(str(lvalue))
			ittr = 0
			while ( ittr < xcol ):
				thisentry += " "
				ittr += 1
		return thisentry + "`."
