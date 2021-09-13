#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains embedded webserver.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
 
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

from BaseHTTPServer import BaseHTTPRequestHandler

import binascii, sqlite3, re

class sordWebserver(BaseHTTPRequestHandler):
	""" S.O.R.D. Embedded webserver """
	def __init__(self,config,*args,**kwargs):
		""" Initialize new server based on BaseHTTPRequestHandler """
		self.config = config
		BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
		
	def do_GET(self):
		""" Override typical GET behavior of server.
		
		Note: this server does not support POST at all.  Very small subset of options"""
		key = self.path[1:]
		if ( key == "drag.png" ):
			self.send_response(200)
			self.send_header('content-type', 'image/png')
			self.end_headers()
			self.wfile.write(binascii.a2b_base64(self.dragonimg()))
		elif ( key == "" or key == "index.html" ):
			self.send_response(200)
			self.send_header('content-type', 'text/html')
			self.end_headers()
			self.wfile.write(self.index())
		elif ( key == "stats" or key == "stats/" ):
			self.send_response(200)
			self.send_header('content-type', 'text/html')
			self.end_headers()
			self.wfile.write(self.stats())
		elif ( key == "conf" or key == "conf/" ):
			self.send_response(200)
			self.send_header('content-type', 'text/html')
			self.end_headers()
			self.wfile.write(self.conf())
		elif ( key == "play" or key == "play/" ):
			self.send_response(200)
			self.send_header('content-type', 'text/html')
			self.end_headers()
			self.wfile.write(self.play())
		else:
			self.send_error(404, "Page not found")
		
	def line(self):
			""" Dark Green Horizontal Rule """
			return "<span style=\"color: darkgreen\">-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-</span>"

	def padnumcol(self, text, col):
		"""Pad a selection of text to be a specied number of columns wide."""
		col = col - len(text)
		ittr = 0
		retval = ""
		while ( ittr < col ):
			retval += " "
			ittr += 1
		return retval
	
	def padright(self, text, col):
		""" Pad a selection of text to be a specied number of columns wide, right justified. """
		col = col - len(text)
		ittr = 0
		retval = ""
		while ( ittr < col ):
			retval += " "
			ittr += 1
		return retval + text
			
	def index(self):
		""" Site Index """
		ret = """<html><head><title>Saga of the Red Dragon</title><style>a { color: #ccc; text-decoration: none; } a:hover { text-decoration: underline; }</style></head>
<body style="background-color: black; color: white; background-image: url(drag.png); background-repeat: no-repeat; background-position: top right;">
<h1><span style="color: #F77">S</span><span style="color: #F00">aga of the</span> <span style="color: #F77">R</span><span style="color: #F00">ed</span> <span style="color: #F77">D</span><span style="color: #F00">ragon</span></h1>
<font size="+1"><pre>
<span style="color: darkgreen">-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-</span>
<span style="color: darkgreen">   A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
   All attempts were made to be as close to the original as possible, 
   including some original artwork, the original fight equations, and 
   most especially the original spelling and punctuation mistakes.  Enjoy.</span>
<span style="color: darkgreen">-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-</span>

    <a href="/stats"><span style="color: darkgreen">(</span><span style="color: magenta">L</span><span style="color: darkgreen">)ist Players</span></a>
    <a href="/conf"><span style="color: darkgreen">(</span><span style="color: magenta">C</span><span style="color: darkgreen">)onfiguration of this Server</span></a>
    <a href="/play"><span style="color: darkgreen">(</span><span style="color: magenta">P</span><span style="color: darkgreen">)lay the game</span></a>
</pre></font></body></html>"""
		return ret
		
	def play(self):
		""" Show instructions for connecting to the server """
		ret = """<html><head><title>Saga of the Red Dragon</title><style>a { color: #ccc; text-decoration: none; } a:hover { text-decoration: underline; }</style></head><body style="background-color: black; color: white; background-image: url(drag.png); background-repeat: no-repeat; background-position: top right;"><h1><span style="color: #F77">S</span><span style="color: #F00">aga of the</span> <span style="color: #F77">R</span><span style="color: #F00">ed</span> <span style="color: #F77">D</span><span style="color: #F00">ragon</span></h1><font size="+2"><pre>"""		
		ret += "   <span style=\"color: darkgreen\">To play the game, simply telnet to host: \n\n     "+self.config.host+"\n\n   on port # \n\n     "+str(self.config.port)+"</span>\n"
		ret += """</pre></font></body></html>"""
		return ret
		
	def conf(self):
		""" Show current server configuration """
		ret = """<html><head><title>Saga of the Red Dragon</title><style>a { color: #ccc; text-decoration: none; } a:hover { text-decoration: underline; }</style></head><body style="background-color: black; color: white; background-image: url(drag.png); background-repeat: no-repeat; background-position: top right;"><h1><span style="color: #F77">S</span><span style="color: #F00">aga of the</span> <span style="color: #F77">R</span><span style="color: #F00">ed</span> <span style="color: #F77">D</span><span style="color: #F00">ragon</span></h1><font size="+1"><pre>"""		
		ret += "   <span style=\"color: darkgreen\">telnet://"+self.config.host+":"+str(self.config.port)+"</span>\n"
		ret += "\n   <span style=\"color: darkgreen\">Compiled June 25, 2009: Version </span><span style=\"color: white\">"+self.config.version+"</span>"
		ret += "\n   <span style=\"color: darkgreen\">(c) pre-2009 by Someone Else</span>\n\n   <span style=\"color: white\">REGISTERED TO</span><span style=\"color: blue\"> "+self.config.admin+"</span>\n"
		ret += "\n   <span style=\"color: darkgreen\">Players are deleted after <strong>"+str(self.config.delinactive)+"</strong> real days of inactivity.</span>"
		ret += "\n   <span style=\"color: darkgreen\">Players are enjoying <strong>"+str(self.config.ffight)+"</strong> forest fights per day.</span>"
		ret += "\n   <span style=\"color: darkgreen\">Players are enjoying <strong>"+str(self.config.pfight)+"</strong> player fights per day.</span>"
		ret += "\n   <span style=\"color: darkgreen\">Players are enjoying <strong>"+str(self.config.bankinterest)+"%</strong> interest at the bank per day.</span>"
		ret += "\n   <span style=\"color: darkgreen\">The current game day is <strong>"+str(self.config.daylength)+"</strong> real hours long.</span>"
		ret += """</pre></font></body></html>"""
		return ret
		
	def stats(self):
		""" Show player standings """
		output  = "<html><head><title>Saga of the Red Dragon - Player Standings</title></head>"
		output += """<body style="background-color: black; color: white; background-image: url(drag.png); background-repeat: no-repeat; background-position: top right;">"""
		output += """<h1><span style="color: #F77">S</span><span style="color: #F00">aga of the</span> <span style="color: #F77">R</span><span style="color: #F00">ed</span> <span style="color: #F77">D</span><span style="color: #F00">ragon</span></h1>"""
		output += "<h2><span style=\"color: lightgreen\">Player Standings</h2><font size=\"+1\"><pre>"
				
		dbc = sqlite3.connect(self.config.progpath+"/"+self.config.sqlitefile)
		
		db = dbc.cursor()
		db.execute("SELECT userid, fullname, exp, level, cls, spclm, spcld, spclt, sex, alive FROM users WHERE 1 ORDER BY exp DESC")
		output += "\n<span style=\"color: green\">     Name                    Experience    Level    Mastered    Status       </span>\n" + self.line() + "\n"
		for line in db.fetchall():
			if ( line[8] == 2 ):
				lineSex = "<span style=\"color: magenta\">F</span> "
			else:
				lineSex = "  "
				
			lineClass = "<span style=\"color:#F77\">"
			if ( line[4] == 1 ):
				lineClass += "D "
			elif ( line[4] == 2 ):
				lineClass += "M "
			else:
				lineClass += "T "
			lineClass += "</span>"
			
			lineMaster = ""
			if ( line[6] > 19 ):
				if ( line[6] > 39 ):
					lineMaster += "<span style=\"color:#fff\">D </span>"
				else:
					lineMaster += "<span style=\"color:#ccc\">D </span>"
			else:
				lineMaster += "  "
				
			if ( line[5] > 19 ):
				if ( line[5] > 39 ):
					lineMaster += "<span style=\"color:#fff\">M </span>"
				else:
					lineMaster += "<span style=\"color:#ccc\">M </span>"
			else:
				lineMaster += "  "
							
			if ( line[7] > 19 ):
				if ( line[7] > 39 ):
					lineMaster += "<span style=\"color:#fff\">T </span>"
				else:
					lineMaster += "<span style=\"color:#ccc\">T </span>"
			else:
				lineMaster += "  "
										
			
			if ( line[9] == 1 ):
				lineStatus = "<span style=\"color: #6F6\">Alive</span>"
			else:
				lineStatus = "<span style=\"color: #F00\"> Dead</span>"
			
			name = re.sub('`.', '', str(line[1]))
			output += lineSex + lineClass + "<span style=\"color: green\"> " + name + self.padnumcol(name, 24) + self.padright(str(line[2]), 10)
			output += self.padright(str(line[3]), 9) + "       " + lineMaster + '    ' + lineStatus + "       \n"
		db.close()
		dbc.close()
		output += "</pre></font></center></body></html>"
		return output
		
	def dragonimg(self):
		""" Dragon Background Image (base64 encoded) """
		img = """iVBORw0KGgoAAAANSUhEUgAAAjsAAAKBCAMAAACGWZp6AAAAAXNSR0IArs4c
6QAAAv1QTFRFAAEACAAAAAMGBQIHEQICGAEBHgEABQcUIgECBwoHLgACBAof
KgMAEwoBCwkkJgQHNAEABAsrOAACQQAEPAIADxEOTQAARgMAABFKAhM9WAEA
YAABHRIdCBkZaAAACR0DcgAAJBgHGRoYeAEAfgABggAATw8JiQABZA0AjQEA
Bx9iKhotQBkDlQAClwAAMR8GRhcalwEMlgESoAABngAImgQGBDIDrQACVBsF
lgUgpQQAnAcAmAYZcRIcKCgmSR8rpAgNFytUTCYCJSw8nw4CqAsHOywXpg0V
bR8fuwsCqA4fIjQ3uA4JTDAJNDYVoRUdMzQzohUnnhcvaigvuRQSjCIiBE4C
uRgacTACthofzhYEtB0kiSkyazFAazgBsSAuzRsPtCEqhzAm0RshryQ2yx8X
RENCjjQAlTICQ0gbXkEVyiIdKUiCNU40aUMIySQkqy0nxiYpPExQgUEAxigx
nzoBNU9tpzM9rjIzSUxbwC4x4ygSXEw7vy86UU9On0IAl0YB4i4e1zAr3i8j
4S8r1zE5lkoC2TI0zTY70jY2mkVIW1wg4zIznE8A5TY76Dcq3zkxBX8I4Do5
2T076Do2YF9djFobR2V8fmEyll4KT2eIqlsAeGJTYGZzhmYpbm1rXHF6qGRg
tWsHe30srXUia4g7fH18a4GIYIGrsHkThnxzY4OXnXtDn38wnH5SeIOTRoze
ALoBqoYik4Zx04UUlI6FepWVjZCUkJCNhpOVkZOAyo4LlZeUm5aVlZicpJSc
o5iCu5k0p583kZyZh5+doZifpJmSlZyup5uc15g+sZqdn6GeAOIAy6Mfx55y
w640oazBkLHEs6qjrK2uvKqdlcBDqrpGvLk/3LYdzrox6bNn6bRfybmuzLe5
t73Ivb27ssHY0b2n3sYxrcva19FA6sSKz9dFi93ex8zXwM/T1cu+6Mufz87M
sdjZ5tszfufy4d1G49W84OJG2eVLy+pK4t7S6exF3eLM5d/e3+He3eLl2OTj
yujm5uzv6uzpjvoH9wAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCa
nBgAAAAHdElNRQfaCBsWIB6/Oci1AAAgAElEQVR42uy9fUxbZ5o3bIMxhHqK
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"""
		return img

