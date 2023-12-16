INSERT INTO sport (sport_id, sport_type, is_competitive, capacity_min, capacity_max, is_ind)
VALUES 
(1,'Football', True, 5, 11, 0), 
(2,'Volleyball', True, 2, 6, 0), 
(3,'Basketball', True, 3, 5, 0),
(4,'Tennis Individuals', True, 1, 1, 1),
(5,'Tennis Teams', True, 2, 2, 0),
(6,'Swimming', False, 1, 1, 1),
(7,'Gym', False, 1, 1, 1),
(8,'PingPong Individuals', True, 1, 1, 1),
(9,'PingPong Teams', True, 2, 2, 0);



INSERT INTO campus (campus_id, name, address, image_id)
VALUES
(1, 'Ayazaga', 'Maslak-ISTANBUL', 1),
(2, 'Taskisla', 'Taksim-ISTANBUL', 2),
(3, 'Gumussuyu', 'Gumussuyu-ISTANBUL', 3),
(4, 'Macka', 'Macka-ISTANBUL', 4),
(5, 'Tuzla', 'Tuzla-ISTANBUL', 5),
(6, 'ITU KKTC', 'Gazimagusa - KKTC', 6);



INSERT INTO facility (facility_id, name, campus_id, tel_no, email, address)
VALUES
(1, 'Acik Spor Alanlari'        , 1, '+90 (212) 122 12 17', 'ayazagaacik@itu.edu.tr', 'Maslak/ISTANBUL'),
(2, 'Merkez Spor Salonu'        , 2, '+90 (212) 154 56 22', 'taskislamerkez@itu.edu.tr', 'Taskisla'),
(3, 'Gumussuyu Spor Salonu'     , 3, '+90 (212) 186 71 55', 'gumussuyuspor@itu.edu.tr', 'Gumussuyu'),
(4, 'Vadi Yurtlari Spor Salonu' , 1, '+90 (212) 501 13 54', 'vadispor@itu.edu.tr', 'Maslak/ISTANBUL'),
(5, 'Olimpik Yuzme Havuzu'      , 1, '+90 (212) 622 87 23', 'ayazagaolimpik@itu.edu.tr', 'Maslak/ISTANBUL'),
(6, 'ITU Stadyumu'              , 1, '+90 (212) 743 65 57', 'ayazagastadium@itu.edu.tr', 'Ayazaga'),
(7, 'Gumussuyu Hali Saha'       , 3, '+90 (212) 951 49 57', 'gumussuyuhalisaha@itu.edu.tr', 'Gumussuyu'),
(8, 'Ayazaga Hali Saha'         , 1, '+90 (212) 224 57 35', 'ayazagahalisaha@itu.edu.tr', 'Maslak/ISTANBUL'),
(9, 'Saglikli Yasam Merkezi'    , 4, '+90 (212) 366 19 64', 'mackasaglikliyasam@itu.edu.tr', 'Besiktas/ISTANBUL'),
(10, 'Tenis Kortlari'           , 5, '+90 (212) 475 27 49', 'tuzlatenis@itu.edu.tr', 'Tuzla/ISTANBUL'),
(11, 'Olimpik Yuzme Havuzu'     , 6, '+90 (212) 522 26 54', 'kktcolimpik@itu.edu.tr', 'KKTC');


INSERT INTO facility_for_sport (fac_per_spor_id, facility_id, sport_id, capacity, current)
VALUES
(1, 1, 3, 20, 0),
(2, 1, 2, 12, 0),
(3, 1, 1, 22, 0),
(4, 1, 4, 2, 0),
(5, 1, 5, 2, 0),
(6, 2, 3, 20, 0),
(7, 2, 2, 12, 0),
(8, 2, 1, 22, 0),
(9, 2, 8, 8, 0),
(10, 2, 9, 8, 0),
(11, 3, 3, 20, 0),
(12, 3, 2, 12, 0),
(13, 3, 1, 22, 0),
(14, 4, 3, 20, 0),
(15, 4, 2, 12, 0),
(16, 4, 1, 22, 0),
(17, 5, 6, 20, 0),
(18, 6, 1, 44, 0),
(19, 7, 1, 22, 0),
(20, 8, 1, 22, 0),
(21, 9, 7, 50, 0),
(22, 10, 4, 8, 0),
(23, 10, 5, 8, 0),
(24, 11, 6, 20, 0);




