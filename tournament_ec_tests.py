from tournament import *
from random import shuffle, randint

def setUp():
	""" basic setup for some tests"""
	deleteMatches()
	deletePlayers()
	registerPlayer("Mr. Incredible")
	registerPlayer("Superman")
	registerPlayer("The Flash")
	registerPlayer("Batman")

def testExtraCredit():
	""" tests various conditions"""
	testDraw()
	testNoRematch()
	testSwissGamesPlayed(6,False,True)
	testSwissGamesPlayed(4,False,True)
	testSwissGamesPlayed(2,False,True)
	testSwissGamesPlayed(3,False,True)
	testSwissGamesPlayed(5,False,True)
	testSwissGamesPlayed(7,False,True)

def testSwissGamesPlayed(number=5, drawsAllowed=False, rematchesAllowed=True):
	"""tests by running through games for a number of players"""
	deleteMatches()
	deletePlayers()
	players = number
	for n in range(1, players+1):
		registerPlayer("Player "+str(n))

	# does this until no more pairs left
	simulateSwissGame(number, drawsAllowed, rematchesAllowed)

	# counts matches
	m = countMatches()

	# only test if rematches are allowed
	if rematchesAllowed:
		i = int(players%2 == 0);
		expected_games = ( players * (players+i) ) / 2
		print "11.%s tested that swiss game produces correct # of matches (%s) with %s players" % (players, expected_games, players)		
		assert m==expected_games, "Full number of matches are not being played, got " + str(m) + " but expected: " + str(expected_games)
	else:
		print "Games played: "+str(m)


def testNoRematch():
	"""tests that a rematch does not happen between 2 players"""
	setUp()
	standings = playerStandings()
	[id1, id2, id3, id4] = [row[0] for row in standings]
	reportMatch(id1, id2)
	reportMatch(id3, id4)
	pairings = swissPairings()

	old_pairings = pairings
	# conduct matches among pairs
	for (pid1, pname1, pid2, pname2) in pairings:
		reportMatch(pid1,pid2)

	# register 2 players
	registerPlayer("Captain Falcon")
	registerPlayer("Queen Zelda")

	new_pairings = swissPairings()
	print "10. No rematch allowed between swiss pairs"
	assert len(new_pairings), "Nothing in the new pairs"

	# Check that each new swiss pair is not in the old pairing
	for pair in new_pairings:
		assert pair not in old_pairings, "\nCurrent pair: \n  " + str(pair) + "\nIn old pairings: \n  "+str(old_pairings)

def simulateSwissGame(n=20, drawsAllowed=False, rematchesAllowed=True):
	"""
	Simulates a swiss tournament for n rounds or less
	- user can choose to allow draws or not allow rematches
	- each round a swis pairing is chosen and random winners or draws are chosen and reported
	then a new pair is chosen
	"""
	pairings = swissPairings(rematchesAllowed)
	count = 0
	tie = 0

	while len(pairings):
		for (id1, n1, id2, n2) in pairings:
			pair = [id1,id2]
			# randomly shuffle winners and losers
			shuffle(pair)
			# randomly decide if there is a tie
			if drawsAllowed:
				tie = randint(0,1)
			reportMatch(pair[0],pair[1], tie)
		pairings = swissPairings(rematchesAllowed)
		count+=1
		# failsafe
		if count>n:
			break


def testDraw():
	""" tests that a draw or tie is possible and does not produce a win for the players invovled"""
	setUp()
	standings = playerStandings()
	[id1, id2, id3, id4] = [row[0] for row in standings]
	reportMatch(id1, id2, 1)
	reportMatch(id3, id4, 0)

	standings = playerStandings()
	[win1, win2, win3, win4] = [row[2] for row in standings]
	print "9. Draws should produce no win for each player"
	assert len(standings), "No standings"
	assert win2+win3+win4 == 0, "Draw did not result in loss for players 2,3,4 "+str(win1+win2+win3)
	assert win1 == 1, "Player 1 still winning, but no draw"

if __name__ == '__main__':
	testExtraCredit()