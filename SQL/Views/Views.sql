CREATE OR REPLACE VIEW hunt_UseCase1 AS
	SELECT g.id, bl.date_recorded, t1.Nickname AS 'T1 Name', t2.Nickname AS 'T2 Name', bl.spread, bl.ML_1, bl.ML_2 FROM Betting_Line AS bl
	JOIN Game as g ON g.ID=bl.game_id
    JOIN Team as t1 ON t1.ID=g.team1_id
	JOIN Team as t2 ON t2.ID=g.team2_id
    WHERE WEEK(bl.date_recorded) = WEEK(DATE(NOW()));
    
CREATE OR REPLACE VIEW hunt_UseCase2 AS
	SELECT g.id, g.date, t1.Nickname AS 'T1 Name', t2.Nickname AS 'T2 Name' FROM Game AS g
		JOIN Team as t1 ON t1.ID=g.team1_id
		JOIN Team as t2 ON t2.ID=g.team2_id
		WHERE WEEK(DATE(NOW()))=WEEK(g.date);
        
CREATE OR REPLACE VIEW hunt_UseCase3 AS
	SELECT g.id, t1.Nickname AS 'T1 Name', t2.Nickname AS 'T2 Name', r.score_1, r.score_2, ABS(r.score_1 - r.score_2), bl.spread FROM Game as g
	JOIN Result as r ON r.game_id=g.ID
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE bl.spread < ABS(GREATEST(r.score_1, r.score_2) - LEAST(r.score_1, r.score_2));

CREATE OR REPLACE VIEW hunt_UseCase4 AS
	SELECT g.id, t1.Nickname AS 'T1 Name', t2.Nickname AS 'T2 Name', bl.spread FROM Game as g
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE WEEK(g.date) = WEEK(NOW())
		ORDER BY bl.spread
        LIMIT 5;

CREATE OR REPLACE VIEW hunt_UseCase5 AS
SELECT g.id, t1.Nickname AS 'T1 Name', t2.Nickname AS 'T2 Name', bl.spread FROM Game as g
    JOIN Team as t1 ON t1.ID=g.team1_id
    JOIN Team as t2 ON t2.ID=g.team2_id
	JOIN Betting_Line as bl ON bl.game_id=g.ID
		WHERE WEEK(g.date) = WEEK(NOW())
		ORDER BY bl.spread DESC
        LIMIT 5;

CREATE OR REPLACE VIEW hunt_UseCase7 AS
	SELECT Team.Nickname, Player.Name, MAX(Points/Games) FROM Stats
	JOIN Player ON Player.CBS_PlayerID = Stats.CBS_PlayerID
    JOIN Team ON Player.CBS_TeamID = Team.CBS_TeamID
    GROUP BY Team.CBS_TeamID;

CREATE OR REPLACE VIEW hunt_UseCase8 AS
	SELECT Team.Nickname, Player.Name, MIN(Points/Games) FROM Stats
	JOIN Player ON Player.CBS_PlayerID = Stats.CBS_PlayerID
    JOIN Team ON Player.CBS_TeamID = Team.CBS_TeamID
    GROUP BY Team.CBS_TeamID;
