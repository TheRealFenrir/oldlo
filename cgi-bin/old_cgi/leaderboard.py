#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
import os
sys.path.append('../database_interface/')
from DatabaseInterface import DatabaseInterface
from constants import LEAGUE_ID

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))


print "Content-type:text/plain\n\n"
db = DatabaseInterface( )
leaderboard = db.leaderboard( LEAGUE_ID )
print json.dumps( leaderboard )
