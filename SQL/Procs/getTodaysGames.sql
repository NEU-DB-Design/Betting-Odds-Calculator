DELIMITER 
CREATE PROCEDURE getTodaysGames()
BEGIN
	SET @today = DATE_SUB(NOW(), INTERVAL 4 HOUR); -- Switch to UTC.
   
	SELECT Game.result_id
    FROM Game
    Join Betting_Line as BL ON BL.game_id
    WHERE DATE(date) = DATE(@today)
        AND NOT EXISTS(SELECT 1 FROM Result WHERE Game.ID=Result.game_id);
END;

