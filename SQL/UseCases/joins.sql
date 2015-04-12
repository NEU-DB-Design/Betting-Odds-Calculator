-- Find all games for this week and there corresponding betting lines
SELECT g.id, bl.date_recorded, t1.name, t2.name, bl.spread, bl.ML_1, bl.ML_2 FROM Betting_Line AS bl
	JOIN Game as g ON g.ID=bl.game_id
    JOIN Team as t1 ON t1.ID=g.team1_id
	JOIN Team as t2 ON t2.ID=g.team2_id
    WHERE WEEK(bl.date_recorded) = WEEK(DATE(NOW()));

-- Find all games for this week
SELECT g.id, g.date, t1.Nickname, t2.Nickname FROM Game AS g
    JOIN Team as t1 ON t1.ID=g.team1_id
	JOIN Team as t2 ON t2.ID=g.team2_id
    WHERE WEEK(DATE(NOW()))=WEEK(g.date);
    
-- Find all games where underdog betters won
SELECT g.id, t1.Nickname, t2.Nickname, r.score_1, r.score_2, ABS(r.score_1 - r.score_2), bl.spread FROM Game as g
	JOIN Result as r ON r.game_id=g.ID
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE bl.spread < ABS(GREATEST(r.score_1, r.score_2) - LEAST(r.score_1, r.score_2));
        
-- Find 5 highest spreads this week
SELECT g.id, t1.Nickname, t2.Nickname, bl.spread FROM Game as g
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE WEEK(g.date) = WEEK(NOW())
		ORDER BY bl.spread
        LIMIT 5;
        
-- Find 5 lowest spreads this week
SELECT g.id, t1.Nickname, t2.Nickname, bl.spread FROM Game as g
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE WEEK(g.date) = WEEK(NOW())
		ORDER BY bl.spread DESC
        LIMIT 5;

-- Find player with highest points per game on each team  
SELECT Team.Nickname, Player.Name, MAX(Points/Games) FROM Stats
	JOIN Player ON Player.CBS_PlayerID = Stats.CBS_PlayerID
    JOIN Team ON Player.CBS_TeamID = Team.CBS_TeamID
    GROUP BY Team.CBS_TeamID;
    
-- Find player with lowest points per game on each team  
SELECT Team.Nickname, Player.Name, MIN(Points/Games) FROM Stats
	JOIN Player ON Player.CBS_PlayerID = Stats.CBS_PlayerID
    JOIN Team ON Player.CBS_TeamID = Team.CBS_TeamID
    GROUP BY Team.CBS_TeamID;
    
-- Find player with highest Points Per Game
SELECT Name, MAX(PPG) FROM Stats
	JOIN Player ON Player.playerID = Stats.playerID;

-- Find highest underdog moneyline payoff
SELECT MAX(GREATEST(ML_1, ML_2)) FROM Betting_Line;

-- Find highest favorite moneyline payoff
SELECT MIN(LEAST(ML_1, ML_2)) FROM Betting_Line;