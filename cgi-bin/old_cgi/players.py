#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface
import elo

print "Content-type:text/plain\n\n"
db = DatabaseInterface( )
players_dict = db.players( )

print json.dumps( players_dict )
