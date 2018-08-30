#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface

print "Content-type:text/plain\n\n"
db = DatabaseInterface( )
print json.dumps( db.listLeagues( ) )
