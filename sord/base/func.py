#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all misc display functions.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import re, time, random

def slowecho(connection, data, LINESPEED=0, NOISE=0):
	""" Modem speed emulation display routine """
	ldcolors = [
		( '`1', '\x1b[31m'), ( '`2', '\x1b[32m'), ( '`3', '\x1b[33m'), ( '`4', '\x1b[34m'),
		( '`5', '\x1b[35m'), ( '`6', '\x1b[36m'), ( '`7', '\x1b[37m'), ( '`8', '\x1b[1;30m'),
		( '`9', '\x1b[1;31m'), ( '`0', '\x1b[1;32m'), ( '`!', '\x1b[1;33m'), ( '`@', '\x1b[1;34m'), 
		( '`#', '\x1b[1;35m'), ( '`\$', '\x1b[1;36m'), ( '`%', '\x1b[1;37m'), ( '`\.', '')]
	if ( LINESPEED == 0 ):
		pause = 0.001
	elif ( LINESPEED == 1 ):
		pause = 0.002
	elif ( LINESPEED == 2 ):
		pause = 0.0005
	elif ( LINESPEED == 3 ):
		pause = 0.00001
	for cpair in ldcolors:
		data = re.sub(cpair[0], '\x1b[0m'+cpair[1], data)
		
	for thisData in list(data):
		if ( NOISE ):
			if ( random.randint(1, 2000) == 3 ):
				thisData = ' '
		time.sleep(pause)
		connection.send(thisData)
		

def pauser(connection):
	""" Sreen pauser """
	slowecho(connection, casebold("\r\n    :-: Press Any Key :-:", 2))
	pauser_quit = False
	while ( not pauser_quit ):
		data = connection.recv(5)
		if not data: break
		pauser_quit = True
		for i in xrange(1, 22):
				slowecho(connection, "\x1b[1D \x1b[1D")
		connection.send("\r\n")
		

def getLine(connection, echo, prompt=""):
	""" Get line from user"""
	getterquit = False
	retval = ""
	if ( not prompt == "" ):
		connection.send("  "+prompt)
	while ( not getterquit ):
		key = connection.recv(2)
		if not key: break
		if ( key[0] == "\n" or key[0] == "\r" ):
			getterquit = True
		else:
			if ( key[0] == chr(127) ):
				retval = retval[:-1]
				connection.send("\x1b[1D \x1b[1D")
			else:
				retval += key
				if ( echo ):
					connection.send(key)
				else:
					connection.send('*')
	return retval

def caseclr(text, boldcolor, normcolor):
	""" Color by character case. - Capitals returns in boldcolor, lowercase in normcolor
	 
	@param string $text Input text to color
	@param int $boldcolor Color for capital letters
	@param int $normcolor Color for lowercase letters """
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(normcolor) + "m"
	return re.sub("([A-Z:<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"

def casebold(text, boldcolor):
	""" Color by character case. - Capitals returns in bold of suplied color, lowercase in suplied color.
	 
	@param string $text Input text to color
	@param int $boldcolor Color for lowercase letters"""
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(boldcolor) + "m"
	return re.sub("([A-Z:*<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"

def normmenu(text):
	"""Return a standard colored menu entry.
	
	@param string $text Text to convert to menu entry """
	bclrstr = "  `2(`#"
	nclrstr = "`2)"
	return re.sub("\(([A-Z:<>])\)", bclrstr + r"\1" + nclrstr, text) + "`.\r\n"


def menu_2col(text1, text2, col1, col2):
	""" 2 Column Menu -  Generate a 2 column menu entry
	
	@param string $text1 Menu Option 1
	@param string $text2 Menu Option 2
	@param int $col1 Option color for menu option 1
	@param int $col2 Option color for menu option 2 """
	nclrstr = "`2)"
	bclrstr1 = "`2(\x1b[1;3"+str(col1)+"m"
	bclrstr2 = "`2(\x1b[1;3"+str(col2)+"m"
	text1col = re.sub("\(([A-Z:<>])\)", bclrstr1 + r"\1" + nclrstr, text1) + "\x1b[0m"
	text2col = re.sub("\(([A-Z:<>])\)", bclrstr2 + r"\1" + nclrstr, text2) + "\x1b[0m"
	return "  " + text1col + padnumcol(text1, 36) + text2col + "`.\r\n"

def maketime(user):
	""" Make a time since login string"""
	currenttime = time.time()
	ontime = int(currenttime) - int(user.logontime)
	sec = ontime % 60
	min = ( ontime - sec ) / 60
	if ( sec < 10 ):
		ptime = str(min) + ':0' + str(sec)
	else: 
		ptime = str(min) + ':' + str(sec)
	return ptime

def padnumcol(text, col):
	"""Pad a selection of text to be a specied number of columns wide.
	
	@param string $text Text to pad
	@param int $col Number of columns to fill """
	ltext = re.sub('`.', '', text)
	col = col - len(ltext)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval

def padright(text, col):
	""" Pad a selection of text to be a specied number of columns wide, right justified.
	 
	@param string $text Text to pad
	@param int $col Number of columns to fill """
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval + text

def getclientconfig(connection, log):
	""" Retrieve client generated line speed / noise configuration for emulation """
	LINESPEED = 0
	LINENOISE = 0
	slowecho(connection, "\r\n"+normmenu('(A) 1200 Baud'))
	slowecho(connection, normmenu('(B) 2400 Baud'))
	slowecho(connection, normmenu('(C) 28800 Baud'))
	slowecho(connection, normmenu('(D) T1 Line (no delay)'))
	slowecho(connection, casebold('\r\n  Emulated Linespeed [B] : ', 7))
	linespeeds = ['2400', '1200', '28800', 'ISDN' ]
	quitter = False
	while ( not quitter):
		data = connection.recv(2)
		if not data: break
		elif ( data == "A" or data == "a" ):
			connection.send('A')
			LINESPEED = 1
			quitter = True
		elif ( data == "B" or data == "b" ):
			connection.send('B')
			LINESPEED = 0
			quitter = True
		elif ( data == "C" or data == "c" ):
			connection.send('C')
			LINESPEED = 2
			quitter = True
		elif ( data == "D" or data == "d" ):
			connection.send('D')
			LINESPEED = 3
			quitter = True
		else:
			connection.send('B')
			LINESPEED = 0
			quitter = True
	log.add('   ** User at emulated linespeed::' + linespeeds[LINESPEED] + ' ' + str(connection.getpeername()))
	slowecho(connection, casebold('\r\n  Emulated Line Noise [y/N] : ', 7))
	quitter = False
	while ( not quitter):
		data = connection.recv(2)
		if not data: break
		elif ( data == "Y" or data == "y" ):
			connection.send('Y')
			log.add('   ** User at emulated line noise:: ' + str(connection.getpeername()))
			LINENOISE = 1
			quitter = True
		else:
			connection.send('N')
			LINENOISE = 0
			quitter = True
	return (LINESPEED, LINENOISE)
