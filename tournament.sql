-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- Initialize db
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- these lines here.
drop view if exists player_rankings;
drop view if exists standings;
drop view if exists totals;
drop view if exists wins;
drop view if exists allMatchPairings;


drop table if exists matches;

create table matches(
	id serial,
	winner int DEFAULT 0,
	loser int DEFAULT 0,
	draw1 int DEFAULT 0,
	draw2 int DEFAULT 0,
	primary key (id)
);

drop table if exists players;

create table players(
        id serial,
	name text,
	primary key (id)
	
);


-- holds view of number of wins
create view wins as select
            players.id, 
            players.name,  
            count(matches.winner) as win            
                from players left join matches 
                    on players.id = matches.winner
                    group by players.id;

-- holds view for current total matches
create view totals as 
        select
            players.id,            
            count(matches.id) as total_matches 
            from players left join matches
                on players.id = matches.winner or players.id = matches.loser
                or players.id = matches.draw1 or players.id = matches.draw2
                group by players.id;


-- holds view for current standings of all players
create view standings as 
          select * from wins left join totals
          using (id)
            group by wins.id, wins.name, 
              wins.win, totals.total_matches
            order by wins.win desc;

-- holds rank of player
CREATE VIEW player_rankings AS
	SELECT id AS PlayerId, name, row_number() 
	OVER (order by win) as PlayerRank
	FROM standings;


-- holds matches
CREATE VIEW allMatchPairings AS
	SELECT winner, loser from matches
	UNION
	SELECT draw1, draw2 from matches;
