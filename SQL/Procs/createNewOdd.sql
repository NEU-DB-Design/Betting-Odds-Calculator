DELIMITER 
CREATE PROCEDURE createNewOdd(IN game_id INT, IN mL1 FLOAT, IN mL2 FLOAT, IN spread FLOAT)
	BEGIN
		INSERT INTO `bets`.`Betting_Line`
			(`game_id`,
			`spread`,
			`ML_2`,
			`ML_1`,
            date_recorded
            )
		VALUES
			(
			game_id,
            spread,
			mL1,
			mL2,
            DATE_SUB(NOW(), INTERVAL 4 HOUR)
			);
END;