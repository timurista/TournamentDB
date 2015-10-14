# Tournament DB Interface API in Python
## How to Run

### Initialization
First you must install vagrant or another virtual system to run Postgres or psql.
After you have a virtual machine up and running, log into the tournament director and create a "tournament" database. This can be done by logging into psql (type the command "psql") and typing "CREATE DATABASE tournament." You can then use "\c tournament" to connect to the database. You must then import "tournament.sql" by typing the command "\i tournament.sql" which will create the necessary views and tables.
### Running the tests
After you have imported the required views and tables, exit psql and run "python tournament_test.py" to confirm all tests pass and finally "python tournament_ec_tests.py" to confirm no rematches occur and that draws can be allowed.

## What this code does
Tournament.py provides an api for deleting, registering, pairing and displaying the results of a tournament match. You can use this code as an interface to retrieve results from a database and implement them into a web application.

### Tournament commands
	1. deleteMatches() deletes all current matches
	2. deletePlayers() delete all current players in the tournament
	3. registerPlayer(name) Adds a player to the tournament database using unique serial id.
	4. playerStandings() Returns a list of the players and their win records, sorted by wins.
	5. reportMatch(winner, loser, draw=0) Records the outcome of a single match between two players. Defaults to no draw, but if draw is set to 1, then winner/loser become draw1/draw2 in matches table.
	6. swissPairings() Returns a list of pairs of players for the next round of a match. No rematches are allowed.

