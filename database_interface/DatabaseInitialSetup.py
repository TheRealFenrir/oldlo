#!/usr/bin/python

import MySQLdb

# open database connection
db = MySQLdb.connect( "localhost", "root", "lwgmysql" )

c = db.cursor( )
c.execute( """CREATE DATABASE IF NOT EXISTS elo""" )
c.execute( """GRANT ALL ON elo.* TO 'elo'@'localhost' IDENTIFIED BY 'lwgelomysql'""" )
c.execute( """USE elo""" )

c.execute( """CREATE TABLE `Players` (
    `playerId` int NOT NULL AUTO_INCREMENT,
    `playerName` varchar(40) NOT NULL,
    PRIMARY KEY (`playerId`)
);""" )

c.execute( """CREATE TABLE `Games` (
    `gameId` int NOT NULL AUTO_INCREMENT,
    `player1Id` int NOT NULL,
    `player2Id` int NOT NULL,
    `player3Id` int NOT NULL,
    `player4Id` int NOT NULL,
    `scoreDifference` int NOT NULL,
    `date` DATETIME NOT NULL,
    `leagueId` int NOT NULL,
    PRIMARY KEY (`gameId`)
);""" )

c.execute( """CREATE TABLE `PlayerGames` (
    `playerId` int NOT NULL,
    `gameId` int NOT NULL,
    `elo` int NOT NULL
);""" )

c.execute( """CREATE TABLE `Leagues` (
    `leagueName` varchar(40) NOT NULL,
    `leagueId` int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`leagueId`)
);""" )

c.execute( """CREATE TABLE `LeaguePlayer` (
    `playerId` int NOT NULL,
    `leagueId` int NOT NULL,
    `leagueElo` int NOT NULL
);""" )

c.execute( """ALTER TABLE `Games` ADD CONSTRAINT `Games_fk0` FOREIGN KEY (`player1Id`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `Games` ADD CONSTRAINT `Games_fk1` FOREIGN KEY (`player2Id`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `Games` ADD CONSTRAINT `Games_fk2` FOREIGN KEY (`player3Id`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `Games` ADD CONSTRAINT `Games_fk3` FOREIGN KEY (`player4Id`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `Games` ADD CONSTRAINT `Games_fk4` FOREIGN KEY (`leagueId`) REFERENCES `Leagues`(`leagueId`);""" )

c.execute( """ALTER TABLE `PlayerGames` ADD CONSTRAINT `PlayerGames_fk0` FOREIGN KEY (`playerId`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `PlayerGames` ADD CONSTRAINT `PlayerGames_fk1` FOREIGN KEY (`gameId`) REFERENCES `Games`(`gameId`);""" )

c.execute( """ALTER TABLE `LeaguePlayer` ADD CONSTRAINT `LeaguePlayer_fk0` FOREIGN KEY (`playerId`) REFERENCES `Players`(`playerId`);""" )

c.execute( """ALTER TABLE `LeaguePlayer` ADD CONSTRAINT `LeaguePlayer_fk1` FOREIGN KEY (`leagueId`) REFERENCES `Leagues`(`leagueId`);""" )


