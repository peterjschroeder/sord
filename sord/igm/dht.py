""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please.
 
 # IGM:  The Dark Horse Tavern
 
 # This is pretty close to the original dark horse tavern, found
 # in the L.O.R.D forest - it has however been converted to a IGM
 # cabable format for documentation purposes.  
 
 # ** A few notes:
 #    __init__() is called during server startup - in other words, 
 #               far to early to be of much use.
 #    run() is called from the main sord code when the user invokes
 #          the IGM.  A sord user object is passed as the sole 
 #          argument.  See ../base/user.py for details on the 
 #          standard API.
         
 #    The two imports listed allow for standard display functions,
 #    plus use of things like daily happenings and user stats view
   
 # ** Best practice note:
 #    It's a good idea to throw a tracking log entry in the top of
 #    your run() method.  Ex:
 #       user.log.add("   ** "+user.thisFullname+" entered IGM: IGM Name") 
      
 #    Also, see the example to have the module print it's own
 #    installation options below:   
"""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__sordversion__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
__igmversion__ = "1.0"
__version__ = __igmversion__

if ( __name__ == '__main__' ) :
	print "The Dark Horse Tavern IGM"
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "  To install, add this tuple to igmlist in"
	print "  <sorddir>/sord/igm/__init__.py :"
	print "      ('D', dht.dht(), 'The Dark Horse Tavern')"
else:
	from ..base import func
	from ..game import util
	from ..base import userlib

class dht():
	""" S.O.R.D. IGM :: The Dark Horse Tavern """
	def __init__(self):
		""" Initialize Dark Horse Tavern Instance """
		pass
	
	def main_menu(self):
		""" DHT :: Main Menu"""
		user = self.user
		thismsg  = "\r\n\r\n`2                          Dark Cloak Tavern`.\r\n"
		thismsg += user.art.line()
		thismsg += "  `2A blazing fire warms your heart as well as your body in this fragrant.\r\n"
		thismsg += "  `2roadhouse.  Many a wary traveler has had the good fortune to find this\r\n"
		thismsg += "  `2cozy hostel, to escape the harsh reality of the dense forest for a few\r\n"
		thismsg += "  `2moments.  You notice someone has etched something in the table you are\r\n"
		thismsg += "  `2sitting at.`.\r\n\r\n"
		thismsg += func.menu_2col("(C)onverse With The Patrons", "(D)aily News", 5, 5)
		thismsg += func.menu_2col("(E)xamine Etchings In Table", "(Y)our Stats", 5, 5)
		thismsg += func.menu_2col("(T)alk with Bartender", "(R)eturn to Forest", 5, 5)
		return thismsg
	
	def prompt(self):
		""" DHT :: Main User Prompt"""
		user = self.user
		ptime = func.maketime(user)
		thismenu  = "\r\n  `#The Dark Cloak Tavern`8 (? for menu)`.\r\n"
		thismenu += "  `8(C,D,E,Y,T,R)`.\r\n\r\n"
		thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
		return thismenu

	def run(self, user):
		""" DHT :: Main Run Logic"""
		self.user = user
		user.log.add("   ** "+user.thisFullname+" entered IGM: Dark Horse Tavern") 
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if (  not user.expert ):
					user.write(self.main_menu())
				user.write(self.prompt())
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == '?' ):
				user.write('?')
				user.write(self.main_menu(user))
				skipDisp = True
			elif ( key[0] == 'y' or key[0] == 'Y' ):
				user.write('Y')
				user.write(util.viewstats(user))
				user.pause()
			elif ( key[0] == 'd' or key[0] == 'D' ):
				user.write('D')
				util.dailyhappen(False, user)
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				self.converse()
			elif ( key[0] == 'e' or key[0] == 'E' ):
				user.write('E')
				db = user.dbcon.cursor()
				db.execute("SELECT fullname, fuck FROM users WHERE fuck > 0 ORDER by fuck DESC")
				user.write("\r\n\r\n  `2Users who have gotten lucky:`.\r\n")
				
				for row in db.fetchall():
					if not row:
						user.write("\r\n\r\n  `2What a sad thing - there are no carvings here after all.`.\r\n")
					else:
						for (nombre, data) in row:
							user.write("  `2"+nombre+padnumcol(nombre, 25)+"`0"+str(data)+"`.\r\n")
				user.write("\r\n")
				db.close()
				user.pause()
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				self.chance()
			else:
				skipDisp = True

	def converse(self):
		""" DHT :: Converse with the patrons """
		user = self.user
		output  = "\r\n\r\n  `%Converse with the Patrons`2....`.\r\n"
		output += "`2                                      -=-=-=-=-=-`.\r\n"
		db = user.dbcon.cursor()
		db.execute("SELECT data, nombre FROM (SELECT * FROM dhtpatrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
		for (data, nombre) in db.fetchall():
			output += "    `2"+nombre+" `%says: `2" + data
			output += "\r\n`2                                      -=-=-=-=-=-`0\r\n"
		output += "\r\n  `2Add to the conversation? `8(Y/N) `2[`#N`2] `0: `."
		user.write(output)
		db.close()
		yesno = user.ntcon.recv(2)
		if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
			user.write(func.casebold("\r\n  What say you? :-: ", 2))
			ann = func.getLine(user.ntcon, True)
			user.dbcon.execute("INSERT INTO dhtpatrons ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
			user.dbcon.commit()
			user.write(func.casebold("\r\n  Wisdom added!\r\n", 2))
			user.pause()
		else: 
			user.write('N')
			
	def chance_menu(self):
		""" DHT :: Chance the Bartender - Menu """
		user = self.user
		ptime = func.maketime(user)
		thismenu = func.normmenu("(C)hange Profession")
		thismenu += func.normmenu("(L)earn About Your Enemies")
		thismenu += func.normmenu("(T)alk About Colors")
		thismenu += func.normmenu("(R)eturn to Tavern")
		thismenu += "\r\n  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
		return thismenu
	
	def chance(self):
		""" DHT :: Chance the bartender run logic """
		user = self.user
		header = "\r\n\r\n  `2              Talking To Chance`.\r\n"
		header += "`2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-`.\r\n"
		header += "  `2You seat yourself next to the bartender,`.\r\n"
		header += "  `2for some reason you like him.          `.\r\n\r\n"
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				user.write(header)
				user.write(self.chance_menu())
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				user.write("\r\n\r\n  `2Colors are easy my friend!\r\n\r\n  Just use a ` character followed by one\r\n  of the following:\r\n    `11 `22 `33 `44 `55 `66 `77 `88\r\n    `99 `00 `!! `@@ `## `$$ `%%`.\r\n")
				user.pause()
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write('L')
				whoid = util.finduser(user, "\r\n  `2Get information on who?")
				if ( whoid > 0 ):
					whoName = user.userGetLogin(whoid)
					whoCost = user.level * 100
					user.write("\r\n  `2That will be `0"+str(whoCost)+"`2 gold.  Ok? ")
					yesno = user.ntcon.recv(2)
					if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
						user.write('Y')
						if ( user.gold < whoCost ):
							user.write("\r\n  `2You don't have enough gold jackass!`.\r\n")
						else:
							usertoSee = userlib.sorduser(whoName, user.dbcon, user.ntcon, user.art)
							user.gold -= whoCost
							user.write(util.viewstats(usertoSee))
							del usertoSee
							user.pause()
					else:
						user.write('N')
						user.write("\r\n  `2Ok.  You got it.`.\r\n")
				else: 
					user.write("\r\n  `2Ok.  Nevermind.`.\r\n")
			elif ( key[0] == 'c' or key[0] == 'C' ):
				user.write('C')
				user.write(func.casebold("\r\n  Pick that which best describes your childhood.\r\n  From an early age, you remember:\r\n\r\n", 2))
				user.write(func.normmenu("(D)abbling in the mystical forces"))
				user.write(func.normmenu("(K)illing a lot of woodland creatures"))
				user.write(func.normmenu("(L)ying, cheating, and stealing from the blind"))
				thisLooper = False
				while ( not thisLooper ):
					user.write(func.casebold("\r\n  Your Choice (D/K/L) :-: ", 2))
					key = user.ntcon.recv(2)
					if not key: break
					if ( key[0] == 'k' or key[0] == 'K' ):
						user.write('K')
						user.cls = 1
						thisLooper = True
						user.write(func.casebold("\r\n  Welcome warrior to the ranks of the Death Knights!\r\n", 2))
					if ( key[0] == 'd' or key[0] == 'D' ):
						user.write('D')
						user.cls = 2
						thisLooper = True
						user.write(func.casebold("\r\n  Feel the force young jedi.!\r\n", 2))
					if ( key[0] == 'l' or key[0] == 'L' ):
						user.write('L')
						user.cls = 3
						thisLooper = True
						user.write(func.casebold("\r\n  You're a real shitheel, you know that?\r\n", 2))
			else:
				skipDisp = True
	
