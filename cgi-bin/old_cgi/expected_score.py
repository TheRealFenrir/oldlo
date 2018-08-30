#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append('/var/www/elo/database_interface')

from DatabaseInterface import DatabaseInterface
import elo

print "Content-type:text/plain\n\n"

form = cgi.FieldStorage() 

p1_id = form.getvalue( 'p1_id' )
p2_id = form.getvalue( 'p2_id' )
p3_id = form.getvalue( 'p3_id' )
p4_id = form.getvalue( 'p4_id' )

db = DatabaseInterface( ) 

p1_elo = db.elo( p1_id )
p2_elo = db.elo( p2_id )
p3_elo = db.elo( p3_id )
p4_elo = db.elo( p4_id )

t1_elo = ( p1_elo + p2_elo ) / 2
t2_elo = ( p3_elo + p4_elo ) / 2

expected_score = elo.calculateExpectedScore( 1000, [ t1_elo, t2_elo ], 5, True )

print json.dumps( expected_score )
