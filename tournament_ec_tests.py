from tournament import *
from random import shuffle, randint

def setUp():
	deleteMatches()
	deletePlayers()
	registerPlayer("Mr. Incredible")
	registerPlayer("Superman")
	registerPlayer("The Flash")
	registerPlayer("Batman")

def testExtraCredit():
	setUp()
	testDraw()
	testNoRematch()
	testSwissGamesPlayed(2)
	testSwissGamesPlayed(5)
	testSwissGamesPlayed(6)
	testSwissGamesPlayed(11)
	testSwissGamesPlayed(8,True)
	testSwissGamesPlayed(7,True)


def testSwissGamesPlayed(number=5, drawsAllowed=False):
	"""tests by running through games for a number of players"""
	deleteMatches()
	deletePlayers()
	players = number
	for n in range(1, players+1):
		registerPlayer("Player "+str(n))

	# does this until no more pairs left
	simulateSwissGame(100, drawsAllowed)

	# counts matches
	m = countMatches()

	print "11.%s tested swiss game with %s players" % (players, players)

	expected_games = ( players * (players-1) ) / 2
	
	# players where players-1 is number of player each one plays and / 2 because a,b only not b,a		
	assert "Full number of matches are not being played, got " + str(m) + " but expected: " + str(expected_games)
	if drawsAllowed:
		print "\t ties allowed Expected: " + str(m) + "got: "+ str(expected_games)

def testNoRematch():
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

	registerPlayer("Captain Falcon")
	registerPlayer("Queen Zelda")

	new_pairings = swissPairings()
	print "10. No rematch allowed between swiss pairs"
	assert len(new_pairings), "Nothing in the new pairs"

	for pair in new_pairings:
		assert pair not in old_pairings, "\nCurrent pair: \n  " + str(pair) + "\nIn old pairings: \n  "+str(old_pairings)

def simulateSwissGame(n=1000, drawsAllowed=False):
	pairings = swissPairings()
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
		pairings = swissPairings()
		count+=1
		# failsafe
		if count>n:
			break


def testDraw():
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