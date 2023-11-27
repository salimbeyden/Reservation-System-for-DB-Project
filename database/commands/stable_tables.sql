--SPORT TABLE
INSERT INTO sport (sport_id, sport_type, is_competitive, capacity_min, capacity_max)
VALUES 
(1,'Futbol', True, 5, 11), 
(2,'Voleybol', True, 2, 6), 
(3,'Basketbol', True, 1, 5),
(4,'Tenis', True, 1, 2),
(5,'Yüzme', False, 1, 1),
(6,'Gym', False, 1, 1),
(7,'Ping-Pong', True, 2, 2);



--CAMPUS TABLE
INSERT INTO campus (campus_id, name, address, image_id)
VALUES
(1, 'Ayazağa', 'Maslak-İSTANBUL', 1),
(2, 'Taşkişla', 'Taksim-İSTANBUL', 2),
(3, 'Gümüşsuyu', 'Gümüşsuyu-İSTANBUL', 3),
(4, 'Maçka', 'Maçka-İSTANBUL', 4),
(5, 'Tuzla', 'Tuzla-İSTANBUL', 5),
(6, 'İTÜ KKTC', 'Gazimağusa - KKTC', 6);



--FACILITIES TABLE
INSERT INTO facilities (facility_id, name, campus_id, tel_no, email, address)
VALUES
(1, 'Açik Spor Alanlari', 1, '-', '-', 'Maslak/İSTANBUL'),
(2, 'Merkez Spor Salonu', 1, '-', '-', 'Maslak/İSTANBUL'),
(3, 'Gümüşsuyu Spor Salonu', 3, '-', '-', 'Gümüşsuyu'),
(4, 'Vadi Yurtlari Spor Salonu', 1, '-', '-', 'Maslak/İSTANBUL'),
(5, 'Olimpik Yüzme Havuzu', 1, '+90 (212) 285 71 18', '-', 'Maslak/İSTANBUL'),
(6, 'İTÜ Stadyumu', 1, '-', '-', 'Ayazağa'),
(7, 'Gümüşsuyu Hali Saha', 3, '+90 (212) 285 39 51', '-', 'Gümüşsuyu'),
(8, 'Ayazağa Hali Saha', 1, '-', '-', 'Maslak/İSTANBUL'),
(9, 'Sağlikli Yaşam Merkezi', 1, '-', '-', 'Maslak/İSTANBUL'),
(10, 'Tenis Kortlari', 1, '-', '-', 'Maslak/İSTANBUL');



--FACILITY FOR SPORT TABLE
INSERT INTO facility_for_sport (fac_per_spor_id, facility_id, sport_id, capacity, current)
VALUES
--Açık Spor Alanları
(1, 1, 3, 20, 14),
(2, 1, 2, 12, 4),
(3, 1, 1, 22, 16),
(4, 1, 4, 2, 1),
--Merkez Spor Salonu
(5, 2, 3, 20, 14),
(6, 2, 2, 12, 4),
(7, 2, 1, 22, 16),
(8, 2, 7, 8, 4),
--Gümüşsuyu Spor Salonu
(9, 3, 3, 20, 14),
(10, 3, 2, 12, 4),
(11, 3, 1, 22, 16),
--Vadi Yurtları Spor Salonu
(12, 4, 3, 20, 14),
(13, 4, 2, 12, 4),
(14, 4, 1, 22, 16),
--Olimpik Yüzme Havuzu
(15, 5, 5, 20, 7),
--İTÜ Stadyumu
(16, 6, 1, 44, 22),
--Gümüşsuyu Halı Saha
(17, 7, 1, 22, 11),
--Ayazağa Halı Saha
(18, 8, 1, 22, 11),
--Sağlıklı Yaşam Merkezi
(19, 9, 6, 50, 27),
--Tenis Kortları
(20, 10, 4, 8, 6);




