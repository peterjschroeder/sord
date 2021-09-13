#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains server-side command center display.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
import curses, time

class sordCommandCenter():
	""" S.O.R.D. Command Center """
	def __init__(self, config, log):
		""" Inialize new command center """
		self.config = config
		self.log = log
				
	def scrnInit(self):
		""" Init the screen """
		self.mainscrn = curses.initscr()
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
		curses.noecho()
		curses.curs_set(0)
		self.mainscrn.timeout(1000)
		
	def scrnSetup(self):
		""" Setup local screen """
		
		self.mainscrn.clear()
		self.totalY, self.totalX = self.mainscrn.getmaxyx()
		self.loglines = self.totalY - 7
		
		self.mainscrn.attron(curses.color_pair(5) | curses.A_BOLD)
		self.mainscrn.border(0)
		self.mainscrn.hline((self.totalY-3), 1,  curses.ACS_HLINE, (self.totalX-2))
		self.mainscrn.hline(2, 1, curses.ACS_HLINE, (self.totalX-2))
		self.mainscrn.attroff(curses.color_pair(5) | curses.A_BOLD)
		
		self.mainscrn.addstr((self.totalY-3), (self.totalX-17), '(Q,N,D,A,S,C,?)')
		self.mainscrn.addstr(2,7, 'server')
		self.mainscrn.addstr(2,14, 'log')
		self.mainscrn.addstr((self.totalY-3),7,'server')
		self.mainscrn.addstr((self.totalY-3),14, 'stats')
		
		title = [
			(21, 'Saga Of The Red Dragon -+- Command Center', curses.A_BOLD),
			(21, 'S', curses.color_pair(3) | curses.A_BOLD),
			(16, 'O', curses.color_pair(3) | curses.A_BOLD),
			(13, 'T', curses.color_pair(3) | curses.A_BOLD),
			(9, 'R', curses.color_pair(3) | curses.A_BOLD),
			(5, 'D', curses.color_pair(3) | curses.A_BOLD),
			(20, 'aga', curses.color_pair(3)),
			(15, 'f', curses.color_pair(3)),
			(12, 'he', curses.color_pair(3)),
			(8, 'ed', curses.color_pair(3)),
			(4, 'ragon', curses.color_pair(3)),
			(-7, 'ommand', curses.color_pair(0)),
			(-15, 'enter', curses.color_pair(0)) ]
			
		for item in title:
			self.mainscrn.addstr( 1, (self.totalX / 2) - item[0], item[1], item[2])
		
		chars = [
			[curses.ACS_BTEE, [(self.totalY-1,24), (self.totalY-1,44), (self.totalY-1,60)]],
			[curses.ACS_TTEE, [(self.totalY-3,24), (self.totalY-3,44), (self.totalY-3,60)]],
			["|", [(self.totalY-2,24), (self.totalY-2,44), (self.totalY-2,60)]],
			[curses.ACS_LTEE, [(self.totalY-3,0), (2,0)]],
			[curses.ACS_RTEE, [(self.totalY-3,self.totalX-1), (2,self.totalX-1)]]]
		
		for items in chars:
			for item in items[1]:
				self.mainscrn.addch(item[0], item[1], items[0], curses.color_pair(5) | curses.A_BOLD)
				
		headers = [
			(2, 'Connected Peers:'),
			(26, 'Total Peers:'),
			(46, 'Port:'),
			(62, 'Time:')]
		
		for item in headers:
			self.mainscrn.addstr(self.totalY-2, item[0], item[1], curses.color_pair(2))
			
	def run(self):
		""" Run command center logic """
		self.scrnInit()
		self.scrnSetup()
		doCmdCntr = True
		
		types = [ 
			(' === ', curses.color_pair(4) | curses.A_BOLD),
			(' *** ', curses.color_pair(4)),
			(' ** ',  curses.color_pair(1) | curses.A_BOLD),
			(' !!! ', curses.color_pair(3)),
			(' ~~~ ', curses.color_pair(3) | curses.A_BOLD),
			(' && ',  curses.color_pair(3) | curses.A_BOLD),
			(' -w- ', curses.color_pair(2)),
			('-=-',   curses.color_pair(0) | curses.A_BOLD)]
			
		if self.config.fulldebug:
			self.log.add(" !!! DEBUG MODE :: FULL DEBUG ENABLED !!!")
			self.mainscrn.addstr(self.totalY-3, 3, 'D', curses.A_BOLD)
			
		if self.config.ansiskip:
			self.log.add(" !!! DEBUG MODE :: ANSI SKIP ENABLED !!!")
			self.mainscrn.addstr(self.totalY-3, 5, 'A', curses.A_BOLD)
			
		if self.config.forcenewday:
			self.log.add(" !!! DEBUG MODE :: NEW DAY FORCE !!!")
			self.mainscrn.addstr(self.totalY-3, 1, 'N', curses.A_BOLD)

		while doCmdCntr:
			try:
				lineno = 3
				linelength = self.totalX - 4
				for line in self.log.show(self.loglines):
					thisattr = curses.color_pair(0)
					for item in types:
						if ( line.find(item[0]) > -1 ):
							thisattr = item[1]
					self.mainscrn.addstr(lineno, 2, line.ljust(linelength)[:linelength], thisattr)
					self.mainscrn.chgat(lineno, 2, 17, curses.color_pair(0))
					self.mainscrn.chgat(lineno, 19, 2, curses.color_pair(5) | curses.A_BOLD)
					lineno += 1
				self.mainscrn.addstr(self.totalY-2, 19, str(self.log.getactive()), curses.color_pair(4))
				self.mainscrn.addstr(self.totalY-2, 39, str(self.log.gettotal()), curses.color_pair(4))
				self.mainscrn.addstr(self.totalY-2, 52, str(self.config.port), curses.color_pair(4) | curses.A_BOLD)
				self.mainscrn.addstr(self.totalY-2, 68, time.strftime('%H:%M:%S', time.localtime()), curses.color_pair(4))
				
				if ( not self.config.forcenewday ):
					self.mainscrn.addch(self.totalY-3, 1, curses.ACS_HLINE, curses.color_pair(5) | curses.A_BOLD)
					
				self.mainscrn.refresh()
				key = self.mainscrn.getch()

				if ( key == ord('C') or key == ord('c') or key == curses.KEY_RESIZE ):
					self.scrnSetup()
				if ( key == ord('Q') or key == ord('q') ):
					f = open(self.config.progpath+"/sord.last.log", 'w')
					for line in self.log.show(100):
						f.write(line+"\n")
					f.close()
					raise KeyboardInterrupt
				if ( key == ord('S') or key == ord('s') ):
					f = open(self.config.progpath+"/sord.log", 'w')
					for line in self.log.show(100):
						f.write(line+"\n")
					f.close()
					self.log.add("  && Log File Written to "+self.config.progpath+"/sord.log")
				if ( key == ord('D') or key == ord('d') ):
					if ( self.config.fulldebug ):
						self.config.fulldebug = False
						self.log.add(" !!! DEBUG MODE :: FULL DEBUG DISABLED !!!")
						self.mainscrn.addch(self.totalY-3, 3, curses.ACS_HLINE, curses.color_pair(5) | curses.A_BOLD)
					else:
						self.config.fulldebug = True
						self.log.add(" !!! DEBUG MODE :: FULL DEBUG ENABLED !!!")
						self.mainscrn.addstr(self.totalY-3, 3, 'D', curses.A_BOLD)
				if ( key == ord('A') or key == ord('a') ):
					if ( self.config.ansiskip ):
						self.config.ansiskip = False
						self.log.add(" !!! DEBUG MODE :: ANSI SKIP DISABLED !!!")
						self.mainscrn.addch(self.totalY-3, 5, curses.ACS_HLINE, curses.color_pair(5) | curses.A_BOLD)
					else:
						self.config.ansiskip = True
						self.log.add(" !!! DEBUG MODE :: ANSI SKIP ENABLED !!!")
						self.mainscrn.addstr(self.totalY-3, 5, 'A', curses.A_BOLD)
				if ( key == ord('N') or key == ord('n') ):
					if ( self.config.forcenewday ):
						self.config.forcenewday = False
						self.log.add(" !!! DEBUG MODE :: NEW DAY FORCE DISABLED !!!")
						self.mainscrn.addch(self.totalY-3, 1, curses.ACS_HLINE, curses.color_pair(5) | curses.A_BOLD)
					else:
						self.config.forcenewday = True
						self.log.add(" !!! DEBUG MODE :: FORCE NEW DAY ENABLED !!!")
						self.mainscrn.addstr(self.totalY-3, 1, 'N', curses.A_BOLD)
				if ( key == ord('?') or key == ord('h') or key == ord('H') ):
					self.log.add("(Q) Quit to shell")
					self.log.add("(A) Toggle Long ANSI Display")
					self.log.add("(D) Toggle Debug (autologin / skip intros) Mode")
					self.log.add("(S) Save Current Log to File")
					self.log.add("(C) Clear (refresh) Screen")
					self.log.add("(N) Force New Day on Next Login")

			except KeyboardInterrupt:
				curses.endwin()
				doCmdCntr = False
				print "\nS.O.R.D. Server Exiting. (main)  GoodBye!"
