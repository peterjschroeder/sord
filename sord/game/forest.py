#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains forest, dragon fight code

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
import random, re, time
from ..base import func
from . import data
from . import util
from . import menu
from ..igm import dht

class getenemy():
	""" Get a new forest enemy """
	def __init__(self, level):
		""" Initialize a random enemy """
		self.level = level
		topenemy = len(data.enemies[level]) - 1
		enemynum = random.randint(0, topenemy)
		
		if ( random.randint(1,10) == 8 ):
			self.underdog = True
		else:
			self.underdog = False
			
		self.hit    = data.enemies[level][enemynum][2] / 2
		self.hp     = data.enemies[level][enemynum][3]
		self.name   = data.enemies[level][enemynum][0]
		self.weapon = data.enemies[level][enemynum][1]
		self.win    = data.enemies[level][enemynum][6]
		self.exp    = data.enemies[level][enemynum][5]
		self.gold   = data.enemies[level][enemynum][4]


class ffight():
	""" S.O.R.D. Forest Interface """
	def __init__(self, user, healers):
		""" Initialize Forest Interface """
		self.user = user
		self.healers = healers
	
	def run(self):
		""" Forest Fight - Non-Combat """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.forest())
					if ( user.horse == True ): 
						user.write(func.normmenu("(T)ake Horse to Dark Horse Tavern"))
				user.write(menu.forest(self.user))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( user.config.fulldebug and key[0] == '!' ): # Debug happenings - by number
				try:
					number = int(func.getLine(user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > 0 and number < 13 ):
					user.write("\r\n")
					self.special(True, number)
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('Q')
				thisQuit = True
			elif ( key[0] == '?' ):
				user.write('?')
				if ( user.expert ):
					user.write(user.art.forest())
			elif ( key[0] == 'x' or key[0] == 'X' ):
				user.write('X')
				user.toggleXprt()
			elif ( key[0] == 's' or key[0] == 'S' ):
				if ( user.level == 12 ):
					user.write('S')
					self.dragon()
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write('H')
				self.healers.run()
			elif ( key[0] == 'v' or key[0] == 'V' or key[0] == 'y' or key[0] == 'Y' ):
				user.write(util.viewstats(user))
			elif ( key[0] == 'l' or key[0] == 'l' ):
				user.write("L\r\n")
				if ( user.ffight > 0 ):
					if ( random.randint(1, 7) == 3 ):
						self.special()
					else:
						self.fight()
				else:
					user.write(func.casebold("\r\n  You are mighty tired.  Try again tommorow\r\n", 2))
			elif ( key[0] == 'a' or key[0] == 'A' ):
				user.write('A')
				user.write(func.casebold("\r\n  You brandish your weapon dramatically.\r\n", 2))
			elif ( key[0] == 'd' or key[0] == 'D' ):
				user.write('D')
				user.write(func.casebold("\r\n  Your Death Knight skills cannot help your here.\r\n", 2))
			elif ( key[0] == 'm' or key[0] == 'M' ):
				user.write('M')
				user.write(func.casebold("\r\n  Your Mystical skills cannot help your here.\r\n", 2))
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				if ( user.horse == True ):
					thismod = dht.dht()
					thismod.run(user)
					del thismod
				else:
					user.write(func.casebold("\r\n  Your Thieving skills cannot help your here.\r\n", 2))
			elif ( key[0] == 'b' or key[0] == 'B' ):
				user.write('B')
				user.write(func.casebold("\r\n  A buzzard swoops down and grabs all your gold on hand.\r\n", 2))
				if ( user.gold > 0 ):
					user.bank += user.gold
					user.gold = 0
			else:
				skipDisp = True

	def menu(self, user, enemy) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  `2Your Hitpoints : `0"+str(user.hp)+"`.\r\n"
		thismenu += "  `2"+enemy.name+"'s Hitpoints : `0"+str(enemy.hp)+"`.\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n"
		if ( user.getSkillUse(1) > 0 ):
			thismenu += func.normmenu("(D)eath Knight Attack ("+str(user.getSkillUse(1))+")")
		if ( user.getSkillUse(2) > 0 ):
			thismenu += func.normmenu("(M)ystical Powers ("+str(user.getSkillUse(2))+")")
		if ( user.getSkillUse(3) > 0 ):
			thismenu += func.normmenu("(T)heiving Sneak Attack ("+str(user.getSkillUse(3))+")")
		thismenu += "\r\n  `2Your command, `0"+user.thisFullname+"`2? [`#A`2] `0:`2-`0: `."
		return thismenu
		
	def dmenu(self, user, ehp, ename) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  `2Your Hitpoints : `0"+str(user.hp)+"`.\r\n"
		thismenu += "  `2The `9Red `2Dragon's Hitpoints : `0"+str(ehp)+"`2\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n"
		if ( user.getSkillUse(1) > 0 ):
			thismenu += func.normmenu("(D)eath Knight Attack ("+str(user.getSkillUse(1))+")")
		if ( user.getSkillUse(2) > 0 ):
			thismenu += func.normmenu("(M)ystical Powers ("+str(user.getSkillUse(2))+")")
		if ( user.getSkillUse(3) > 0 ):
			thismenu += func.normmenu("(T)heiving Sneak Attack ("+str(user.getSkillUse(3))+")")
		thismenu += "\r\n  `2Your command, `0"+user.thisFullname+"`2? [`#A`2] `0:`2-`0: `."
		return thismenu

	def fight(self):
		""" Forest Fight System """
		user = self.user
		user.ffight -= 1
		enemy = getenemy(user.level)
		udef = user.defence
		uhit = user.str / 2
		
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		
		user.write("\r\n\r\n  `2**`%FIGHT`2**\r\n")
		user.write("\r\n  `2You have encountered `%"+enemy.name+"`2!!`.\r\n")
	
		if ( enemy.underdog ): # User is the underdog 
			if ( user.horse == True and random.randint(1, 3) == 2 ): # Saved by the horse 
				user.write("\r\n  `2\"Prepare to die, fool!\" "+enemy.name+" screams.\r\n  He takes a Death Crystal from his cloak and throws it at you.\r\n  Your horse moves its huge body to intercept the crystal.\r\n")
				user.write("\r\n  `0YOUR HORSE IS VAPORIZED!`2\r\n\r\n  Tears of anger flow down your cheeks.  Your valiant steed must be\r\n  avenged.\r\n")
				user.write("\r\n  `0YOU PUMMEL "+enemy.name+" WITH BLOWS!`2\r\n\r\n  A few seconds later, your adversary is dead.\r\n  You bury your horse in a small clearing.  The best friend you ever\r\n  had.\r\n")
				enemy.hp = 0
				ctrlWin = True
				user.horse = 0
			else:
				hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
				if ( hisAttack > 0 ):
					if ( hisAttack >= user.hp ):
						ctrlDead = True
						hisAttack = user.hp
					user.write("\r\n  `2"+enemy.name+" executes a sneak attach for `0"+str(hisAttack)+"`2 damage!`.\r\n")
					user.hp -= hisAttack
				else:
					user.write("\r\n  `2"+enemy.name+" misses you completely!`.\r\n")
		else:
			user.write("\r\n  `2Your skill allows you to get the first strike.`.\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and enemy.hp > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.menu(user, enemy))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( key[0] == 'a' or key[0] == 'A' ): # Attack!
				user.write("A\r\n")
				hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
				myAttack  = ( uhit + random.randint(0, uhit))
				if ( not enemy.underdog ): # We Hit First
					if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`0 damage.`.\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  `2"+enemy.name+" misses you completely.`.\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  `2You hit "+enemy.name+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
					enemy.hp -= myAttack
					if ( enemy.hp < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  `1"+enemy.win+"`.\r\n")
						
			elif ( key[0] == 'd' or key[0] == 'D' ): # Death Knight Attack!
				user.write("D\r\n")
				if ( user.getSkillUse(1) > 0 ):
					user.updateSkillUse(1, -1)
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
					myAttack  = ( uhit + (random.randint(2,5) * random.randint((uhit / 2), uhit))) + uhit
					if ( not enemy.underdog ): # We Hit First
						if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  `2"+enemy.name+" misses you completely`.\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  `0Ultra Powerful Move!\r\n  `2You hit "+enemy.name+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
						enemy.hp -= myAttack
						if ( enemy.hp < 1 ): # We Win!
							ctrlWin = True
							user.write("\r\n  `1"+enemy.win+"`.\r\n")
				else:
					user.write("\r\n  `2You have no Death Knight Skill Use Points!`.\r\n\r\n")
					
			elif ( key[0] == 't' or key[0] == 'T' ): # Thief Sneaky Attack!
				user.write("T\r\n")
				if ( user.getSkillUse(3) > 0 ):
					user.updateSkillUse(3, -1)
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - ( udef * 2 )
					myAttack  = ( uhit + (random.randint(1,3) * random.randint((uhit / 2), uhit))) + uhit
					if ( not enemy.underdog ): # We Hit First
						if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  `2"+enemy.name+" misses you completely`.\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  `0Ultra Sneaky Move!\r\n  `2You hit "+enemy.name+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
						enemy.hp -= myAttack
						if ( enemy.hp < 1 ): # We Win!
							ctrlWin = True
							user.write("\r\n  `1"+enemy.win+"`.\r\n")
				else:
					user.write("\r\n  `2You have no Thief Skill Use Points!`.\r\n\r\n")
					
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
				if ( random.randint(1, 10) == 4 ): # Hit in the back.
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+enemy.name+" hits you in the back with it's "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
						ctrlRan = True
				else:
					user.write("\r\n  `2You narrowly escape harm.`.\r\n")
					ctrlRan = True
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("\r\n  `1You are in Combat!  Try Running!`.\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write("\r\n  `2You are in combat, and they don't make house calls!`.\r\n")
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write("\r\n  `2What?!  You want to fight two at once?`.\r\n")
			elif ( key[0] == 'm' or key[0] == 'M' ): #Magic!
				if ( user.getSkillUse(2) < 1 ):
					user.write("\r\n  `2You have no Magical Use Points!`0\r\n\r\n")
				else:
					user.write("\r\n" + func.normmenu("(N)evermind") + func.normmenu("(P)inch Real Hard (1)"))
					if ( user.getSkillUse(2) > 3 ):
						user.write(func.normmenu("(D)isappear (4)"))
						if ( user.getSkillUse(2) > 7 ):
							user.write(func.normmenu("(H)eat Wave (8)"))
							if ( user.getSkillUse(2) > 11 ):
								user.write(func.normmenu("(L)ight Shield (12)"))
								if ( user.getSkillUse(2) > 15 ):
									user.write(func.normmenu("(S)hatter (16)"))
									if ( user.getSkillUse(2) > 19 ):
										user.write(func.normmenu("(M)ind Heal (20)"))
					user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? [`#A`2] `0:`2-`0:`. ")
					tinyQuit = False
					while ( not tinyQuit ):
						miniData = user.ntcon.recv(2)
						if not miniData: break
						elif ( minikey[0] == 'n' or minikey[0] == 'N' ): #Nothing
							user.write("N\r\n  `2Sure thing boss.`.\r\n")
							tinyQuit = True
						elif ( minikey[0] == 'p' or minikey[0] == 'P' ): #Pinch!
							user.write("P")
							user.updateSkillUse(2, -1)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + ( uhit / 4 )
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `2"+enemy.name+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You pinch "+enemy.name+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  `1"+enemy.win+".`.\r\n")
						elif ( (minikey[0] == 'd' or minikey[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
							user.write("D\r\n  `2You disapper like a ghost!`.\r\n")
							user.updateSkillUse(2, -4)
							tinyQuit = True
							ctrlRan = True
						elif ( (minikey[0] == 'h' or minikey[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
							user.write("H")
							user.updateSkillUse(2, -8)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + (uhit / 2)
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `2"+enemy.name+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You blast "+enemy.name+" with Heat Wave for `9"+str(myAttack)+"`2 damage.`.\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  `1"+enemy.win+"`.\r\n")
						elif ( (minikey[0] == 'l' or minikey[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
							user.write("L\r\n  `2You feel a bit odd.  You dig in a feel better defended.`.\r\n")
							user.updateSkillUse(2, -12)
							udef = udef * 2
							tinyQuit = True
						elif ( (minikey[0] == 's' or minikey[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
							user.write("S")
							user.updateSkillUse(2, -16)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + (uhit * 2)
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+enemy.name+" hits you with "+enemy.weapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `2"+enemy.name+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You Shatter "+enemy.name+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  `1"+enemy.win+"`.\r\n")
						elif ( (minikey[0] == 'm' or minikey[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
							user.write("M\r\n  `2You feel much better!`.\r\n")
							user.updateSkillUse(2, -20)
							hptoadd = user.hpmax - user.hp
							user.hp = user.hpmax
							if ( hptoadd < 5 ):
								user.write("\r\n  `2Though, you are likely clinicly retarded.`.\r\n")
							tinyQuit = True
			else: #Catch non-options
				skipDisp = True
	
		if ( ctrlWin ) :
			user.exp += enemy.exp
			user.gold += enemy.gold
			user.write("\r\n  `2You have recieved `0"+str(enemy.gold)+"`2 gold and `0"+str(enemy.exp)+"`2 experience.`.\r\n")
			user.pause()
		if ( ctrlDead ) :
			if ( user.fairy == True ):
				user.hp = 1
				user.fairy = 0
				user.write(func.casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
			else:
				user.alive = 0
				user.gold = 0
				#exception handles, do it later. user.logout()
				lamentTop = len(data.forestdie) - 1
				lamentThis = data.forestdie[random.randint(0, lamentTop)]
				lamentThis = re.sub("`n", "\r\n    ", lamentThis)
				lamentThis = re.sub("`g", user.thisFullname, lamentThis)
				lamentThis = re.sub("`e", enemy.name, lamentThis)
				user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (lamentThis,user.getgday()))
				user.dbcon.commit()
				user.write(func.casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
				raise Exception('normal', "User is DOA.  Bummer.")

	def special(self, preset = False, option = 0):
		""" Forest Special Events """
		user = self.user
		if ( preset ):
			happening = option
		else:
			happening = random.randint(1, 16)
			if ( user.horse == True and happening == 12 ):
				happening = 10
					
		if ( happening == 1 ):   # Find Gems GOOD!
			thisfind = random.randint(1, 4)
			user.write(user.art.line())
			user.write("  `2Fortune Smiles Upon You.  You find `%"+str(thisfind)+"`2 gems!`.\r\n")
			user.write(user.art.line())
			user.pause()
			user.gems += thisfind
		elif ( happening == 2 ): # Find Gold  GOOD!
			thisfind = random.randint(1, 4) * 200 * user.level
			user.write(user.art.line())
			user.write("  `2Fortune Smiles Upon You.  You find a sack full of `%"+str(thisfind)+"`2 gold!`.\r\n")
			user.write(user.art.line())
			user.pause()
			user.gold += thisfind
		elif ( happening == 3 ): # Hammerstone (attack str++)  GOOD!
			user.write(user.art.line())
			user.write("  `2You find a hammer stone.  You quickly hit it as hard as possible.\r\n\r\n  `0Your attack strength is raised by 1!`.\r\n")
			user.write(user.art.line())
			user.pause()
			user.str += 1
		elif ( happening == 4 ): # Merry Men (hp = hpmax)
			user.write(user.art.line())
			user.write("  `2You stumble across a group of merry men.\r\n  They offer you ale you can't resist.\r\n  `0You feel refreshed!`.\r\n")
			user.write(user.art.line())
			user.pause()
			user.hp = user.hpmax
		elif ( happening == 5 ): # Old Man (gold + (lvl * 500) && charm +1 on help) (costs 1 fight) GOOD!
			user.write(user.art.line())
			user.write("  `2You come upon an old man wandering around.\r\n  He asks you for help back to town.`.\r\n\r\n")
			user.write(func.normmenu("(H)elp the old man"))
			user.write(func.normmenu("(I)gnore him"))
			user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? `0:`2-`0: `.")
			miniQuit = False
			while ( not miniQuit ):
				key = user.ntcon.recv(2)
				if ( key[0] == 'h' or key[0] == 'H' ):
					user.write('H')
					goldtoadd = user.level * 500
					user.write("\r\n\r\n  `2You help the old gentleman home.\r\n  `0He gives you "+str(goldtoadd)+" gold and 1 charm!.`.\r\n")
					user.gold += goldtoadd
					user.charm += 1
					user.ffight -= 1
					miniQuit = True
				elif ( key[0] == 'i' or key[0] == 'I' ):
					user.write('I')
					user.write("\r\n  `1You just really `9SUCK`1, don't you?`.\r\n")
					miniQuit = True
				else:
					pass
			user.pause()
		elif ( happening == 6 ): # Ugly (33%) and Pretty (66%) stick GOOD!
			user.write(user.art.line())
			user.write("  `2A demented penguin jumps from the bushes and whacks you with a")
			sticktype = random.randint(1, 3)
			if ( sticktype == 2 ):
				user.write("`9 ugly `2")
			else:
				user.write("`0 pretty `2")
			user.write("stick!\r\n  Your charm is ")
			if ( sticktype == 2 ):
				user.write("lowered")
				if ( user.charm > 0 ):
					user.charm -= 1
			else:
				user.write("raised")
				user.charm += 1
			user.write(" by 1!!`.\r\n")
			user.pause()
		elif ( happening == 7 ): # Old Hag GOOD!
			user.write(user.art.line())
			user.write("  `2You come across an old hag.\r\n\r\n  `0\"Give me a gem my pretty, and I will completely heal you!\"`2\r\n  She screeches!`.\r\n\r\n")
			user.write(func.normmenu("(G)ive her a gem"))
			user.write(func.normmenu("(K)ick her and run"))
			user.write(func.normmenu("(L)eave polietly"))
			miniQuit = False
			while ( not miniQuit ):
				user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? `0:`2-`0: `.")
				key = user.ntcon.recv(2)
				if ( key[0] == 'l' or key[0] == 'L' ):
					user.write("L\r\n\r\n  `2The old hag begins following you like a lost puppy.`.\r\n")
				elif ( key[0] == 'k' or key[0] == 'K' ):
					user.write("K\r\n\r\n  `2You hate to be rude to your elders, but sometimes deperate times call for\r\n  deperate measures.  You which the old hag in the shin and run for it.`.\r\n")
					miniQuit = True
				elif ( key[0] == 'g' or key[0] == 'G' ):
					user.write('G')
					if ( user.gems > 0 ):
						user.write("\r\n\r\n  `0\"Thank you\"`2 she cackles.\r\n  `0You feel refreshed and renewed.`.\r\n")
						user.hpmax += 1
						user.hp = user.hpmax
						user.gems -= 1
						miniQuit = True
					else:
						user.write("\r\n\r\n  `0\"You don't have any gems you stinky cow-pox pustule!\"`2 she yells.\r\n  `0Come to think of it, you feel rather like a cow-pie.`.\r\n")
						user.hp = 1
						miniQuit = True
				else: 
					pass
			user.pause()
		elif ( happening == 8 ): # Flowers in the forest. GOOD!
			user.write(user.art.line())
			user.write("  `2You come across a grove of flowers, and decide to inspect them closer...\r\n  `0There is something written here!`.\r\n")
			user.pause()
			util.flowers(user)
		elif ( happening == 9 ): # rescue man/maiden GOOD!
			user.write(user.art.line())
			user.write("  `2You come upon a dead bird.  While gross, you begin to put it out of your\r\n  mind when you notice a scroll attached to it's leg\r\n\r\n")
			user.write("  `0To Whome It May Concern:\r\n    I have been locked in this terrible tower for many cycles.\r\n    Please save me soon!\n        ~ Elora\r\n\r\n")
			user.write(func.normmenu("(S)eek the maiden"))
			user.write(func.normmenu("(I)gnore her plight"))
			user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? `0:`2-`0:`. ")
			miniQuit = False
			while ( not miniQuit ):
				key = user.ntcon.recv(2)
				if ( key[0] == 'i' or key[0] == 'I' ):
					user.write('I')
					miniQuit = True
				elif ( key[0] == 's' or key[0] == 'S' ):
					user.write('S')
					user.ffight -= 1
					thisMiniQuit = False
					thisTower = 0
					user.write("\r\n\r\n  `2Where do you wish to seek the maiden?`.\r\n")
					user.write(func.normmenu("(K)eep of Hielwain"))
					user.write(func.normmenu("(S)tarbucks Seattle Spaceneedle"))
					user.write(func.normmenu("(C)astle Morbidia"))
					user.write(func.normmenu("(S)ty of Pigashia"))
					user.write(func.normmenu("(B)logshares Brutal Belfry"))
					user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? `0:`2-`0:`. ")
					while ( not thisMiniQuit ):
						miniData = user.ntcon.recv(2)
						if ( miniData[0] == 'k' or miniData[0] == 'K' ):
							user.write('K')
							thisTower = 1
							thisMiniQuit = True
						elif ( miniData[0] == 's' or miniData[0] == 'S' ):
							user.write('S')
							thisTower = 2
							thisMiniQuit = True
						elif ( miniData[0] == 'c' or miniData[0] == 'C' ):
							user.write('C')
							thisTower = 3
							thisMiniQuit = True
						elif ( miniData[0] == 's' or miniData[0] == 'S' ):
							user.write('S')
							thisTower = 4
							thisMiniQuit = True
						elif ( miniData[0] == 'b' or miniData[0] == 'B' ):
							user.write('B')
							thisTower = 5
							thisMiniQuit = True
						else:
							pass
					user.write(user.art.tower())
					user.pause()
					if ( thisTower == random.randint(1, 5) ): # Correct Choice
						user.write("\r\n  `2You have choosen `0wisely.`.\r\n")
						user.write("  `2Elora gasps in suprise, saunters over, and thanks you 'properly'\r\n  `0You feel smarter, more gem laden, and -erm- 'satisfied'`.\r\n")
						user.gems += 5
						user.gold += (user.level * 500)
					else: # WRONG
						if ( random.randint(1, 2) == 1 ): # REALLY, REALLY WRONG
							user.write("\r\n  `2You have choosen `1poorly.  `9really poorly.`.\r\n\r\n")
							user.write("  `2You hear a strange groan and out pops Ken the Magnificent,\r\n  the disfigured midget (er, 'little person').\r\n  Sadly, 'little person' doesn't refer to all of him.\r\n\r\n  `0You feel terrible, both physically and mentally`.\r\n")
							user.hp = 1
						else: # NOT SO BAD
							user.write("\r\n  `2You have choosen `1poorly.`.\r\n")
							user.write("  `2You run like hell before anything bad happens.`.\r\n")
					miniQuit = True
			user.pause()
		elif ( happening == 10 or happening > 12 ): # lessons DKNIGHT GOOD, 
			if ( user.cls == 1 ):
				self.lesson_d()
			elif ( user.cls == 2 ):
				self.lesson_m()
			else:
				self.lesson_t()
			user.pause()
		elif ( happening == 11 ): # fairies
			self.fairies()
			user.pause()
		elif ( happening == 12 ): # darkhorse
			thismod = dht.dht()
			thismod.run(user)
			del thismod
		else:
			pass

	def fairies(self):
		""" Happening - Forest Fairies """
		user = self.user
		user.write(user.art.fairies())
		user.pause()
		user.write("  `2You glance at the fairies, trying to decide what to do.\r\n\r\n")
		user.write(func.normmenu("(A)sk for a Blessing"))
		user.write(func.normmenu("(T)ry and catch one"))
		miniQuit = False
		while ( not miniQuit ):
			user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? `0:`2-`0:`. ")
			miniData = user.ntcon.recv(2)
			if ( miniData[0] == 'a' or miniData[0] == 'A' ):
				user.write('A')
				miniQuit = True
				blessingIs = random.randint(1, 4)
				if ( blessingIs == 4 and user.horse == True ):
					# Trap for already has a horse!
					blessingIs = 2
				if ( blessingIs == 1 ): # A Kiss
					user.write("\r\n\r\n  `2You recieve a kiss from Teesha and feel better!`.\r\n\r\n")
					user.hp = user.hpmax
				elif ( blessingIs == 2 ): # Sad Stories
					user.write("\r\n\r\n  `2The fairies tell you sad stories.\r\n  `0You're tears turn into gems!`.\r\n\r\b")
					user.gems += 2
				elif ( blessingIs == 3 ): # Fairy lore.
					user.write("\r\n\r\n  `2The fairies tell you secret fairly lore.\r\n  `0You feel smarter.`.\r\n\r\b")
					user.exp += ( user.level * 20 )
				elif ( blessingIs == 4 ): # The Horse
					user.write("\r\n\r\n  `2The fairys bless you with a new companion!\r\n  Please remember, horses are for riding, not, er... `0*riding*`.\r\n\r\n")
					user.horse = 1
				else:
					user.write("\r\n\r\n  `%WTF?`.\r\n\r\n")
			if ( miniData[0] == 't' or miniData[0] == 'T' ):
				user.write('T')
				miniQuit = True
				caughtIt = random.randint(1, 3)
				if ( caughtIt == 3 ):  # Grabbed One!
					user.write("\r\n\r\n  `2You managed to grab one!\r\n  You place it in your pocket for later.`.\r\n")
					user.fairy = 1
				else:
					user.write("\r\n\r\n  `2You `0MISS`2!  And grab a thornberry bush instead!`.\r\n")
					user.hp = 1
	
	def lesson_d(self) :
		""" Learn to be a death kniofht"""
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  `2You come upon a group of warriors, they carry the look of a proud people.`.\r\n")
		user.write("\r\n   `3Death Knight #1: `2We shall teach you the ways of the death knights weakling.`.\r\n\r\n")
		user.write("   `3Death Knight #2: `2Aye.  But you must prove your wisdom first.\r\n                    This man is guilty of a crime.\r\n\r\n")
		user.write("   `3Death Knight #1: `2Yup.  Or he's completely innocent.  Decide wisely.!\r\n\r\n")
		user.write(func.normmenu("(K)ill Him"))
		user.write(func.normmenu("(F)ree him as an innocent"))
		user.write("\r\n  `2Your choice, `0"+user.thisFullname+"`2? `8(K,F) `0:`2-`0:`. ")
		miniQuit = False
		while ( not miniQuit ):
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'k' or key[0] == 'K' ):
				user.write('K')
				user.write("\r\n  `2You draw your weapon, and ram it as hard as you can through his midsection.`.\r\n")
				thisChoice = 1
				miniQuit = True
			elif ( key[0] == 'f' or key[0] == 'F' ):
				user.write('F')
				user.write("\r\n  `2You consider a moment, and shout \"Let him live!  He's done nothing wrong!\"`.\r\n")
				thisChoice = 2
				miniQuit = True
	
		user.write("\r\n  `%...")
		time.sleep(1)
		user.write("`1AND`%")
		time.sleep(1)
		user.write("...`.\r\n")
		
		if ( thisChoice == random.randint(1,2) ):
			user.write("\r\n   `3Death Knight #1: `2Well spotted young warrior.\r\n                    We shall teach you!`.\r\n\r\n")
			user.write("  `2You recieve `01`2 use point")
			user.updateSkillUse(1, 1)
			user.hp = user.hpmax
			if ( user.getSkillPoint(1) < 40 ):
				user.updateSkillPoint(1, 1)
				user.write(" and `01`2 skill point")
			user.write(".`.\r\n")
		else:
			user.write("\r\n   `3Death Knight #3: `2Oh god no!  That wasn't right at all!\r\n                    Somebody get a mop and a bandaid!`.\r\n\r\n")
	
	def lesson_t(self) :
		""" LEarn to be a thief """
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  `2You come upon a gathering of the theives guild, they kinda smell bad.`.\r\n")
		user.write("\r\n   `3Thief #1: `2We can make you a better thief.  Just cost ya a gem.`.\r\n")
		user.write(func.normmenu("(G)ive him the gem"))
		user.write(func.normmenu("(S)pit on him and walk away"))
		user.write(func.normmenu("(M)utter incoherantly, hoping he'll leave"))
		user.write("\r\n  `2Your choice, `0"+user.thisFullname+"`2? `8(G,S,M) `0:`2-`0:`. ")
		miniQuit = False
		while ( not miniQuit ):
			key = user.ntcon.recv(2)
			if not data: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write("S\r\n  `2mAs you spit on him, the thief looks at you closely.  He almost looks proud.`.\r\n")
				miniQuit = True
			elif ( key[0] == 'm' or key[0] == 'M' ):
				user.write("M\r\n  `2As the thief leaves, you distincly hear the words \"nutjob\" and \"jackass\".  Oh well.`.\r\n")
				miniQuit = True
			elif ( key[0] == 'g' or key[0] == 'G' ):
				user.write('G')
				if ( user.gems > 0 ):
					user.updateSkillUse(3, 1)
					user.write("\r\n  `2You recieve `01`2 use point")
					if ( user.getSkillPoint(3) < 40 ):
						user.updateSkillPoint(3, 1)
						user.write(" and `01`2 skill point")
					user.write(".`.\n")
					user.gems -= 1
				else:
					user.write("\r\n  `3Thief #1: `2You don't have any gems dumbass.`.\r\n")
				miniQuit = True
	
	def lesson_m(self) :
		""" Learn about magic """
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  `2You come upon an old house.  You sense an old mage might live here.`.\r\n")
		user.write(func.normmenu("(K)nock on the door"))
		user.write(func.normmenu("(B)ang on the door"))
		user.write(func.normmenu("(L)eave"))
		user.write("\r\n  `2Your choice, `0"+user.thisFullname+"`2? `8(K,B,L) `0:`2-`0:`. ")
		miniQuit1 = False
		miniQuit2 = False
		
		while ( not miniQuit1 ):
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'k' or key[0] == 'K' ):
				user.write('K')
				user.write("\r\n  `2You knock polietly on the door.`.\r\n")
				miniQuit1 = True
			elif ( key[0] == 'b' or key[0] == 'B' ):
				user.write('B')
				user.write("\r\n  `2You bang wildly on the door.`.\r\n")
				miniQuit1 = True
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write('L')
				user.write("\r\n  `2You leave, confident in finding better things to do.`.\r\n")
				miniQuit1 = True
				miniQuit2 = True
	
		if ( not miniQuit2 ):
			if ( random.randint(1, 5) == 2 ):
				user.write("\r\n  `2Nothing happens, and you leave.`.\r\n")
			else:
				user.write("\r\n  `2The old man rips open the door and screams `!\"WHAT?!?\"`.\r\n")
				user.write("  `2He then gazes at you and says \"I'll teach you magic if you can guess\r\n  the number I'm thinking of.  It's between 1 and 100`.\r\n")
				magicNumber  = random.randint(1, 100)
				magicCorrect = False
				magicGuess   = 0
				while ( magicGuess < 7 ):
					user.write("\r\n  `2Your guess, `0"+user.thisFullname+"`2? `0:`2-`0:`. ")
					try: 
						thisGuess = int(func.getLine(user.ntcon, True))
					except ValueError:
						thisGuess = 1
					if ( thisGuess == magicNumber ):
						magicGuess = 7
						magicCorrect = True
					else:
						if ( thisGuess < magicNumber ):
							user.write("\r\n  `2Higher!`.\r\n")
						if ( thisGuess > magicNumber ):
							user.write("\r\n  `2Lower!`.\r\n")
					magicGuess += 1
	
				if ( magicCorrect ):
					user.write("\r\n  `2Well Done young mage!`0\r\n")
					user.updateSkillUse(2, 1)
					user.write("  `2You recieve `01`2 use point")
					if ( user.getSkillPoint(2) < 40 ):
						user.updateSkillPoint(2, 1)
						user.write(" and `01`2 skill point")
					user.write(".`.\r\n")
				else:
					user.write("\r\n  `2Better luck next time!`.\r\n")

	def dragon(self):
		""" Forest Fight System """
		user = self.user
		user.write(user.art.lair())
		thisUserDefense = user.defence
		thisUserHit     = user.str / 2
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		thisEnemyHit    = 2000
		thisEnemyHP     = 15000
		thisEnemyName   = "The Red Dragon"
		thisEnemyWeapon = "Set Later."
		
		user.write("\r\n\r\n  `2**`%FIGHT`2**\r\n")
		user.write("\r\n  `2You have encountered "+thisEnemyName+"!!`.\r\n")
	
		user.write("\r\n  `2Your skill allows you to get the first strike.`.\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.dmenu(user, thisEnemyHP, thisEnemyName))
			hisType = random.randint(1, 7)
			if ( hisType == 1 or hisType == 2 ):
				thisEnemyWeapon = "Huge Fucking Claws"
				thisEnemyHit = 2100
			elif ( hisType == 3 or hisType == 4 ):
				thisEnemyWeapon = "Swishing Tail"
				thisEnemyHit = 1800
			elif ( hisType == 5 or hisType == 6 ):
				thisEnemyWeapon = "Stomping the Ground"
				thisEnemyHit = 1500
			else:
				thisEnemyWeapon = "Flaming Breath"
				thisEnemyHit = 3000
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( key[0] == 'a' or key[0] == 'A' ): # Attack!
				user.write("A\r\n")
				hisAttack = ( thisEnemyHit + random.randint(500, thisEnemyHit)) - thisUserDefense
				myAttack  = ( thisUserHit + random.randint(0, thisUserHit))
				if ( True ): # We Hit First
					if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  `2"+thisEnemyName+" misses you completely.`.\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  `2You hit "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
			elif ( key[0] == 'd' or key[0] == 'D' ): # Attack!
				user.write("D\r\n")
				if ( user.getSkillUse(1) > 0 ):
					user.updateSkillUse(1, -1)
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
					myAttack  = ( thisUserHit + (random.randint(2,5) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
					if ( True ): # We Hit First
						if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  `2"+thisEnemyName+" misses you completely.`.\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  `0Ultra Powerful Move!\r\n  `2You hit "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
						thisEnemyHP = thisEnemyHP - myAttack
						if ( thisEnemyHP < 1 ): # We Win!
							ctrlWin = True
				else:
					user.write("\r\n  `2You have no Death Knight Skill Use Points!`.\r\n\r\n")
			elif ( key[0] == 't' or key[0] == 'T' ): # Attack!
				user.write("T\r\n")
				if ( user.getSkillUse(3) > 0 ):
					user.updateSkillUse(3, -1)
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - ( thisUserDefense * 2 )
					myAttack  = ( thisUserHit + (random.randint(1,3) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
					if ( True ): # We Hit First
						if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  `2"+thisEnemyName+" misses you completely.`.\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  `0Ultra Sneaky Move!\r\n  `2You hit "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
						thisEnemyHP = thisEnemyHP - myAttack
						if ( thisEnemyHP < 1 ): # We Win!
							ctrlWin = True
				else:
					user.write("\r\n  `2You have no Thief Skill Use Points!`.\r\n\r\n")
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
				if ( random.randint(1, 10) == 4 ): # Hit in the back.
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  `2"+thisEnemyName+" hits you in the back with it's "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
						user.hp -= hisAttack
						ctrlRan = True
				else:
					user.write("\r\n  `2You narrowly escape harm.`.\r\n")
					ctrlRan = True
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("\r\n  `1You are in Combat!  Try Running!`.\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write("\r\n  `2You are in combat, and they don't make house calls!`.\r\n")
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write("\r\n  `2What?!  You want to fight two at once?`.\r\n")
			elif ( key[0] == 'm' or key[0] == 'M' ): #Magic!
				if ( user.getSkillUse(2) < 1 ):
					user.write("\r\n  `2You have no Magical Use Points!`.\r\n\r\n")
				else:
					user.write("\r\n" + func.normmenu("(N)evermind") + func.normmenu("(P)inch Real Hard (1)"))
					if ( user.getSkillUse(2) > 3 ):
						user.write(func.normmenu("(D)isappear (4)"))
						if ( user.getSkillUse(2) > 7 ):
							user.write(func.normmenu("(H)eat Wave (8)"))
							if ( user.getSkillUse(2) > 11 ):
								user.write(func.normmenu("(L)ight Shield (12)"))
								if ( user.getSkillUse(2) > 15 ):
									user.write(func.normmenu("(S)hatter (16)"))
									if ( user.getSkillUse(2) > 19 ):
										user.write(func.normmenu("(M)ind Heal (20)"))
					user.write("\r\n  `2Your command, `0"+user.thisFullname+"`2? [`#A`2] `0:`2-`0:`. ")
					tinyQuit = False
					while ( not tinyQuit ):
						miniData = user.ntcon.recv(2)
						if not miniData: break
						elif ( miniData[0] == 'n' or miniData[0] == 'N' ): #Nothing
							user.write("N\r\n  `2Sure thing boss.`.\r\n")
							tinyQuit = True
						elif ( miniData[0] == 'p' or miniData[0] == 'P' ): #Pinch!
							user.write("P")
							user.updateSkillUse(2, -1)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + ( thisUserHit / 4 )
							if ( True ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `2"+thisEnemyName+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You pinch "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'd' or miniData[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
							user.write("D\r\n  `2You disapper like a ghost!`.\r\n")
							user.updateSkillUse(2, -4)
							tinyQuit = True
							ctrlRan = True
						elif ( (miniData[0] == 'h' or miniData[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
							user.write("H")
							user.updateSkillUse(2, -8)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit / 2)
							if ( True ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `2"+thisEnemyName+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You blast "+thisEnemyName+" with Heat Wave for `9"+str(myAttack)+"`2 damage.`.\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'l' or miniData[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
							user.write("L\r\n  `2You feel a bit odd.  You dig in a feel better defended.`.\r\n")
							user.updateSkillUse(2, -12)
							thisUserDefense = thisUserDefense * 2
							tinyQuit = True
						elif ( (miniData[0] == 's' or miniData[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
							user.write("S")
							user.updateSkillUse(2, -16)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit * 2)
							if ( not thisUnderdog ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  `2"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for `9"+str(hisAttack)+"`2 damage.`.\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  `."+thisEnemyName+" misses you completely.`.\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  `2You Shatter "+thisEnemyName+" for `9"+str(myAttack)+"`2 damage.`.\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'm' or miniData[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
							user.write("M\r\n  `2You feel much better!`.\r\n")
							user.updateSkillUse(2, -20)
							hptoadd = user.hpmax - user.hp
							user.hp = user.hpmax
							if ( hptoadd < 5 ):
								user.write("\r\n  `2Even though you are clearly a fuck-tard...`.\r\n")
							tinyQuit = True
			else: #Catch non-options
				skipDisp = True
	
		if ( ctrlWin ) :
			user.gold = 500
			user.bank = 0
			user.str = 10
			user.defence = 1
			user.level = 1
			user.exp = 1
			user.dragon += 1
			user.ffight = user.config.ffights
			user.pfight = user.config.pfights
			user.hp = 20
			user.hpmax = 20
			user.gems = 10
			user.weapon = 1
			user.armor = 1
			
			lamentThis = "`0"+user.thisFullname+" `9Decimated `2The `1Red `2Dragon!!! `%Rejoice!!!`."
			user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (lamentThis,user.getgday()))
			user.dbcon.commit()
			user.write(func.casebold("\r\n\r\n  You have defeated the Dragon, and saved the town.  Your stomach\r\n", 2))
			user.write(func.casebold("  churns at the site of stacks of clean white bones - Bones of small\r\n", 2))
			user.write(func.casebold("  children.\r\n\r\n", 2))
			user.write(func.casebold("  THANKS TO YOU, THE HORROR HAS ENDED!\r\n\r\n", 2))
			user.pause()
			for myline in data.endstory[user.cls]:
				user.write("`2"+myline+"`0\r\n")
			user.pause()
			user.write(func.casebold("                  ** YOUR QUEST IS NOT OVER **\r\n\r\n", 2))
			user.write(func.casebold("  You are a hero.  Bards will sing of your deeds, but that doesn't\r\n", 2))
			user.write(func.casebold("  mean your life doesn't go on.\r\n", 2))
			user.write(func.casebold("  YOUR CHARACTER WILL NOW BE RESET.  But you will keep a few things\r\n", 2))
			user.write(func.casebold("  you have earned.  Like the following.\r\n", 2))
			user.write(func.casebold("  ALL SPECIAL SKILLS.\r\n  CHARM.\r\n  A FEW OTHER THINGS.\r\n", 2))			
			user.pause()
			
		if ( ctrlDead ) :
			if ( user.fairy == True ):
				user.hp = 1
				user.fairy = 0
				user.write(func.casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
			else:
				user.alive = 0
				#exception handles, do it later. user.logout()
				lamentThis = "`2The `1Red `2Dragon `9Decimated `2"+user.thisFullname+"`."
				user.dbcon.execute("INSERT INTO daily ( `data`, `gday` ) VALUES ( ?, ? )", (lamentThis,user.getgday()))
				user.dbcon.commit()
				user.write(func.casebold("\r\n\r\n  The Dragon pauses to look at you, then snorts in a Dragon laugh, and\r\n", 1))
				user.write(func.casebold("  delicately rips your head off, with the finess only a Dragon well\r\n", 1))
				user.write(func.casebold("  practiced in the art could do.\r\n", 1))
				raise Exception('normal', "User is DOA.  Bummer.")
	
