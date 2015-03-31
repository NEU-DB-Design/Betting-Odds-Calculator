-- Validation: If this week's moneyline data is clean, no single row should have 2 positive MLs
SELECT COUNT(*) FROM Betting_Line 
	WHERE 
			((ML_1 > 0 AND ML_2 > 0) OR (ML_1 < 0 AND ML_2 < 0))
		AND 
			WEEK(NOW()) = WEEK(date_recorded);

-- Make sure we don't have any crazy values in Betting_Line data this week
SELECT STD(spread) FROM Betting_Line
	WHERE WEEK(DATE(NOW()))=WEEK(date_recorded);
SELECT MIN(spread), MAX(spread) FROM Betting_Line
	WHERE WEEK(DATE(NOW()))=WEEK(date_recorded);
    
-- Do the same with moneyline
SELECT STD(ML_1), STD(ML_2) FROM Betting_Line
	WHERE WEEK(DATE(NOW()))=WEEK(date_recorded);
SELECT MIN(ABS(ML_1)), MAX(ABS(ML_1)) FROM Betting_Line
	WHERE WEEK(DATE(NOW()))=WEEK(date_recorded);
SELECT MIN(ABS(ML_2)), MAX(ABS(ML_2)) FROM Betting_Line
	WHERE WEEK(DATE(NOW()))=WEEK(date_recorded);


-- Make sure we have the correct number of games/players
SELECT COUNT(*) FROM Team;
SELECT COUNT(*) FROM Player;
SELECT COUNT(*) FROM Game; 	