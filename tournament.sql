-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop view standings;
drop view totals;
drop view wins;

drop table matches;

create table matches(
	id serial,
	winner int,
	loser int,
	draw1 int,
	draw2 int,
	primary key (id)
);

drop table players;

create table players(
        id serial,
	name text,
	wins int,
	matches int,
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