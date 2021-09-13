""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all menus.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import time
from . import data
from ..base import func

def turgon(user):
	"""Turgons warrior training """
	ptime = func.maketime(user)
	try:
		thismenu = "\r\n  `2Your master is `%"+data.masters[user.level][0]+"`2.`.\r\n\r\n"
	except IndexError:
		thismenu = "\r\n  `2You have no master.  You are as smart as you can possibly get.`.\r\n\r\n"
	thismenu += "`#  Turgon's Warrior Training `8(Q,A,V,R) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu

def bank(user):
	"""Ye olde bank """
	ptime = func.maketime(user)
	thismenu = "\r\n\r\n`2  Gold In Hand: `0" + str(user.gold)
	thismenu += "`2 Gold In Bank: `0" + str(user.bank) + "\r\n"
	thismenu += "`#  The Bank `8(W,D,R,T,Q) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu

def forest(user):
	""" Forest fight menu (pre-battle) """
	ptime = func.maketime(user)
	thismenu = "\r\n  `2HitPoints: (`0" + str(user.hp) + "`2 of `0" + str(user.hpmax)
	thismenu += "`2)  Fights: `0" + str(user.ffight) + "`2  Gold: `0" + str(user.gold)
	thismenu += "`2  Gems: `0" + str(user.gems) + "`.\r\n"
	thismenu += "  `#The Forest  `8(L,H,R,Q) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu

def slaughter(user):
	""" Slaughter other players """
	ptime = func.maketime(user)
	thismenu = "\r\n`#  Slaughter Other Players `8(S,L,E,W,R) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu
	
def heal(user):
	""" Healers Hut """
	ptime = func.maketime(user)
	thismenu  = "\r\n\r\n  `%Saga of the Red Dragon - `2Healers Hut`.\r\n"
	thismenu += user.art.line()
	thismenu += "  `2You enter the smoky healers hut.\r\n  `#\"What is your wish, warrior?\" `2the old\r\n  `2healer asks.`.\r\n\r\n"
	thismenu += func.normmenu("(H)eal all possible")
	thismenu += func.normmenu("(C)ertain amount healed")
	thismenu += func.normmenu("(R)eturn")
	thismenu += "\r\n`2  HitPoints: `0" + str(user.hp) + "`2 of `0" + str(user.hpmax) + "`."
	thismenu += "`2  Gold In Hand: `0" + str(user.gold)
	thismenu += "`2.\r\n  It costs `0" + str(user.level * 5) + "`2 gold to heal 1 HitPoint`.\r\n"
	thismenu += "`#  The Healers Hut `8(H,C,R) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu

def mainlong(user):
	"""Main Menu - Non-Expert
	* @todo Married List
	"""
	thismenu  = "\r\n\r\n`%  Saga of the Red Dragon - `2Town Square\r\n"
	thismenu += user.art.line()
	thismenu += "`2  The streets are crowded, it is difficult to\r\n  push your way through the mob....\r\n\r\n"
	thismenu += func.menu_2col("(F)orest", "(S)laughter other players", 5, 5)
	thismenu += func.menu_2col("(K)ing Arthurs Weapons", "(A)bduls Armour", 5, 5)
	thismenu += func.menu_2col("(H)ealers Hut", "(V)iew your stats", 5, 5)
	thismenu += func.menu_2col("(I)nn", "(T)urgons Warrior Training", 5, 5)
	thismenu += func.menu_2col("(Y)e Old Bank", "(L)ist Warriors", 5, 5)
	thismenu += func.menu_2col("(W)rite Mail", "(D)aily News", 5, 5)
	thismenu += func.menu_2col("(P)eople Online", "(O)ther Places", 5, 5)
	thismenu += func.menu_2col("(X)pert Mode", "(M)ake Announcement", 7, 5)
	thismenu += func.menu_2col("", "(Q)uit to Fields", 5, 2)
	return thismenu

def mainshort(user):
	""" Main Menu - Expert
	
	* Generate short main menu with prompt.  Appended to Non-Expert menu as well. """
	ptime = func.maketime(user)
	thismenu  = "\r\n  `#The Town Square `8(? for menu)`.\r\n"
	thismenu += "  `8(F,S,K,A,H,V,I,T,Y,L,W,D,P,O,X,M,Q)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu

def abdul(user):
	""" Abdul's Armor """
	ptime = func.maketime(user)
	thismenu  = "\r\n  `2Current armour: `0"+data.armor[user.armor]+"`.\r\n"
	thismenu += "  `#Abduls Armour `8(B,S,Y,R) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu
 
def arthur(user):
	"""King Arthur's Weapons """
	ptime = func.maketime(user)
	thismenu  = "\r\n  `2Current weapon: `0"+data.weapon[user.weapon]+"`.\r\n"
	thismenu += "  `#King Arthur's Weapons `8(B,S,Y,R) (? for menu)`.\r\n\r\n"
	thismenu += "  `2Your command, `0" + user.thisFullname + "`2? `%[`7"+ptime+"`%] `0:`2-`0: `."
	return thismenu
