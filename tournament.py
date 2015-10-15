#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players;")
    count = c.fetchone()[0]
    db.close()
    return count

def countMatches():
    """Returns number of games played during the tournament"""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM matches;")
    count = c.fetchone()[0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,) )
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # view standings is setup on initialization / import of tournament.sql
    c.execute("SELECT * FROM standings;")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser, draw=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()

    # ties are logged seperately from wins and losses so that extra matches aren't logged
    if draw:
        c.execute("INSERT INTO matches (draw1, draw2) VALUES (%s, %s);", (winner, loser) )
    else:
        c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);", (winner, loser) )
    db.commit()
    db.close()    
 
 
def swissPairings(rematchesAllowed=True):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    # get all matches (even draws) which have been played
    c.execute("SELECT * FROM allMatchPairings;")
    allMatches = c.fetchall()
 
    if rematchesAllowed:
        allMatches = []

    c.execute("""
        SELECT ranked1.PlayerId player1, ranked1.name, 
            ranked2.PlayerId player2, ranked2.name
        FROM player_rankings AS 
            ranked1
        INNER JOIN player_rankings 
            AS ranked2 
            -- checks that evens are selected
            ON ranked1.PlayerRank + 1 = ranked2.PlayerRank
        -- makes sure only odds are selected
        WHERE ranked1.playerrank % 2 = 1;
            """)
    pairs = c.fetchall()
    db.close()

    # Make sure no matches in pairs
    pairs = [p for p in pairs if (p[0],p[2]) not in allMatches and (p[2],p[0]) not in allMatches]
    return pairs   
