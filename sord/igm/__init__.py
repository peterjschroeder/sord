""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * This sub-package contains all site-specific in-game-modules.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please.
 
 *** Notes on IGM's:

 * All IGM module files should be listed in the above import.
 * To install a new IGM, add another tuple to the list of tuples in igmlist

 *  ex:  igmlist = list( ( 'KEY COMMAND', igm_module.igm_main_class() , 'DISPLAY NAME' ) )
  
 * IGM Module files *may* include more than one IGM class, list them seperatly.
 * IGM Module classes *must* have a run(<sordUser object>) method, used to initiate the IGM
 * IGM Module classes *may* have an __init__() method
 *   !! but it is called too early in processing to do anything other that basic setup !!

 * NOTE: See dht.py for an example of a working IGM (has access to basic display functions, 
 *       basic user info display functions, and the full user object.
      
 * WARNING: The IGMs are loaded with the server, and do nothing (unavoidable in order to enumerate them)
 *          However, they are also loaded for each connected user again.  As you might imagine, if an
 *          IGM uses a lot of memory, or you have a ton of IGMS, this can be a performance hit.  Natrually,
 *          with modern systems, this isn't quite the problem it was in the days of LORD and a BBS running 
 *          on a 386, but it is certainly something to be aware of.
 """
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

from . import dht

igmlist = [('D', dht.dht(), "Dark Horse Tavern")]

