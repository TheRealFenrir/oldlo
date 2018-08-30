#!/usr/bin/env python

def calculateNewElos( k, spread, scores, elos ):
    """Calculate new Elo scores based on a game result
    :param k: The 'k' parameter for this Elo system
    :param spread: The 'spread' parameter for this Elo system
    :param scores: The scores in this game. Should be normalized such that the sum of this list is 1, otherwise the scores will be normalized automatically.
    :param elos: A list elos of the players in this game
    :return: The changes to each players elos"""
    eloSum = sum( elos )
    scoreSum = sum( scores )
    normalizedScores = [ x / float( scoreSum ) for x in scores ]
    expectedScores = [ 1.0 / ( 1.0 + 10.0 ** ( ( eloSum - x - x ) / float( spread ) ) ) for x in elos ]
    eloChanges = [ k * ( normalized - expected ) for normalized, expected in zip( normalizedScores, expectedScores ) ]
    #print expectedScores
    #print normalizedScores
    #print eloChanges
    return eloChanges

def calculateExpectedScore( spread, elos, scale, rounded ):
    """Calculate the expected score of a game given a list of elos of the competitors.
       The scores will be scaled to give the winner a certain value.
    :param elos: List of a elos of the competitors
    :param scale: The amount of points the winner should have
    :param rounded: Whether the results should be rounded or left as floating points
    :return: The expected scores of each competitor"""
    eloSum = sum( elos )
    expectedScores = [ 1.0 / ( 1.0 + 10.0 ** ( ( eloSum - x - x ) / float( spread ) ) ) for x in elos ]
    multiplier = scale / max( expectedScores )
    if rounded:
        return [ int( round( multiplier * x ) )  for x in expectedScores ]
    else:
        return [  multiplier * x for x in expectedScores ]

if __name__ == '__main__':
	print calculateNewElos( 80, 400, [ 5, 2 ], [ 1400, 1500 ] )
	print calculateExpectedScore( 400, [ 1400, 1500 ], 5, False )
	print calculateExpectedScore( 400, [ 1400, 1500 ], 5, True )
