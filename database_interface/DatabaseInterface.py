#!/usr/bin/python

import MySQLdb
import elo

class DatabaseInterface:
    INITIAL_ELO = 1400
    K_CONSTANT = 128
    SPREAD_CONSTANT = 1000

    def __init__( self, dbName = "elo" ):
        '''
        Initialization function that creates MySQLdb objects for use in the database interface functions
        dbName: The name of the database to connect to, defaults to EloDatabase
        '''
        self.db = MySQLdb.connect( "localhost", "elo", "lwgelomysql" )
        self.c = self.db.cursor( )
        self.c.execute( """USE """ + dbName )

    def mean( self, numbers ):
        return float( sum( numbers ) ) / len( numbers )

    def listLeagues( self ):
        ''' Returns a list of (leagueId, leagueName) tuples '''
        self.db.query( "SELECT * FROM Leagues" )
        r = self.db.store_result( )
        return r.fetch_row( maxrows = 0 )

    def addLeague( self, leagueName ):
        '''
        Creates a new league with the name 'leagueName'
        Returns the leagueId
        '''
        self.c.execute( """INSERT INTO Leagues ( leagueName ) VALUES ( '%s' ) """ % ( leagueName ) )
        self.db.commit( )
        return { 'id': self.c.lastrowid }

    def deleteLeague( self, leagueId ):
        ''' Destroys a league with 'leagueId' '''
        self.c.execute( """DELETE FROM Games WHERE leagueId = %d""" % ( leagueId ) )
        self.c.execute( """DELETE FROM Leagues WHERE leagueId = %d""" % ( leagueId ) )
        self.db.commit( )

    def addPlayer( self, name ):
        '''
        Adds a player to the system
        Returns the playerId
        '''
        self.c.execute( """INSERT INTO Players ( PlayerName ) VALUES ( '%s' )""" % name )
        self.db.commit( )
        return { 'id': self.c.lastrowid }

    def addPlayerToLeague( self, playerId, leagueId ):
        ''' Adds a player to a league '''
        self.c.execute( """INSERT INTO LeaguePlayer ( playerId, leagueId, leagueElo ) VALUES ( '%d', '%d', %d )""" % ( playerId, leagueId, self.INITIAL_ELO ) )
        self.db.commit( )

    def listPlayersInLeague( self, leagueId ):
        ''' Returns a list of a (playerId, playerName, playerElo) tuples sorted by elo '''
        self.db.query( """SELECT p.playerId, playerName, lp.leagueElo FROM Players p INNER JOIN LeaguePlayer lp ON lp.leagueId = %d AND lp.playerId = p.playerId ORDER BY lp.leagueElo DESC""" % leagueId )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        return [ { 'id': x[ 0 ], 'name': x[ 1 ], 'elo': x[ 2 ] } for x in results ]

    def getPlayerEloInLeague( self, leagueId, playerId ):
        ''' Returns a dict describing a player's elo in a league '''
        self.db.query( """SELECT leagueElo FROM LeaguePlayer WHERE leagueId = %d AND playerId = %d""" % ( leagueId, playerId ) )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        return results[ 0 ][ 0 ]

    def getExpectedScore( self, p1Id, p2Id, p3Id, p4Id, leagueId ):
        self.db.query( "SELECT playerId, leagueElo " + 
                       "FROM LeaguePlayer " +
                       ( "WHERE leagueId = %d AND (" % leagueId ) +
                       ( "playerId = %d OR playerId = %d OR playerId = %d OR playerId = %d) " % ( p1Id, p2Id, p3Id, p4Id ) ) )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        if len( results ) != 4:
            return None

        currentElos = { x[ 0 ]: x[ 1 ] for x in results }
        return elo.calculateExpectedScore( self.SPREAD_CONSTANT, [ self.mean( [ currentElos[ p1Id ], currentElos[ p2Id ] ] ), self.mean( [ currentElos[ p3Id ], currentElos[ p4Id ] ] ) ], 5, True )

    def addGame( self, p1Id, p2Id, p3Id, p4Id, scoreDifference, leagueId, gameId = None ):
        '''
        Adds a completed game to the database
        Returns the gameId
        '''
        self.db.query( "SELECT playerId, leagueElo " + 
                       "FROM LeaguePlayer " +
                       ( "WHERE leagueId = %d AND (" % leagueId ) +
                       ( "playerId = %d OR playerId = %d OR playerId = %d OR playerId = %d) " % ( p1Id, p2Id, p3Id, p4Id ) ) )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        if len( results ) != 4:
            return None

        currentElos = { x[ 0 ]: x[ 1 ] for x in results }
        eloChange = elo.calculateNewElos( self.K_CONSTANT, self.SPREAD_CONSTANT, [ 5, 5 - scoreDifference ], [ self.mean( [ currentElos[ p1Id ], currentElos[ p2Id ] ] ), self.mean( [ currentElos[ p3Id ], currentElos[ p4Id ] ] ) ] )

        if gameId == None:
            self.c.execute( """INSERT INTO Games ( player1Id, player2Id, player3Id, player4Id, scoreDifference, date, leagueId ) VALUES ( %d, %d, %d, %d, %d, NOW( ), %d )""" % ( p1Id, p2Id, p3Id, p4Id, scoreDifference, leagueId ) )
            gameId = self.c.lastrowid;
            self.c.execute( """INSERT INTO PlayerGames ( playerId, gameId, elo ) VALUES ( %d, %d, %d )""" % ( p1Id, gameId, round( currentElos[ p1Id ] + eloChange[ 0 ] ) ) )
            self.c.execute( """INSERT INTO PlayerGames ( playerId, gameId, elo ) VALUES ( %d, %d, %d )""" % ( p2Id, gameId, round( currentElos[ p2Id ] + eloChange[ 0 ] ) ) )
            self.c.execute( """INSERT INTO PlayerGames ( playerId, gameId, elo ) VALUES ( %d, %d, %d )""" % ( p3Id, gameId, round( currentElos[ p3Id ] + eloChange[ 1 ] ) ) )
            self.c.execute( """INSERT INTO PlayerGames ( playerId, gameId, elo ) VALUES ( %d, %d, %d )""" % ( p4Id, gameId, round( currentElos[ p4Id ] + eloChange[ 1 ] ) ) )
        else:
            self.c.execute( """UPDATE PlayerGames SET elo = %d WHERE gameId = %d AND playerId = %d""" % ( round( currentElos[ p1Id ] + eloChange[ 0 ] ), gameId, p1Id ) )
            self.c.execute( """UPDATE PlayerGames SET elo = %d WHERE gameId = %d AND playerId = %d""" % ( round( currentElos[ p2Id ] + eloChange[ 0 ] ), gameId, p2Id ) )
            self.c.execute( """UPDATE PlayerGames SET elo = %d WHERE gameId = %d AND playerId = %d""" % ( round( currentElos[ p3Id ] + eloChange[ 1 ] ), gameId, p3Id ) )
            self.c.execute( """UPDATE PlayerGames SET elo = %d WHERE gameId = %d AND playerId = %d""" % ( round( currentElos[ p4Id ] + eloChange[ 1 ] ), gameId, p4Id ) )
        self.c.execute( """UPDATE LeaguePlayer SET leagueElo = %d WHERE playerId = %d AND leagueId = %d""" % ( round( currentElos[ p1Id ] + eloChange[ 0 ] ), p1Id, leagueId ) )
        self.c.execute( """UPDATE LeaguePlayer SET leagueElo = %d WHERE playerId = %d AND leagueId = %d""" % ( round( currentElos[ p2Id ] + eloChange[ 0 ] ), p2Id, leagueId ) )
        self.c.execute( """UPDATE LeaguePlayer SET leagueElo = %d WHERE playerId = %d AND leagueId = %d""" % ( round( currentElos[ p3Id ] + eloChange[ 1 ] ), p3Id, leagueId ) )
        self.c.execute( """UPDATE LeaguePlayer SET leagueElo = %d WHERE playerId = %d AND leagueId = %d""" % ( round( currentElos[ p4Id ] + eloChange[ 1 ] ), p4Id, leagueId ) )

        self.db.commit( )
        return gameId

    def refreshElos( self, leagueId ):
        self.db.query( "SELECT player1Id, player2Id, player3Id, player4Id, scoreDifference, gameId FROM Games WHERE leagueId = %d" % leagueId )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )

        self.c.execute( "UPDATE LeaguePlayer SET leagueElo = %d WHERE leagueId = %d" % ( self.INITIAL_ELO, leagueId ) )
        self.db.commit( )

        for result in results:
            self.addGame( result[ 0 ], result[ 1 ], result[ 2 ], result[ 3 ], result[ 4 ], leagueId, result[ 5 ] )

    def getPlayerHistory( self, playerId, leagueId ):
        self.db.query( "SELECT pg.elo, p1.playerName, p2.playerName, p3.playerName, p4.playerName, g.scoreDifference, g.date, CONCAT(CASE WHEN pg.playerId = p1.playerId OR pg.playerId = p2.playerId THEN 'won' ELSE 'lost' END) FROM PlayerGames pg INNER JOIN Games g ON pg.gameId = g.gameId AND g.leagueId = %d AND pg.playerId = %d LEFT JOIN Players p1 ON p1.playerId = g.player1Id LEFT JOIN Players p2 ON p2.playerId = g.player2Id LEFT JOIN Players p3 ON p3.playerId = g.player3Id LEFT JOIN Players p4 ON p4.playerId = g.player4Id" % ( leagueId, playerId ) )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        formatter = "%Y-%m-%d %H:%M"
        return [ { 'elo': x[ 0 ], 'p1Name': x[ 1 ], 'p2Name': x[ 2 ], 'p3Name': x[ 3 ], 'p4Name': x[ 4 ], 'scoreDifference': x[ 5 ], 'date': x[ 6 ].strftime( formatter ), 'result':x[7] } for x in results ]

    def getLeagueHistory( self, leagueId ):
        self.db.query( "SELECT g.gameId, g.date, p1.playerName, p2.playerName, p3.playerName, p4.playerName, g.scoreDifference FROM Games g LEFT JOIN Players p1 ON p1.playerId = g.player1Id LEFT JOIN Players p2 ON p2.playerId = g.player2Id LEFT JOIN Players p3 ON p3.playerId = g.player3Id LEFT JOIN Players p4 ON p4.playerId = g.player4Id WHERE g.leagueId = %d order by g.date DESC limit 10" % leagueId )
        r = self.db.store_result( )
        results = r.fetch_row( maxrows = 0 )
        formatter = "%Y-%m-%d %H:%M"
        return [ { 'gameId': x[ 0 ], 'date': x[ 1 ].strftime( formatter ), 'player1': x[ 2 ], 'player2': x[ 3 ], 'player3': x[ 4 ], 'player4': x[ 5 ], 'scoreDifference': x[ 6 ] } for x in results ]

    def numberOfGames( self, leagueId ):
        '''Returns the total number of games played in this league'''
        self.c.execute( "SELECT COUNT( * ) FROM Games WHERE leagueId = %d" % leagueId )
        r = self.c.fetchone( )
        return r[ 0 ]

######### IGNORE BELOW ###########

    def players( self ):
        ''' 
        Gets the list of players by id and name limited to 100 players 
        RETURN: a list of dicts each with keys: "id" and "name"
        '''
        self.db.query( """SELECT playerID, playerName FROM Players LIMIT 100""" )
        r = self.db.store_result( )
        players = r.fetch_row( maxrows = 0 )
        
        playersList = list( )
        for row in players:
            player = { }
            player["id"] = row[0]
            player["name"] = row[1]
            playersList.append( player )
 
        return playersList

    def elo( self, playerID ):
        '''
        Gets the elo for a specified player
        PARAM: playerID ( NOTE: must be playerID not playerName )
        RETURN: the int value of the players elo
        '''
        self.c.execute( """SELECT elo FROM Players WHERE playerID = %s""", ( playerID, ) )
        r = self.c.fetchone( )
        return r[0]  

    def leagueDuration( self ):
        '''
        Gets the time that league has been ongoing
        RETURN: the datetime value of time that the league has been ongoing
        '''
        self.c.execute( """SELECT TIMESTAMPDIFF( DAY, dateTime, CURDATE( ) ) AS leagueDuration FROM GameInfo WHERE GameID = 1""" )
        r = self.c.fetchone( )
        return r[0]

# This is a test class ONLY and should never be 
# created when running from the website
class TestDatabaseInterface(DatabaseInterface):
    def __init__( self, dbName = "elo" ):
       DatabaseInterface.__init__( self, dbName )

    def updatePlayerElo( self, playerName, leagueName, newElo ):
        ''' Updates a player's rating in a league '''
        self.c.execute( "UPDATE LeaguePlayer AS lp INNER JOIN (" +
                            "SELECT p.playerId, l.leagueId FROM Players p INNER JOIN Leagues l " +
                            "WHERE p.playerName='%s' AND l.leagueName='%s') r ON " % ( playerName, leagueName ) +
                        "lp.leagueId=r.leagueId AND lp.playerId=r.playerId SET lp.leagueElo=%d" % newElo )
        self.db.commit( )

