#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Main Server Program
 
 * Memory Usage:  around 25M base, plus about 11M per client.
 * Magic Number: 6342 / 7507 (-1165)
 
 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import threading, time, sys, traceback, random, socket, sqlite3, os, optparse, locale
import sord
from functools import partial
from BaseHTTPServer import HTTPServer

#locale.setlocale(locale.LC_ALL, '')

p = optparse.OptionParser(version=__version__,description="Saga of the Red Dragon :: "+__version__,epilog="A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  All attempts were made to be as close to the original as possible, including some original artwork, the original fight equations, and most especially the original spelling and punctuation mistakes.  Enjoy.")

p.add_option("-t", "--testing", help="telnet server in testing (random port) mode", action="store_true", dest="testing")
p.add_option("-d", "--debug", help="put server in debug (auto login) mode", action="store_true", dest="debug")
p.add_option("-a", "--ansi-skip", help="skip large banner ansi", action="store_true", dest="ansiskip")
p.add_option("-w", "--web-off", help="do not start web server", action="store_true", dest="weboff")
p.add_option("-n", "--force-new-day", help="force new day on next login", action="store_true", dest="newday")
p.set_defaults(testing=False, debug=False, ansiskip=False, weboff=False, newday=False)

if ( __name__ == '__main__' ) :
	opt, args = p.parse_args()
	config = sord.config.config.sordConfig(opt.testing)
else: # Trap for pydoc.
	config = sord.config.config.sordConfig(1)

log = sord.base.logger.sordLogger()

if ( __name__ == '__main__' ) :
	if opt.debug:
		config.fulldebug = True
	if opt.ansiskip:
		config.ansiskip = True
	if opt.weboff:
		config.webport = 0
	if opt.newday:
		config.forcenewday = True

try:
	sockobj = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	sockobj.bind(('', config.port))
	sockobj.listen(5)
except:
	print "Socket In Use!"
	sys.exit()

class eachClient(threading.Thread):
	""" Actual client->server thread process """
	def __init__(self, connection, config, log):
		threading.Thread.__init__(self)
		self.daemon = True
		self.connection = connection
		self.config = config
		self.log = log
	def run(self):
		""" Actual server->client thread process """
		connection = self.connection
		config = self.config
		log = self.log
		try:
			loggedin = False
			time.sleep(1)
			thisClientAddress = connection.getpeername()
			
			connection.send(chr(255) + chr(253) + chr(34)) # drop to character mode.
			connection.send(chr(255) + chr(251) + chr(1))  # no local echo (client side)
			connection.send(chr(255) + chr(253) + chr(39))
			connection.send(chr(255) + chr(250) + chr(39) + chr(1) + chr(255) + chr(240))
			connection.send("Welcome to SORD\r\n")
			data = connection.recv(4096) # dump garbage.
			data_chars = map(lambda x:x, data)
			data_string = "";
			for char in data_chars:
				data_string = data_string + " " + str(ord(char))
			log.add(data_string)
			connection.send(data_string)
			data = connection.recv(4096) # dump garbage.
				
			connection.settimeout(120)
			sqc = sord.base.dbase.getDB(config)
			art = sord.game.art.sordArtwork(config, sqc)
			sord.base.dbase.dayRollover(config, sqc, log)
			
			""" Line speed and noise options """
			sord.base.func.pauser(connection)
			
			
			if ( not config.fulldebug ):
				lineconfig = sord.base.func.getclientconfig(connection, log)
			else:
				lineconfig = (3,0)
			
			if ( not config.fulldebug ):
				if ( not config.ansiskip ):
					sord.base.func.slowecho(connection, art.header(), lineconfig[0], lineconfig[1])
				sord.base.func.pauser(connection)
		
			intro = sord.game.main.intro(connection, config, art, log, sqc, lineconfig)
			if ( not config.fulldebug ):
				intro.run()
	
			ittr = 0
			if ( config.fulldebug ):
				loggedin = True
				currentUser = sord.base.userlib.sorduser(config.gameadmin, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
		
			""" Login Code """
			while ( not loggedin ):
				username = ""
				password = ""
				currentUser = ""
				ittr += 1
				if ( ittr > 3 ):
					sord.base.func.slowecho(connection, sord.base.func.casebold("\r\n\r\nDisconnecting - Too Many Login Attempts\r\n", 1), lineconfig[0], lineconfig[1])
					log.add('  !!! Too Many Login Attemtps::' + str(thisClientAddress))
					raise Exception('normal', "Too many bad logins!")
				sord.base.func.slowecho(connection, sord.base.func.casebold("\r\n\r\nWelcome Warrior!  Enter Your Login Name (OR '`9new`2') :-: ", 2), lineconfig[0], lineconfig[1])
				username = sord.base.func.getLine(connection, True)
				currentUser = sord.base.userlib.sorduser(username, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
				if ( currentUser.thisUserID > 0 ):
					sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nPassword :-: ",2), lineconfig[0], lineconfig[1]);  
					password = sord.base.func.getLine(connection, False)
					password = password.strip()
					if ( password == currentUser.thisPassword ):
						loggedin = True
					else:
						sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nIncorrect Password\r\n", 1), lineconfig[0], lineconfig[1])
				else:
					if ( username == "new" ):
						log.add('   ** New User! ' + str(thisClientAddress))
						newusername = sord.game.util.newuser(currentUser)
						currentUser = sord.base.userlib.sorduser(newusername, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
						newclass = currentUser.cls
						currentUser.updateSkillUse(newclass, 1)
						currentUser.updateSkillPoint(newclass, 1)
						loggedin = True
						log.add('   ** User Created: ' + newusername)
					else:
						sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nUser Name Not Found!\r\n",2), lineconfig[0], lineconfig[1])
					
			currentUser.login()
			log.add('   ** User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress))
	
			if ( currentUser.alive == 0 ) :
				currentUser.write(sord.base.func.casebold("\r\n\r\n  I'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
				raise Exception('normal', "User is DOA.  Bummer for them.")
			elif ( currentUser.alive == 2 ) :
				currentUser.write(sord.base.func.casebold("\r\n\r\n  You feel like shit! (you were dead - much better now though\r\n", 1))
				currentUser.alive = 1
			
			if ( not config.fulldebug ):
				sord.game.util.dailyhappen(True, currentUser)
				currentUser.pause()
				currentUser.write(sord.game.util.who(currentUser))
				currentUser.pause()
				currentUser.write(sord.game.util.viewstats(currentUser))
				currentUser.pause()
				sord.game.util.readmail(currentUser)
		
			townSquare = sord.game.main.mainmenu(currentUser)
			townSquare.run()
	
			exitQuote = ['The black thing inside rejoices at your departure.', 'The very earth groans at your depature.', 'The very trees seem to moan as you leave.', 'Echoing screams fill the wastelands as you close your eyes.', 'Your very soul aches as you wake up from your favorite dream.']
			exitTop = len(exitQuote) - 1
			exitThis = exitQuote[random.randint(0, exitTop)]
			connection.send(sord.base.func.casebold("\r\n\r\n   "+exitThis+"\r\n\r\n", 7))
			connection.send("NO CARRIER\r\n\r\n")
			if ( loggedin ):
				currentUser.logout()
				del currentUser
			connection.shutdown(socket.SHUT_RD)
			connection.close()
			sqc.close()
			del sqc
			del art
			log.add('  *** Thread Disconnected:' + str(thisClientAddress))
			log.remcon()
			
		except Exception as e:
			skipClose = False
			if ( e[0] == "timed out" ):
				log.add("  *** Network Timeout: " + str(thisClientAddress))
				connection.send("\r\n\r\n\x1b[0mNetwork Connection has timed out.  120sec of inactivity.\r\n\r\n")
				connection.send("NO CARRIER\r\n\r\n")
			elif ( e[0] == "normal" ):
				log.add("  *** Normal Exit ("+e[1]+"): " + str(thisClientAddress))
			elif type(e) is socket.error:
				log.add("  *** Remote Closed Host: " + str(thisClientAddress))
				skipClose = True
			else:
				log.add("  !!! Program Error Encountered("+ str(e) + "): " + str(thisClientAddress))
				try:
					connection.send("\r\n\x1b[0mProgram Error Encountered ( "+str(e)+" ), Closing Connection.\r\n")
					connection.send("NO CARRIER\r\n\r\n")
				except:
					log.add("   && No message to client")
				formatted = traceback.format_exc().splitlines()
				for formattedline in formatted:
					log.add("    ~~~ " + formattedline)
			if ( loggedin ):
				currentUser.logout()
				del currentUser
			log.remcon()
			sqc.close()
			del sqc
			del art
			if ( not skipClose ):
				connection.shutdown(socket.SHUT_RD)
				connection.close()
	
def sordLoop(config, log):
	""" Main program loop, spawn telnetServe thread """
	log.add("-=-=-=-=-=-= SORD Server Version " + config.version + " =-=-=-=-=-=-")	
	sord.base.dbase.initialTest(config, log)
	log.add(" === Starting Server on port: "+str(config.port))
	igms = list()
	for item in sord.igm.igmlist:
		igms.append(item[2])
	log.add(" === Found IGMs: "+str(igms))
	
	wServer = webServe(config, log)
	wServer.start()
	
	tServer = telnetServe(sockobj, config, log)
	tServer.start()
	
	display = sord.base.commandcenter.sordCommandCenter(config, log)
	display.run()

	try:
		sockobj.shutdown(2)
	except:
		pass
	sockobj.close()
	sys.exit()

class telnetServe(threading.Thread):
	""" Telnet Server Thread Object """
	def __init__(self, sockobj, config, log):
		threading.Thread.__init__(self)
		self.daemon = True
		self.config = config
		self.log = log
		self.sockobj = sockobj
	def run(self):
		while True:
			connection, address = self.sockobj.accept()
			log.add('  *** Server connected by'+str(address))
			thisClient = eachClient(connection,self.config,self.log)
			thisClient.start()
			self.log.addcon()

class webServe(threading.Thread):
	def __init__(self, config, log):
		threading.Thread.__init__(self)
		self.daemon = True
		self.config = config
		self.log = log
	def run(self):
		if ( self.config.webport > 0 ):
			self.log.add(" === Starting Embedded Web Server, port: "+str(self.config.webport))
			srvaddr = ("", self.config.webport)
			sys.stderr = self.log
			srvobj = HTTPServer(srvaddr, partial(sord.base.webserve.sordWebserver, self.config))
			srvobj.serve_forever()


		
if ( __name__ == '__main__' ) :
	sordLoop(config, log) # MAIN PROGRAM LOOP!


