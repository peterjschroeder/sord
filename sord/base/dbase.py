#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all database functions.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
 
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
import sqlite3, time, random
from os.path import isfile
from os import unlink
from shutil import copy

def getDB(config):
	""" Get an active database connection """
	sqc = sqlite3.connect(config.progpath+"/"+config.sqlitefile)
	return sqc

def dayRollover(config, sqc, log):
	""" Daily Update routine """
	
	randdaily = [ 
			'More children are missing today.',
			'A small girl was missing today.',
			'The town is in grief.  Several children didnt come home today.',
			'Dragon sighting reported today by a drunken old man.',
			'Despair covers the land - more bloody remains have been found today.',
			'A group of children did not return from a nature walk today.',
			'The land is in chaos today.  Will the abductions ever stop?',
			'Dragon scales have been found in the forest today..Old or new?',
			'Several farmers report missing cattle today.',
			'A Child was found today!  But scared deaf and dumb.']
			
	checklast = 0
	timestr = '%Y%j00'
	if ( config.daylength > 24 ) :
		days = config.daylength // 24
		checklast = time.strftime('%Y%j00', time.localtime(time.mktime(time.localtime()) - (days*24*60*60)))
	elif ( config.daylength == 6 ) :
		if ( int(time.strftime('%H', time.localtime())) < 6 ): end = '00' 
		elif ( int(time.strftime('%H', time.localtime())) < 12 ): end = '06' 
		elif ( int(time.strftime('%H', time.localtime())) < 18 ): end = '12' 
		else: end = '18' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	elif ( config.daylength == 8 ) :
		if ( int(time.strftime('%H', time.localtime())) < 8 ): end = '00' 
		elif ( int(time.strftime('%H', time.localtime())) < 16 ): end = '08' 
		else: end = '16' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	elif ( config.daylength == 12 ) :
		if ( int(time.strftime('%H', time.localtime())) < 12 ): end = '00' 
		else: end = '12' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	else:
		checklast = time.strftime('%Y%j00', time.localtime())
	
	sqr = sqc.cursor()
	
	for row in sqr.execute("select value from sord where name=?", ('lastday',)):
		lday, = row
		if ( int(lday) < int(checklast) or config.forcenewday ):
			if config.forcenewday:
				config.forcenewday = False
				log.add(" === DAY ROLLOVER (FORCED)")
			else:
				log.add(" === DAY ROLLOVER (NORMAL)")
			db = sqc.cursor()
			db.execute("SELECT value FROM sord WHERE name = ?", ('gdays',))
			gday = int(db.fetchone()[0]) + 1
			rsaying = randdaily[random.randint(0, 9)]
			laster = time.strftime('%Y%j', time.localtime(time.mktime(time.localtime()) - (config.delinactive*24*60*60)))
			sqc.execute("UPDATE users set ffight = ?, pfight = ? WHERE 1", (config.ffight, config.pfight))
			sqc.execute("UPDATE users set flirt = 0, sung = 0, master = 0, usem = spclm, hp = hpmax WHERE 1")
			sqc.execute("UPDATE users set alive = 1 WHERE alive = 2")
			sqc.execute("UPDATE users set alive = 2 WHERE alive = 0")
			sqc.execute("UPDATE users set used = (spcld / 5 ) + 1 WHERE spcld > 0")
			sqc.execute("UPDATE users set uset = (spclt / 5 ) + 1 WHERE spclt > 0")
			sqc.execute("UPDATE users set bank = bank + ( bank * ("+str(config.bankinterest)+"/100) ) WHERE bank > 0")
			if ( gday > 1 ):
				sqc.execute("INSERT INTO daily ( 'data', 'gday' ) VALUES ( ?, ? )", ( "`1"+rsaying, gday))
			sqc.execute("DELETE from users WHERE last < ?", (laster,))
			sqc.execute("UPDATE sord set value = value + 1 WHERE name = 'gdays'")
			sqc.execute("UPDATE sord set value = ? WHERE name = 'lastday'", (time.strftime(timestr, time.localtime()),))
			db.close()
			sqc.commit()
	sqr.close()
	
def initialTest(config, log):
	""" Check for db existence and check version """
	if ( isfile(config.sqlitefile) ):
		sqc = sqlite3.connect(config.progpath+"/"+config.sqlitefile)
		sqr = sqc.cursor()
		
		sqc.execute("vacuum")
		sqc.commit()
		
		for row in sqr.execute("select value from sord where name=?", ('version',)):
			version, = row
			if ( version > 1 ):
				log.add(" === SQLite Database is up to date")
			else:
				log.add(" === SQLite Database is out of date (corrupt), rebuilding...")
				updateDB(config, log)
		sqc.close()
	else:
		createDB(config, log)
		
def updateDB(config, log):
	""" Update S.O.R.D. datebase - for now, nuke and start over """
	copy(config.sqlitefile, config.sqlitefile+".bak")
	unlink(config.sqlitefile)
	createDB(config, log)
		
def createDB(config, log):
	""" Create new S.O.R.D. database """
	log.add(" === Creating New Database - First Run!")
	sqc = sqlite3.connect(config.progpath+"/"+config.sqlitefile)
	
	statstable = [ # (name, default value)
		('cls' , 1) , ('sex', 1), ('flirt', 0), ('sung', 0), ('master', 0),
		('atinn', 0), ('horse', 0), ('fairy', 0), ('ffight', config.ffight), ('pfight', config.pfight),
		('gems', 0), ('gold', 500), ('bank', 0), ('level', 1), ('charm', 0),
		('spclm', 0), ('spclt', 0), ('spcld', 0), ('used', 0), ('dragon', 0),
		('uset', 0), ('usem', 0), ('str', 10), ('defence', 1), ('exp', 1),
		('hp', 20), ('hpmax', 20), ('weapon', 1), ('armor', 1), ('pkill', 0),
		('dkill', 0), ('fuck', 0), ('alive', 1) ]
	statssql = "create table users ( userid INTEGER PRIMARY KEY, username TEXT, password TEXT, fullname TEXT, last TEXT"
	for stat in statstable:
		name, defu = stat
		statssql = statssql + ", " + name + " INTEGER DEFAULT " + str(defu)
	statssql = statssql + " )"
	with sqc:
		sqc.execute("create table sord ( name TEXT, value integer)")
		sqc.execute("insert into sord values (?,?)", ('version', '2'))
		sqc.execute("insert into sord values (?,?)", ('gdays', '0'))
		sqc.execute("insert into sord values (?,?)", ('lastday', '201000101'))
		
		sqc.execute("create table daily ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, gday INTEGER )")
		sqc.execute("insert into daily (data, gday) values (?,?)", ('`0Welcome to `%S`7a`8ga `%o`7f `%t`7h`8e `9R`1ed `%D`7r`8agon', 1))
		sqc.execute("insert into daily (data, gday) values (?,?)", ('`1Despair covers the land - more bloody remains have been found today.', 1))
		
		sqc.execute("create table dhtpatrons (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		dhorse = [ ('`%Chance','`0Pull up a chair, friends.'),
			('`%Barak','`0Ok - These chairs are light...probably because I\'m strong.'),
			('`%Aragorn','`0I really doubt that...'),
			('`%Barak','`0I could juggle these chairs I\'m such a stud!'),
			('`%Aragorn','`0Chance, did you forget to give Barak his medicine?'),
			('`%Chance','`0Whups.  I\'ll slip it in his ale...'),
			('`%Aragorn','`0Why don\'t you move this pub to town?  More business there.'),
			('`%Chance','`0Nah, I don\'t like towns.  Even though I do like that Violet.'),
			('`%Barak','`0She\'s mine I say!  All mine!') ]
		sqc.executemany("insert into dhtpatrons (nombre, data) values (?, ?)", dhorse)

		sqc.execute("create table dirt (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		sqc.execute("insert into dirt (data, nombre) values (?, ?)", ('`1Mighty quiet around here...', 'Jack the `9Ripper'))
		
		sqc.execute("create table flowers ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT )")
		fairy = [ ('`%Fairy Tisha', '`0Oooh!  I love flowers!  And I love to kiss.'),
			('`%Fairy Nolan', '`0Yes!  I\'m glad humans can\'t read our flowers!'),
			('`%Fairy Glimmer', '`0Agreed.  They are all big dumb animals.')]
		sqc.executemany("insert into flowers (nombre, data) values (?, ?)", fairy)

		
		sqc.execute("create table mail ( id INTEGER PRIMARY KEY AUTOINCREMENT, 'from' INTEGER, 'to' integer, message text, sent text)")
		sqc.execute("create table online ( userid integer, whence text )")
		
		sqc.execute("create table patrons ( id INTEGER PRIMARY KEY, data text, nombre TEXT)" )
		pats = [ ('`%Violet', '`0Hey everyone.  Did you hear about that little boy Charles?'),
			('`%Bartender', '`0Yeah.  He is missing.  It\'s a shame.  He was so young.'),
			('`%Halder', '`0Someone has to do something about the Red Dragon!'),
			('`%Aragorn', '`0Look. No one has seen the Red Dragon for 13 years.'),
			('`%Sparhawk', '`0Yes it is. He never died... He is out there.  Somewhere.'),
			('`%Halder', '`0Well lets find him!'),
			('`%Barak', '`0Fine.  You go slay the Dragon then, tough guy.'),
			('`%Halder', '`0Me?!?!  No way!   Let one of those new fools try it!  Haw!'),
			('`%Bartender', '`0Yeah...Those new warriors in town are a joke.')]
		sqc.executemany("insert into patrons (nombre, data) values (?, ?)", pats)
		
		sqc.execute(statssql)
		sqc.execute("insert into users ( userid, username, password, fullname, used, spcld ) values (?, ?, ?, ?, ?, ?)", (1, config.gameadmin, config.gameadminpass, config.admin,1,1))

