#!/usr/bin/env python
#!/usr/bin/python

# Later, the front end should call add_player and add_league_player

import cgi, cgitb 
import sys
import json
import os
sys.path.append('/var/www/elo/database_interface')

from DatabaseInterface import DatabaseInterface
import elo

from constants import LEAGUE_ID

form = cgi.FieldStorage( ) 

name = form.getvalue( 'name' )
#leagueId = form.getvalue( 'leagueId' )
leagueId = LEAGUE_ID 
db = DatabaseInterface( )
playerId = db.addPlayer( name )["id"]
db.addPlayerToLeague( playerId, leagueId );
print "Content-type:text/plain\n\n"
print json.dumps( playerId )
