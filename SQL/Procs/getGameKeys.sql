DELIMITER 
CREATE PROCEDURE GetGameKeys()
BEGIN
	SET @today = DATE_SUB(NOW(), INTERVAL 4 HOUR);
	SELECT id, team1_id, team2_id, DATE(date)
    FROM Game
		WHERE DATE(date) = DATE(@today) OR DATE(date) = DATE_ADD(DATE(@today), INTERVAL 1 DAY);
END;