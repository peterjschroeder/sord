#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains basic player in-game utility displays / functions

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
import re
from ..base import func
from ..base import userlib
from . import data

def readmail(user):
	""" Read waiting in-game e-mail. Very simple. """
	db = user.dbcon.cursor()
	db.execute("SELECT `id`, `from`, `message`, `sent` FROM mail WHERE `to` = ?", (user.thisUserID,))
	try:
		for (id, sender, message, sent) in db.fetchall():
			thismail  = "\r\n  `%New Mail...`.\r\n"
			thismail += "`2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-`.\r\n"
			thismail += "`2  From: `0" + user.userGetName(sender) + "`.\r\n"
			thismail += "`2  Date: `0" + sent + "`.\r\n"
			thismail += "`2  Message: `0" + message + "`.\r\n\r\n"
			#if ( not isinstance(thismail, None) ):
			user.write(thismail)
			user.pause()
	except TypeError:
		pass
	db.close()
	user.dbcon.execute("DELETE FROM mail WHERE `to` = ?", (user.thisUserID,))
	user.dbcon.commit()

def announce(user):
	""" Make announcment """
	user.write(func.casebold("\r\n  Your announcment? :-: ", 2))
	ann = "`2"+ user.thisFullname + "`% says: `2"+func.getLine(user.ntcon, True)
	db = user.dbcon.cursor()
	db.execute("SELECT value FROM sord WHERE name = ?", ('gdays',))
	gday = db.fetchone()[0]
	user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (ann, gday))
	user.dbcon.commit()
	db.close()
	user.write(func.casebold("\r\n  Announcment Made!\r\n", 2))
	user.pause()

def sendmail(user):
	""" Send in game mail to a user """
	toid = finduser(user, "\r\n  `2Send mail to which user?`.")
	if ( toid == 0 ):
		return False
	else:
		user.write("\r\n  `2Your message `0:`. ")
		msg = func.getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO mail (`to`, `from`, `message`) VALUES ( ?, ?, ? )", (toid, user.thisUserID, msg))
		user.dbcon.commit()
		user.write(func.casebold("\r\n  Message Sent\r\n", 2))
		user.pause()

def finduser(user, prompter):
	"""Find a user"""
	user.write(prompter + " `0:`2-`0:`. ")
	name = func.getLine(user.ntcon, True)
	db = user.dbcon.cursor()
	db.execute("select userid, fullname FROM users WHERE 1")
	possible = []
	for row in db.fetchall():
		dbname = re.sub('`.', '', row[1])
		dbname = dbname.lower()
		if ( dbname.find(name.lower()) > -1 ):
			possible.append((row[0], row[1]))
			
	for thisoption in possible :
		if not thisoption:
			return 0
		elif ( thisoption[0] == user.thisUserID ):
			pass
		else:
			user.write("\r\n  `2Did you mean `0" + thisoption[1] +" `8(Y/N) `2[`8N`2] `0:`. ")
			yesno = user.ntcon.recv(2)
			if ( yesno[0] == "Y" or yesno[0] == "y" ):
				user.write('Y')
				return thisoption[0]
			else:
				user.write('N')
				pass
	return 0

def viewstats(user):
	""" View Player Stats """
	output  = "\r\n\r\n  `%"+user.thisFullname+"`2's Stats...\r\n"
	output += user.art.line()
	output += " `2 Experience    : `0"+str(user.exp)+func.padnumcol(str(user.exp), 20)+"`2Player Kills       : `0"+str(user.pkill)+"`.\r\n"
	output += " `2 Level         : `0"+str(user.level) + func.padnumcol(str(user.level), 20) + "`2HitPoints          : `0"+str(user.hp)+" `2of`0 "+str(user.hpmax)+"`.\r\n"
	output += " `2 Forest Fights : `0"+str(user.ffight) + func.padnumcol(str(user.ffight), 20) + "`2Player Fights Left : `0"+str(user.pfight)+"`.\r\n"
	output += " `2 Gold In Hand  : `0"+str(user.gold) + func.padnumcol(str(user.gold), 20) + "`2Gold In Bank       : `0"+str(user.bank)+"`.\r\n"
	output += " `2 Weapon        : `0"+data.weapon[user.weapon]+" ("+str(user.weapon)+")" + func.padnumcol(data.weapon[user.weapon]+" ("+str(user.weapon)+")", 20) + "`2Attack Strength    : `0"+str(user.str)+"`.\r\n"
	output += " `2 Armor         : `0"+data.armor[user.armor]+" ("+str(user.armor)+")" + func.padnumcol(data.armor[user.armor]+" ("+str(user.weapon)+")", 20) + "`2Defensive Strength : `0"+str(user.defence)+"`.\r\n"
	output += " `2 Charm         : `0"+str(user.charm) + func.padnumcol(str(user.charm), 20) + "`2Gems               : `0"+str(user.gems)+"`.\r\n\r\n"
	for skillnum in [1,2,3]:
		if ( user.cls == skillnum or user.getSkillPoint(skillnum) > 0 ):
			output += " `2 The "+data.classes[skillnum]+" Skills: `0"
			if ( user.getSkillPoint(skillnum) > 0 ):
				output +=  str(user.getSkillPoint(skillnum)) + func.padnumcol(str(user.getSkillPoint(skillnum)), 11)
			else:
				output += "NONE     "
			output += func.padnumcol(data.classes[skillnum], 12)
			output += " `2Uses Today: (`0"+str(user.getSkillUse(skillnum))+"`2)`.\r\n"
	output += "\r\n  `0You are currently interested in `%The "+data.classes[user.cls]+" `2skills.`.\r\n\r\n";
	return output
	
def who(user):
	""" Who's Online """
	db = user.dbcon.cursor()
	db.execute("SELECT o.userid, fullname, whence FROM users u, online o WHERE o.userid = u.userid ORDER BY whence ASC")
	output  = "\r\n\r\n`%                     Warriors In The Realm Now`.\r\n"
	output += user.art.line()
	for line in db.fetchall():
		output += "  `0" + line[1] + func.padnumcol(line[1], 28)
		output += "`2Arrived At             `%" + str(line[2]) + "`.\r\n"
	db.close()
	return output + "\r\n"

def dailyhappen(noprmpt, user):
	""" View Daily Happenings
	
	* @param bool $noprmpt Do not prompt for additions. """
	db = user.dbcon.cursor()
	db.execute("SELECT value FROM sord WHERE name = ?", ('gdays',))
	gday = db.fetchone()[0]
	db.execute("SELECT data FROM (SELECT * FROM daily WHERE gday = "+str(gday)+" ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id")
	output  = "\r\n\r\n`% Today's Happenings`2....`.\r\n"
	output += "`2                                      -=-=-=-=-=-`.\r\n"
	for line in db.fetchall():
		output += "    " + line[0]
		output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
	user.write(output)
	if ( not noprmpt ) :
		miniQuit = False
		while ( not miniQuit ):
			user.write("\r\n  `2(`#C`2)ontinue  (`#T`2)odays happenings again  (`#Y`2)esterdays happenings  `8[`#C`8] `2:`0-`2:`. ")
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				db.execute("SELECT data FROM (SELECT * FROM daily WHERE gday = "+str(gday)+" ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id")
				output  = "\r\n\r\n`% Today's Happenings`2....`.\r\n"
				output += "`2                                      -=-=-=-=-=-`.\r\n"
				for line in db.fetchall():
					output += "    " + line[0]
					output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
				user.write(output)
			elif ( key[0] == 'y' or key[0] == 'Y' ):
				user.write('Y')
				db.execute("SELECT data FROM (SELECT * FROM daily WHERE gday = "+str(gday-1)+" ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id")
				output  = "\r\n\r\n`% Yesterday's Happenings`2....`.\r\n"
				output += "`2                                      -=-=-=-=-=-`.\r\n"
				for line in db.fetchall():
					output += "    " + line[0]
					output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
				user.write(output)
			else:
				user.write('C')
				miniQuit = True
	db.close()

def list(art, dbc):
	""" Player List """
	db = dbc.cursor()
	db.execute("SELECT userid, fullname, exp, level, cls, spclm, spcld, spclt, sex, alive FROM users WHERE 1 ORDER BY exp DESC")
	output = "\r\n\r\n`2    Name                    Experience    Level    Mastered    Status`.\r\n";
	output += art.line()
	for line in db.fetchall():
		if ( line[8] == 2 ):
			lineSex = "`#F "
		else:
			lineSex = "  "
			
		if ( line[4] == 1 ):
			lineClass = "`9D "
		elif ( line[4] == 2 ):
			lineClass = "`9M "
		else:
			lineClass = "`9T "
		
		lineMaster = ""
		if ( line[6] > 19 ):
			if ( line[6] > 39 ):
				lineMaster += "`%D "
			else:
				lineMaster += "`7D "
		else:
			lineMaster += "  "
			
		if ( line[5] > 19 ):
			if ( line[5] > 39 ):
				lineMaster += "`%M "
			else:
				lineMaster += "`7M "
		else:
			lineMaster += "  "
						
		if ( line[7] > 19 ):
			if ( line[7] > 39 ):
				lineMaster += "`%T "
			else:
				lineMaster += "`7T "
		else:
			lineMaster += "  "
									
		
		if ( line[9] == 1 ):
			lineStatus = "`0Alive"
		else:
			lineStatus = "`1 Dead"
			
		output += lineSex + lineClass + "`2" + line[1] + func.padnumcol(str(line[1]), 24) + "`2" + func.padright(str(line[2]), 10)
		output += func.padright(str(line[3]), 9) + "       " + lineMaster + "    " + lineStatus + "`.\r\n"
	db.close()
	return output + "\r\n"
	
def flowers(user):
	""" The forest flowers """
	output  = "\r\n\r\n  `%Study the forest flowers`2....`.\r\n"
	output += "`2                                      -=-=-=-=-=-`.\r\n"
	db = user.dbcon.cursor()
	db.execute("SELECT data, nombre FROM (SELECT * FROM flowers ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
	for (data, nombre) in db.fetchall():
		output += "    `2"+nombre+" `%says: `2" + data
		output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
	output += "\r\n  `2Add to the conversation? `8(Y/N) `2[`#N`2] `0: `."
	db.close()
	user.write(output)
	yesno = user.ntcon.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		user.write(func.casebold("Y\r\n  What!? What do you want? :-: ", 2))
		ann = func.getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO flowers ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
		user.dbcon.commit()
		user.write(func.casebold("\r\n  Idiocy added!\r\n", 2))
		user.pause()
	else:
		user.write('N\r\n')

def dirt(user):
	""" The slaughter dirt """
	output  = "\r\n\r\n  `%Examine the dirt`2....`.\r\n"
	output += "`2                                      -=-=-=-=-=-`.\r\n"
	db = user.dbcon.cursor()
	db.execute("SELECT data, nombre FROM (SELECT * FROM dirt ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
	for (data, nombre) in db.fetchall():
		output += "    `2"+nombre+" `%says: `2" + data
		output += "\r\n`2                                      -=-=-=-=-=-`.\r\n"
	user.write(output)
	user.pause()

def newuser(user):
	""" Create a user """
	user.write(func.casebold("\r\nCreating a New Character...\r\n", 2))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nPlease Choose a Username (12 characters MAX) :-: ", 2))
		newname = func.getLine(user.ntcon, True)
		newname = newname[:12]
		if ( user.userLoginExist(newname) ):
			user.write(func.casebold("\r\nName In Use!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nAnd, how will you be addressed? (a Handle) (40 characters MAX) :-: ", 2))
		newfname = func.getLine(user.ntcon, True)
		newfname = newfname[:40]
		if ( newfname == "" ):
			user.write(func.casebold("\r\nHEY! No Anonymous Players!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nPick a Password (12 characters MAX) :-: ", 2))
		newpass = func.getLine(user.ntcon, True)
		newpass = newpass[:12]
		if ( newpass == "" ):
			user.write(func.casebold("\r\nPassword MUST Not Be Empty\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nYour Sex (M/F) :-: ", 2))
		key = user.ntcon.recv(2)
		if not key: break
		if ( key[0] == 'm' or key[0] == 'M' ):
			user.write('M')
			newsexnum = 1
			thisLooper = True
			user.write(func.casebold("\r\nMy, what a girly man you are...\r\n", 2))
		if ( key[0] == 'f' or key[0] == 'F' ):
			user.write('F')
			newsexnum = 2
			thisLooper = True
			user.write(func.casebold("\r\nGee sweetheart, hope you don't break a nail...\r\n", 2))
	user.write(func.casebold("\r\nPick that which best describes your childhood.\r\nFrom an early age, you remember:\r\n\r\n", 2))
	user.write(func.normmenu("(D)abbling in the mystical forces"))
	user.write(func.normmenu("(K)illing a lot of woodland creatures"))
	user.write(func.normmenu("(L)ying, cheating, and stealing from the blind"))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nYour Choice (D/K/L) :-: ", 2))
		key = user.ntcon.recv(2)
		if not key: break
		if ( key[0] == 'k' or key[0] == 'K' ):
			user.write('K')
			newclassnum = 1
			thisLooper = True
			user.write(func.casebold("\r\nWelcome warrior to the ranks of the Death Knights!\n", 2))
		if ( key[0] == 'd' or key[0] == 'D' ):
			user.write('D')
			newclassnum = 2
			thisLooper = True
			user.write(func.casebold("\r\nFeel the force young jedi.!\n", 2))
		if ( key[0] == 'l' or key[0] == 'L' ):
			user.write('L')
			newclassnum = 3
			thisLooper = True
			user.write(func.casebold("\r\nYou're a real shitheel, you know that?\n", 2))
	user.dbcon.execute("INSERT INTO users (`username`, `password`, `fullname`, `sex`, `cls`) VALUES ( ?, ?, ?, ?, ?)", (newname, newpass, newfname, newsexnum, newclassnum))
	user.dbcon.commit()
	return newname
