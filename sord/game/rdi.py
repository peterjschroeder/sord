#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains the Red Dragon Inn

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import random, time, re
from ..base import func
from ..base import userlib
from . import data
from . import util

class rdi():
	""" S.O.R.D. :: Red Dragon Inn """
	def __init__(self, user):
		""" Initialize new RDI instance """
		self.user = user

	def menu_main(self):
		""" Main Menu """
		thismenu  = "\r\n\r\n  `%Saga of the Red Dragon - `2The Inn`.\r\n"
		thismenu += self.user.art.blueline();
		thismenu += "`2  You enter the inn and are immediately hailed by several of the patrons.\r\n"
		thismenu += "`2  You respond with a wave and scan the room.  The room is filled with\r\n"
		thismenu += "`2  smoke from the torches that line the walls.  Oaken tables and chairs\r\n"
		thismenu += "`2  are scattered across the room.  You smile as the well-rounded Violet\r\n"
		thismenu += "`2  brushes by you....`.\r\n\r\n"
		thismenu += func.menu_2col("(C)onverse with the patrons", "(D)aily News", 5, 5)
		if ( self.user.sex == 1 ):
			flirtwith = "`#Violet"
		else:
			flirtwith = "Seth Able"
		thismenu += func.menu_2col("(F)lirt with "+flirtwith, "(T)alk to the Bartender", 5, 5)
		thismenu += func.menu_2col("(G)et a Room", "(V)iew Your Stats", 5, 5)
		thismenu += func.menu_2col("(H)ear Seth Able The Bard", "(M)ake Announcment", 5, 5)
		thismenu += func.menu_2col("(R)eturn To Town", "", 5, 5)
		return thismenu

	def prompt(self):
		""" User Prompt"""
		ptime = func.maketime(self.user)
		thismenu  = "\r\n  `#The Red Dragon Inn`8 (? for menu)`.\r\n"
		thismenu += "  `8(C,D,F,T,G,V,H,M,R)`.\r\n\r\n"
		thismenu += "  `2Your command, `0" + self.user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
		return thismenu

	def run(self):
		""" Red Dragon Inn, main loop """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if (  not user.expert ):
					user.write(self.menu_main())
				user.write(self.prompt())
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == '?' ):
				user.write('?')
				if ( user.expert ):
					user.write(self.menu_main())
			elif ( key[0] == 'd' or key[0] == 'D' ):
				user.write('D')
				util.dailyhappen(False, user)
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				self.bartend()
			elif ( key[0] == 'v' or key[0] == 'V' ):
				user.write('V')
				user.write(util.viewstats(user))
				user.pause()
			elif ( key[0] == 'm' or key[0] == 'M' ):
				user.write('M')
				util.announce(user)
			elif ( key[0] == 'f' or key[0] == 'F' ):
				user.write('F')
				if ( user.flirt ):
					user.write(func.casebold("\r\n  You have already flirted once today\r\n", 2))
				else:
					self.flirt()
				user.pause()
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				self.converse()
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write('H')
				self.menu_bard()
			elif ( key[0] == 'g' or key[0] == 'G' ):
				user.write('G')
				self.getroom()
			elif ( key[0] == 'e' or key[0] == 'E' ):
				if ( user.jennielevel == 4 and not user.jennieused ):
					user.jennielevel = 0
					user.jennieused = True
					user.write("\r\n  `2Jennie, eh?  Describe Her :`. ")
					desc = func.getLine(user.ntcon, True)
					if ( desc == "babe" or desc == "BABE" ):
						user.write("\r\n  `2I agree!`.\r\n")
						user.ffight += 1
					elif ( desc == "cool" or desc == "COOL" ):
						user.write("\r\n  `2Yes, yes she is.`.\r\n")
						user.charm += 1
					elif ( desc == "dumb" or desc == "DUMB" ):
						user.write("\r\n  `1No, *you're* dumb!`.\r\n")
					elif ( desc == "dung" or desc == "DUNG" ):
						user.write("\r\n  `1Be a frog stoopid.`.\r\n")
					elif ( desc == "fair" or desc == "FAIR" ):
						user.flirt = 0
						user.write("\r\n  `1Yeah, a bit more than that though.`.\r\n")
					elif ( desc == "foxy" or desc == "FOXY" ):
						user.gems += 1
						user.write("\r\n  `2And how!`.\r\n")
					elif ( desc == "gift" or desc == "GIFT" ):
						addskill = user.getSkillPoint(user.cls) - user.getSkillUse(user.cls)
						if ( addskill > 0 ):
							user.updateSkillUse(user.cls, addskill)
						user.write("\r\n  `2Ok, she can give you a gift.`.\r\n")
					elif ( desc == "hott" or desc == "HOTT" ):
						user.write("\r\n  `2Hell yeah she is!`.\r\n")
						user.hp = user.hpmax + (user.hpmax / 5)
					elif ( desc == "lady" or desc == "LADY" ):
						user.write("\r\n  `2She's a lady... woo woo woo`.\r\n")
						user.gold += user.level * 1000
					elif ( desc == "nice" or desc == "NICE" or desc == "star" or desc == "STAR" ):
						user.write("\r\n  `2Duh.`.\r\n")
					elif ( desc == "sexy" or desc == "SEXY" ):
						user.write("\r\n  `2Indeed.`.\r\n")
						user.pfight += 1
					elif ( desc == "ugly" or desc == "UGLY" ):
						user.write("\r\n  `2You're an ass.`.\r\n")
						user.hp = 1
						raise Exception('normal', "How dare you insult Jennie!")
					else:
						user.write("\r\n  `4Better luck next time.`.\r\n")
			else:
				skipDisp = True

	def getroom(self):
		""" Red Dragon Inn Get a Room """
		user = self.user
		price = user.level * 400
		user.write("\r\n  `2The bartender approaches you at the mention of a room.`.\r\n")
		user.write("  `5\"You want a room, eh?  That'll be `#"+str(price)+"`5 gold!\"`.\r\n")
		user.write("  `2Do you agree? `0: `.")
		yesno = user.ntcon.recv(2)
		if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
			user.ntcon.send('Y')
			if ( user.gold < price ):
				user.write("\r\n  `5\"How bout you find yourself a nice stretch of cardboard box ya bum?`.\r\n")
			else:
				user.gold -= price
				user.write("\r\n  `2Enjoy your stay.  At next login, you will automatically leave the inn.`.\r\n")
				user.atinn = 1
				raise Exception('normal', "User got a room.  Enjoy.")
		else:
			user.ntcon.send('N')
			user.write("\r\n  `5\"Suit yourself...\"`.\r\n")

	def converse(self):
		""" Converse with patrons """
		user = self.user
		db = user.dbcon.cursor()
		output  = "\r\n\r\n  `%Converse with the Patrons`2....`.\r\n"
		output += "`2                                      -=-=-=-=-=-`.\r\n"
		db.execute("SELECT data, nombre FROM (SELECT * FROM patrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
		for (data, nombre) in db.fetchall():
			output += "    `2"+nombre+" `%says: `2" + data
			output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
		output += "\r\n  `2Add to the conversation? `8[Y/N] `2[`#N`2] `0: `."
		db.close()
		user.write(output)
		yesno = user.ntcon.recv(2)
		if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
			user.write('Y')
			user.write(func.casebold("\r\n  What say you? :-: ", 2))
			ann = func.getLine(user.ntcon, True)
			user.dbcon.execute("INSERT INTO patrons ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
			user.dbcon.commit()
			user.write(func.casebold("\r\n  Wisdom added!\r\n", 2))
			user.pause()
		else:
			user.write('N')

	def menu_bard(self):
		""" Talk with the bard """
		user = self.user
		ptime = func.maketime(user)
		thismenu  = "\r\n\r\n  `%Saga of the Red Dragon - `2Seth Able`.\r\n"
		thismenu += user.art.blueline()
		thismenu += "  `2You stumble over to a dank corner of the Inn.\r\n  Seth able looks at you expectantly...\r\n\r\n"
		thismenu += func.normmenu("(A)sk Seth Able to Sing")
		thismenu += func.normmenu("(R)eturn to the Inn")
		thismenu += "\r\n  `#Seth Able the Bard `8(A,R,Q) (? for menu)`.\r\n\r\n"
		thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				user.write(thismenu)
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			if ( key[0] == 'r' or key[0] == 'R' or key[0] == 'q' or key[0] == 'Q' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == 'a' or key[0] == 'A' ):
				user.write('A')
				self.bard_listen()
			else:
				skipDisp = True

	def bard_listen(self):
		""" Hear the bard sing"""
		user = self.user
		if ( not user.sung ):
			user.write("\r\n  `2Seth thinks for a moment, picks up his lute, and begins...\r\n\r\n")
			songnum = random.randint(1, 10)
			for lyrics in data.thebard[songnum][0]:
				time.sleep(1)
				lyrics = re.sub("\.\.\.\"", "`7...\"`2", lyrics)
				lyrics = re.sub("\"\.\.\.", "`7\"...`.", lyrics)
				lyrics = re.sub("XX", "`@"+user.thisFullname+"`2", lyrics)
				user.write("    "+lyrics+"\r\n")
			user.write("\r\n  `0"+data.thebard[songnum][1][0]+"`.\r\n")
			user.write("\r\n  `@"+data.thebard[songnum][1][1]+"`.\r\n\r\n")
			user.dbcon.execute("UPDATE users SET "+data.thebard[songnum][2]+" WHERE userid = ?", (user.thisUserID, ))
			user.dbcon.commit()
			user.sung = 1
			user.pause()
		else:
			user.write(func.casebold("\r\n  Seth says:  I'm a bit tired, maybe tommorow...\r\n", 2))

	def flirt(self):
		""" Flirt initiator. """
		self.user.write(self.menu_flirt())
		self.user.write("\n  `2Your Choice? `0: `.")
		if ( self.user.sex == 1 ):
			self.flirt_violet()
		else:
			self.flirt_seth()

	def menu_flirt(self):
		""" Show appropriate flirting menu per user.sex """
		thismenu = "\r\n"
		if (self.user.sex == 1):
			thismenu = self.user.art.violet()
		else:
			for saying in data.flirts[self.user.sex]:
				thismenu += func.normmenu(saying[1])
		return thismenu

	def flirt_seth(self):
		"""Flirt with the bard"""
		user = self.user
		thisTry = False
		thisScrew = False
		thisQuit = False
		while ( not thisQuit ):
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'w' or key[0] == 'W' ):
				user.write('W')
				thisRun = 0
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'f' or key[0] == 'F' ):
				user.write('F')
				thisRun = 1
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'd' or key[0] == 'D' ):
				user.write('D')
				thisRun = 2
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'a' or key[0] == 'A' ):
				user.write('A')
				thisRun = 3
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'k' or key[0] == 'K' ):
				user.write('K')
				thisRun = 4
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				thisRun = 5
				thisQuit = True
				thisTry = True
				thisScrew = True
			elif ( key[0] == 'r' or key[0] == 'R' or key[0] == 'n' or key[0] == 'N' or key[0] == 'q' or key[0] == 'Q' ):
				user.write('N')
				thisQuit = True
			else:
				pass
		if ( thisTry ):
			user.write("\r\n  `2"+data.fresult[1][thisRun][2]+"`0\r\n")
			time.sleep(1)
			user.write("\r\n  `%...")
			time.sleep(1)
			user.write("`1AND`%")
			time.sleep(1)
			user.write("...`.")
			if ( user.charm > data.fresult[2][thisRun][0] ):
				thisExp = user.level * data.fresult[2][thisRun][1]
				user.exp += thisExp
				user.flirt = 1
				if ( thisScrew ):
					user.fuck += 1
				user.write("\r\n  `@"+data.fresult[2][thisRun][3]+"\r\n  `2You gain `0"+str(thisExp)+"`2 experience.`.\r\n")
			else:
				thisScrew = False
				user.write("\r\n  `9"+data.fresult[2][thisRun][4]+"`.\r\n")
	
			if ( thisScrew ):
				vd = ['herpes', 'crabs', 'ghonnereah']
				vdc = random.randint(0, 2)
				user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", ("`9"+user.thisFullname+"`2 got a little somethin somethin today.  `4And "+vd[vdc]+".'", user.getgday()))
				user.dbcon.commit()

	def flirt_violet(self):
		"""Flirt with the barmaid"""
		user = self.user
		thisTry = False
		thisScrew = False
		thisQuit = False
		while ( not thisQuit ):
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'w' or key[0] == 'W' ):
				user.write('W')
				thisRun = 0
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'k' or key[0] == 'K' ):
				user.write('K')
				thisRun = 1
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'p' or key[0] == 'P' ):
				user.write('P')
				thisRun = 2
				thisQuit = True
				thisTry = True
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				thisRun = 3
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'g' or key[0] == 'G' ):
				user.write('G')
				thisRun = 4
				thisQuit = True
				thisTry = True
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				thisRun = 5
				thisQuit = True
				thisTry = True
				thisScrew = True
			elif ( key[0] == 'r' or key[0] == 'R' or key[0] == 'n' or key[0] == 'N' or key[0] == 'q' or key[0] == 'Q' ):
				user.write('N')
				thisQuit = True
			else:
				pass
		if ( thisTry ):
			user.write("\r\n  `2"+data.fresult[1][thisRun][2]+"`.\r\n")
			time.sleep(1)
			user.write("\r\n  `%...")
			time.sleep(1)
			user.write("`1AND`%")
			time.sleep(1)
			user.write("...`.")
			if ( user.charm > data.fresult[1][thisRun][0] ):
				thisExp = user.level * data.fresult[1][thisRun][1]
				user.exp += thisExp
				user.flirt = 1
				if ( thisScrew ):
					user.fuck += 1
				user.write("\r\n  `@"+data.fresult[1][thisRun][3]+"\r\n  `2You gain `0"+str(thisExp)+"`2 experience.`.\r\n")
			else:
				thisScrew = False
				user.write("\r\n  `9"+data.fresult[1][thisRun][4]+"`.\r\n")
	
			if ( thisScrew ):
				vd = ['herpes', 'crabs', 'ghonnereah']
				vdc = random.randint(0, 2)
				user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", ("`0"+user.thisFullname+"`2 got a little somethin somethin today.  `4And "+vd[vdc]+".'", user.getgday()))
				user.dbcon.commit()

	def menu_bartend(self):
		""" Show bartender menu """
		ptime = func.maketime(self.user)
		thismenu  = "\r\n\r\n  `%Saga of the Red Dragon - `2Bartender`.\r\n"
		thismenu += self.user.art.blueline()
		thismenu += "  `2The bartender escorts you into a back\r\n"
		thismenu += "  `2room.  `5\"I have heard yer name before kid...\r\n"
		thismenu += "  `5what do ya want to talk about?\"`.\r\n\r\n"
		thismenu += func.normmenu("(V)iolet")
		thismenu += func.normmenu("(G)ems")
		thismenu += func.normmenu("(B)ribe")
		thismenu += func.normmenu("(C)hange your name")
		thismenu += func.normmenu("(R)eturn to Bar")
		thismenu += "\r\n  `#\"Well?\" `2The bartender inquires. `8(V,G,B,C,R) (? for menu)`.\r\n"
		thismenu += "  `2Your command, `0" + self.user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
		return thismenu

	def bartend(self):
		""" Bartender Logic """
		user = self.user
		thisQuit = False
		dispSkip = False
		if ( user.level < 2 ):
			user.write("\r\n  `2Never heard of ya...  Come back when you've done something.`.\r\n")
			user.pause()
			thisQuit = True
		while ( not thisQuit ):
			if ( not dispSkip ):
				user.write(self.menu_bartend())
			dispSkip = False
			key = user.ntcon.recv(2)
			if not key: break
			if ( key[0] == 'r' or key[0] == 'R' or key[0] == 'q' or key[0] == 'Q' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == 'v' or key[0] == 'V' ):
				user.write('V')
				user.write("\r\n\r\n  `5\"Ya want to know about `#Violet`5 do ya?  She is every warrior's")
				user.write("\r\n  `5wet dream...But forget it, Lad, she only goes for the type")
				user.write("\r\n  `5mof guy who would help old peple...\"`.\r\n")
				user.pause()
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				user.write("\r\n\r\n  `5\"Ya wanna change your name, eh?  Yeah...`.")
				if ( user.cls == 1 ):
					thisTitle = "the Death Knight"
				elif ( user.cls == 2 ):
					thisTitle = "the Magiciain"
				else:
					thisTitle = "the Thief"
				thisPrice = user.level * 500
				user.write("\r\n  `5"+user.thisFullname+"`2 "+thisTitle+" does sound kinda funny...`.")
				user.write("\r\n  `5mit would cost ya "+str(thisPrice)+" gold... Deal?\"`.")
				user.write("\r\n  `2Change your name? `8[Y/N] `2[`#N`2]`. ")
				yesno = user.ntcon.recv(2)
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					user.write('Y')
					if ( user.gold < thisPrice ):
						func.slowecho("\r\n  `5\"Then I suggest you go find some more gold...\"`.\r\n")
					else:
						thisGoodName = False;
						user.write("\r\n  `2What'll it be? `0: `.")
						ann = func.getLine(user.ntcon, True)
						if ( ann == "" ):
							thisGoodName = False
						elif ( ann.rfind('barak') >= 0 ):
							user.write("\r\n  `1** `5Naw, the real Barak would decapitate you if he found out. `1** `5\r\n")
						elif ( ann.rfind('seth able') >= 0 ):
							user.write("\r\n  `1** `5You are not God! `1** `5\r\n")
						elif ( ann.rfind('red dragon') >= 0 ):
							user.write("\r\n  `1** `5Oh go plague some other land! `1** `5\r\n")
						elif ( ann.rfind('seth') >= 0 ):
							user.write("\r\n  `1** `5You are not Seth Able!  Don't take his name in vain! `1** `5\r\n")
						elif ( ann.rfind('turgon') >= 0 ):
							user.write("\r\n  `1** `5Haw.  Hardly - Turgon has muscles. `1** `5\r\n")
						elif ( ann.rfind('violet') >= 0 ):
							user.write("\r\n  `1** `5Haw.  Hardly - Violet has breasts. `1** `5\r\n")
						elif ( ann.rfind('dragon') >= 0 ):
							user.write("\r\n  `1** `5You ain't Bruce Lee, so get out! `1** `5\r\n")
						elif ( ann.rfind('bartender') >= 0 ):
							user.write("\r\n  `1** `5Nah, the bartender is smarter than you! `1** `5\r\n")
						elif ( ann.rfind('chance') >= 0 ):
							user.write("\r\n  `1** `5Why not go take a chance with a rattlesnake? `1** `5\r\n")
						else:
							user.write("\r\n  `2Name Changed.`.\r\n")
							user.dbcon.execute("UPDATE users SET fullname = ? WHERE userid = ?", (ann, user.thisUserID))
							user.dbcon.commit()
							user.gold -= thisPrice
							user.thisFullname = ann
				else:
					user.write("\r\n\r\n  `5\"Fine...Keep your stupid name...See if I care...\"`.\r\n")
				user.pause()
			elif ( key[0] == 'd' or key[0] == 'D' ):
				if ( user.level == 12 ):
					user.write('D')
					user.write("\r\n\r\n  `2A `9Red `2Dragon eh?  Have you tried to `0S`2earch?`.\r\n")
					user.pause()
				else:
					dispSkip = True
			elif ( key[0] == 'g' or key[0] == 'G' ):
				user.write('G')
				user.write("\r\n\r\n  `5\"You have `%Gems`5, eh?  I'll give ya a pint of magic elixer for two.\"`.\r\n")
				user.write("  `2Buy how many elixers? : `.")
				try:
					number = int(func.getLine(user.ntcon, True))
					user.write(str(number))
				except ValueError:
					number = 0
					user.write('0')
				if ( number > 0 ):
					if ( number * 2 > user.gems ):
						user.write("\r\n\r\n  `1You don't have that many gems!`.\r\n")
					else: # /*sell and process elixer */
						user.write("\r\n\r\n  `2Increase which stat?`.\r\n")
						user.write(func.normmenu("(H)itpoints"))
						user.write(func.normmenu("(S)trength"))
						user.write(func.normmenu("(V)itality"))
						user.write(func.normmenu("(N)evermind"))
						tinyQuit = False
						while( not tinyQuit ):
							user.write("  `2Choose : `.")
							thisType = user.ntcon.recv(2)
							if ( thisType[0] == 'n' or thisType[0] == 'N' or thisType[0] == 'q' or thisType[0] == 'Q' or thisType[0] == 'r' or thisType[0] == 'R' ):
								user.write('N')
								tinyQuit = True
							if ( thisType[0] == 'H' or thisType[0] == 'h' ):
								user.write('H')
								user.hpmax += number
								user.hp = user.hpmax
								user.gems -= ( number * 2 )
								user.write("\r\n  `2You feel as if your stamina is greater\r\n")
								tinyQuit = True
							if ( thisType[0] == 'S' or thisType[0] == 's' ):
								user.write('S')
								user.str += number
								user.gems -= ( number * 2 )
								user.write("\r\n  `2You feel as if your strength is greater\r\n")
								tinyQuit = True
							if ( thisType[0] == 'v' or thisType[0] == 'V' ):
								user.write('V')
								user.defence += number
								user.gems -= ( number * 2 )
								user.write("\r\n  `2You feel as if your vitality is greater\r\n")
								tinyQuit = True
						user.write("\r\n  `2Pleasure doing business with you!`.\r\n")
			elif ( key[0] == 'b' or key[0] == 'B' ):
				user.write('B')
				user.write("\r\n\r\n  `2Bribe me to kick someone out of thier room, eh?`.\r\n")
				kickID = util.finduser(user, "\r\n  `2Who will it be?")
				if ( kickID > 0 ):
					kickName = user.userGetLogin(kickID)
					kickCost = user.level * 1500
					usertoKick = userlib.sorduser(kickName, user.dbcon, user.ntcon, user.art)
					if ( usertoKick.atinn == True ):
						user.write("\r\n  `2That will be `0"+str(kickCost)+"`2 gold. Ok? `8(Y/N) `2[`#N`2] `0")
						yesno = user.ntcon.recv(2)
						if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
							user.write('Y')
							if ( user.gold < kickCost ):
								user.write("\r\n  `2You don't have enough gold jackass!`.\r\n")
							else:
								user.gold -= kickCost
								if ( usertoKick.level + 2 < user.level ):
									user.write("\r\n  `2I don't like bullies.  Thanks for the nice tip!`.\r\n")
								else:
									usertoKick.atinn = 0
									user.write("\r\n  `2Booted to the killing fields. Better Hurry...`.\r\n")
					else:
						user.write("\r\n  `2They aren't staying here...`.\r\n")
					del usertoKick
				else:
					user.write("\r\n  `2Right then, forget I ever mentioned this.`.\r\n")
				user.pause()
			else:
				dispSkip = True



