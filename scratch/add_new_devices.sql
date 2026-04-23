-- Insert new PLC addresses for OK/NG Result
INSERT INTO `plc_oee_seat_result_detail` (`device`, `value`, `station_id`, `comment`) 
VALUES 
('D968', 'OK', 1, 'OK / NG RESULT ->GOT- QC1 (Total)'),
('D970', 'OK', 2, 'OK / NG RESULT ->GOT- QC2 (Total)'),
('D972', 'OK', 3, 'OK / NG RESULT ->GOT- QC3 (Total)')
ON DUPLICATE KEY UPDATE 
    `value` = VALUES(`value`), 
    `station_id` = VALUES(`station_id`), 
    `comment` = VALUES(`comment`);
