#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append('/var/www/elo/database_interface')

from DatabaseInterface import DatabaseInterface
import elo

form = cgi.FieldStorage( ) 

name = form.getvalue( 'name' )
db = DatabaseInterface( )
playerId = db.addPlayer( name )
print json.dumps( playerId )
