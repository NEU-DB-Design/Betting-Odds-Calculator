DELIMITER 
CREATE PROCEDURE getYesterdaysGames()
BEGIN
	SET @today = DATE_SUB(NOW(), INTERVAL 4 HOUR); -- Switch to UTC.
    SET @yesterday = DATE(DATE_SUB(@today, INTERVAL 1 DAY)); -- Now subtract one day
    
	SELECT result_id, team1_id, ID
    FROM Game
		WHERE DATE(date) = @yesterday
        AND NOT EXISTS(SELECT 1 FROM Result WHERE Game.ID=Result.game_id);
END;	