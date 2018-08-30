#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface
import elo

db = DatabaseInterface( )
for player in db.players( ):
    db.updateElo( player[ 'id' ], 1400 )

for game in db.history( ):
    #print "(" + str( game[ 'p1_id' ] ) + ", " + str( game[ 'p2_id' ] ) + ") " + str( game[ 't1_score' ] ) + "-" + str( game[ 't2_score' ] ) + " (" + str( game[ 'p3_id' ] ) + ", " + str( game[ 'p4_id' ] ) + ")"
    p1_elo = db.elo( game[ 'p1_id' ] )
    p2_elo = db.elo( game[ 'p2_id' ] )
    p3_elo = db.elo( game[ 'p3_id' ] )
    p4_elo = db.elo( game[ 'p4_id' ] )

    t1_score = game[ 't1_score' ]
    t2_score = game[ 't2_score' ]

    t1_elo = ( p1_elo + p2_elo ) / 2
    t2_elo = ( p3_elo + p4_elo ) / 2

    elo_change = elo.calculateNewElos( 128, 1000, [ t1_score, t2_score ], [ t1_elo, t2_elo ] )

    db.updateElo( game[ 'p1_id' ], p1_elo + elo_change[0] )
    db.updateElo( game[ 'p2_id' ], p2_elo + elo_change[0] )
    db.updateElo( game[ 'p3_id' ], p3_elo + elo_change[1] )
    db.updateElo( game[ 'p4_id' ], p4_elo + elo_change[1] )
