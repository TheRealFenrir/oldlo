#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append('/var/www/elo/database_interface')

from DatabaseInterface import DatabaseInterface
import elo

form = cgi.FieldStorage( ) 

player_id = form.getvalue( 'player_id' )
league_id = form.getvalue( 'league_id' )
db = DatabaseInterface( )
playerId = db.addPlayerToLeague( player_id, league_id )
print "Content-type:text/plain\n\n"
