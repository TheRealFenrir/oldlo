#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
import os
from constants import LEAGUE_ID

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface
import elo

form = cgi.FieldStorage() 

p1_id = int(form.getvalue('p1_id'))
p2_id = int(form.getvalue('p2_id'))
p3_id = int(form.getvalue('p3_id'))
p4_id = int(form.getvalue('p4_id'))
#league_id = form.getvalue('league_id')
league_id = LEAGUE_ID 
t1_score = int(form.getvalue('t1_score'))
t2_score = int(form.getvalue('t2_score'))

db = DatabaseInterface( )

if t1_score > t2_score:
    gameId = db.addGame( p1_id, p2_id, p3_id, p4_id, t1_score - t2_score, league_id )
else:
    gameId = db.addGame( p3_id, p4_id, p1_id, p2_id, t2_score - t1_score, league_id )

print "Content-type:text/plain\n\n"

print json.dumps( gameId )

