BEGIN
  DECLARE total BIGINT DEFAULT 0;
  FOR t AS SELECT table_name FROM main.information_schema.tables WHERE table_schema = 'bronze' DO
    EXECUTE IMMEDIATE 'OPTIMIZE main.bronze.' || t.table_name;
    SET total = total + 1;
  END FOR;
  IF total = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No bronze tables found';
  END IF;
  SELECT total AS optimized_tables;
END;
