DELIMITER 
CREATE PROCEDURE addResult(IN s1 INT, IN s2 INT, IN w_id BOOLEAN, IN g_id INT)
	BEGIN
		INSERT INTO `bets`.`Result`
			(`score_1`, `score_2`, `winner`, `game_id`)
		VALUES
			(s1, s2, w_id, g_id);
END;

