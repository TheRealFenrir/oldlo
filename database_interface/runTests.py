#!/usr/bin/env python

from DatabaseInterface import DatabaseInterface
from DatabaseInterface import TestDatabaseInterface

db = TestDatabaseInterface( )

db.addLeague( "testLeague1" )
db.addLeague( "testLeague2" )

db.addPlayer( "dan" )
db.addPlayer( "adam" )
db.addPlayer( "hugh" )
db.addPlayer( "steph" )
db.addPlayer( "lindsay" )

db.addPlayerToLeague( 5, 1 )
db.addPlayerToLeague( 2, 1 )
db.addPlayerToLeague( 3, 1 )
db.addPlayerToLeague( 1, 1 )

db.addPlayerToLeague( 1, 2 )
db.addPlayerToLeague( 4, 2 )
db.addPlayerToLeague( 3, 2 )
db.addPlayerToLeague( 5, 2 )

db.updatePlayerElo( "dan", "testLeague1", 1001 );
db.updatePlayerElo( "adam", "testLeague1", 1002 );
db.updatePlayerElo( "hugh", "testLeague1", 1003 );
db.updatePlayerElo( "lindsay", "testLeague1", 1005 );

db.updatePlayerElo( "dan", "testLeague2", 1101 );
db.updatePlayerElo( "hugh", "testLeague2", 1103 );
db.updatePlayerElo( "steph", "testLeague2", 1104 );
db.updatePlayerElo( "lindsay", "testLeague2", 1105 );
