PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(128), 
	is_admin BOOLEAN, 
	registered_at DATETIME, 
	last_login DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO user VALUES(1,'admin','scrypt:32768:8:1$xGL6Ixq9G8SaVdKb$84148ff2198d2bea77755082d6a98842a7292e5fc5a9162f7f3cddfcb37d6b2f4cd88fc30ad01ed4580ef5c93d00393b06800d4c4c2db07e5b98422940561bf4',1,'2024-11-19 09:20:57.255147','2024-12-01 06:51:47.420493');
INSERT INTO user VALUES(3,'hubers','scrypt:32768:8:1$cjBRxuX1vTOgMwWe$3a6b7a42a49a42e5b19770ef371655871d0ff35397aa57eda2bde094226cc5a313fb6d77960a9abdbd99bc9a7c48941abc233e5e3cbb6f3895f0a2d99800a329',0,'2024-11-19 09:27:06.771984','2024-11-30 12:22:04.767719');
CREATE TABLE category (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	icon VARCHAR(5), 
	sort_order INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO category VALUES(1,'Obst','🍎',10);
INSERT INTO category VALUES(2,'Backwaren','🥨',20);
INSERT INTO category VALUES(3,'Kühlregal','🥛',30);
INSERT INTO category VALUES(4,'Fleisch','🥩',40);
INSERT INTO category VALUES(5,'Tiefkühl','❄️',80);
INSERT INTO category VALUES(6,'Getränke','🥤',60);
INSERT INTO category VALUES(7,'Konserven','🥫',70);
INSERT INTO category VALUES(8,'Naschen ','🍫',90);
INSERT INTO category VALUES(9,'Gewürze','🧂',77);
INSERT INTO category VALUES(10,'Reinigung','🧹',100);
INSERT INTO category VALUES(11,'Drogerie','🧴',110);
INSERT INTO category VALUES(12,'Gemüse','🥬',15);
INSERT INTO category VALUES(13,'Baumarkt','🔧',120);
INSERT INTO category VALUES(14,'Kochen/Vorrat','🍵',75);
INSERT INTO category VALUES(15,'Garten','🌴',130);
INSERT INTO category VALUES(17,'Backen','🍪',79);
INSERT INTO category VALUES(18,'Apotheke','💊',140);
CREATE TABLE article (
	id INTEGER NOT NULL, 
	"artName" VARCHAR(50) NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES category (id)
);
INSERT INTO article VALUES(1,'Apfel',1);
INSERT INTO article VALUES(2,'Kornspitz',2);
INSERT INTO article VALUES(3,'Pfeffer ',9);
INSERT INTO article VALUES(4,'Mon Cherie',8);
INSERT INTO article VALUES(5,'Tomaten gewürfelt ',7);
INSERT INTO article VALUES(6,'Artikel',13);
INSERT INTO article VALUES(8,'Whiskey',6);
INSERT INTO article VALUES(9,'Rotwein',6);
INSERT INTO article VALUES(10,'Nudeln',14);
INSERT INTO article VALUES(11,'Poolpflege',13);
INSERT INTO article VALUES(12,'Bananen ',1);
INSERT INTO article VALUES(14,'Persil',10);
INSERT INTO article VALUES(15,'Karfiol',12);
INSERT INTO article VALUES(16,'Brokkoli',12);
INSERT INTO article VALUES(17,'Karotten',12);
INSERT INTO article VALUES(18,'Paprika',12);
INSERT INTO article VALUES(19,'Zucchini ',12);
INSERT INTO article VALUES(20,'Chinakohl',12);
INSERT INTO article VALUES(21,'Salat',12);
INSERT INTO article VALUES(22,'Weintrauben ',1);
INSERT INTO article VALUES(23,'Orangen ',1);
INSERT INTO article VALUES(24,'Mandarinen ',1);
INSERT INTO article VALUES(25,'Heidelbeeren ',1);
INSERT INTO article VALUES(26,'Toastbrot ',2);
INSERT INTO article VALUES(27,'Brot',2);
INSERT INTO article VALUES(28,'Semmeln ',2);
INSERT INTO article VALUES(29,'Butter',3);
INSERT INTO article VALUES(30,'Lätta',3);
INSERT INTO article VALUES(31,'Joghurt ',3);
INSERT INTO article VALUES(32,'Zitronen ',1);
INSERT INTO article VALUES(33,'Mozzarella ',3);
INSERT INTO article VALUES(34,'Parmesan ',3);
INSERT INTO article VALUES(35,'Käse ',3);
INSERT INTO article VALUES(36,'Cottage Cheese',3);
INSERT INTO article VALUES(37,'Topfen',3);
INSERT INTO article VALUES(38,'Zahnpaste',11);
INSERT INTO article VALUES(39,'Duschgel',11);
INSERT INTO article VALUES(40,'Shampoo ',11);
INSERT INTO article VALUES(41,'Sauerrahm ',3);
INSERT INTO article VALUES(43,'Hühnerfleisch ',4);
INSERT INTO article VALUES(44,'Rindfleisch ',4);
INSERT INTO article VALUES(45,'Faschiertes',4);
INSERT INTO article VALUES(46,'Schinken',4);
INSERT INTO article VALUES(47,'Geräuchertes',4);
INSERT INTO article VALUES(48,'Sekt',6);
INSERT INTO article VALUES(50,'Weißwein ',6);
INSERT INTO article VALUES(51,'Becherovka',6);
INSERT INTO article VALUES(52,'Bayleys',6);
INSERT INTO article VALUES(53,'Mineralwasser ',6);
INSERT INTO article VALUES(54,'Reis',14);
INSERT INTO article VALUES(55,'Vollkornkekse',8);
INSERT INTO article VALUES(56,'Soletti',8);
INSERT INTO article VALUES(57,'Erdnüsse',8);
INSERT INTO article VALUES(58,'Erdbeeren',1);
INSERT INTO article VALUES(59,'Birnen',1);
INSERT INTO article VALUES(60,'Kiwi',1);
INSERT INTO article VALUES(61,'Melone',1);
INSERT INTO article VALUES(62,'Champignon',12);
INSERT INTO article VALUES(63,'Gurke',12);
INSERT INTO article VALUES(64,'Kartoffel',12);
INSERT INTO article VALUES(65,'Kohlrabi',12);
INSERT INTO article VALUES(66,'Weckerl',2);
INSERT INTO article VALUES(67,'Knäckebrot ',2);
INSERT INTO article VALUES(68,'Eier',3);
INSERT INTO article VALUES(69,'Tee',6);
INSERT INTO article VALUES(70,'Saft',6);
INSERT INTO article VALUES(71,'Zwiebel ',12);
INSERT INTO article VALUES(72,'Schweinskarree',4);
INSERT INTO article VALUES(73,'Speck',4);
INSERT INTO article VALUES(74,'Würstel',4);
INSERT INTO article VALUES(75,'Knackwurst ',4);
INSERT INTO article VALUES(76,'Wurst',4);
INSERT INTO article VALUES(77,'Fisch',5);
INSERT INTO article VALUES(78,'Beeren',5);
INSERT INTO article VALUES(79,'Gemüse',5);
INSERT INTO article VALUES(80,'Eiscreme ',5);
INSERT INTO article VALUES(81,'Weizenmehl glatt ',17);
INSERT INTO article VALUES(82,'Weizenmehl griffig',17);
INSERT INTO article VALUES(83,'Salz',9);
INSERT INTO article VALUES(84,'Meersalz',9);
INSERT INTO article VALUES(85,'Paprikapulver',9);
INSERT INTO article VALUES(86,'Oregano ',9);
INSERT INTO article VALUES(87,'Cif',10);
INSERT INTO article VALUES(88,'Geschirrspülmittel',10);
INSERT INTO article VALUES(89,'Kürbis',12);
INSERT INTO article VALUES(90,'Oliven',7);
INSERT INTO article VALUES(91,'Kräuter',9);
INSERT INTO article VALUES(92,'Radieschen',12);
INSERT INTO article VALUES(93,'Spargel',12);
INSERT INTO article VALUES(94,'Suppengemüse',12);
INSERT INTO article VALUES(95,'Tomaten',12);
INSERT INTO article VALUES(96,'Striezel',2);
INSERT INTO article VALUES(97,'Backpapier',17);
INSERT INTO article VALUES(98,'Backpulver',17);
INSERT INTO article VALUES(99,'Baguette',2);
INSERT INTO article VALUES(100,'Blätterteig',3);
INSERT INTO article VALUES(101,'Chia-Samen',14);
INSERT INTO article VALUES(102,'Dinkel',17);
INSERT INTO article VALUES(103,'Dinkelmehl',17);
INSERT INTO article VALUES(104,'Hefe',3);
INSERT INTO article VALUES(105,'Kakao',14);
INSERT INTO article VALUES(106,'Kochschokolade',17);
INSERT INTO article VALUES(107,'Mandeln',14);
INSERT INTO article VALUES(108,'Patisserie Creme',17);
INSERT INTO article VALUES(109,'Roggen',17);
INSERT INTO article VALUES(110,'Roggenmehl',17);
INSERT INTO article VALUES(111,'Sahnesteif',17);
INSERT INTO article VALUES(112,'Schokoglasur',17);
INSERT INTO article VALUES(113,'Schokostreusel',17);
INSERT INTO article VALUES(114,'Staubzucker',14);
INSERT INTO article VALUES(115,'Kristallzucker',14);
INSERT INTO article VALUES(116,'Vanillezucker',17);
INSERT INTO article VALUES(117,'Weizen',17);
INSERT INTO article VALUES(118,'Walnüsse',17);
INSERT INTO article VALUES(119,'Aperol',6);
INSERT INTO article VALUES(120,'Bier',6);
INSERT INTO article VALUES(121,'Cola',6);
INSERT INTO article VALUES(122,'Ajax',10);
INSERT INTO article VALUES(123,'Antikalkgel',10);
INSERT INTO article VALUES(124,'Batterien',13);
INSERT INTO article VALUES(125,'Batterien',11);
INSERT INTO article VALUES(126,'Eiswürfelsäcke',11);
INSERT INTO article VALUES(127,'Entkalker',10);
INSERT INTO article VALUES(128,'Fewa',10);
INSERT INTO article VALUES(129,'Glasreiniger',10);
INSERT INTO article VALUES(130,'Haarspray',11);
INSERT INTO article VALUES(131,'Handcreme',11);
INSERT INTO article VALUES(132,'Klarspüler',10);
INSERT INTO article VALUES(133,'Küchenrolle',10);
INSERT INTO article VALUES(134,'Gesichtswasser',11);
INSERT INTO article VALUES(135,'Pads',11);
INSERT INTO article VALUES(136,'Peeling',11);
INSERT INTO article VALUES(137,'Tabs Geschirrspüler',10);
INSERT INTO article VALUES(138,'Salz Geschirrspüler',10);
INSERT INTO article VALUES(139,'Servietten',11);
INSERT INTO article VALUES(140,'Taschentücher',11);
INSERT INTO article VALUES(141,'Wattestäbchen',11);
INSERT INTO article VALUES(142,'Weichspüler',10);
INSERT INTO article VALUES(143,'Fisch',4);
INSERT INTO article VALUES(144,'Käsekrainer',4);
INSERT INTO article VALUES(145,'Pariser',4);
INSERT INTO article VALUES(146,'Schopfsteaks',4);
INSERT INTO article VALUES(148,'Barbecue Sauce',14);
INSERT INTO article VALUES(149,'Gewürze',9);
INSERT INTO article VALUES(150,'Gries',14);
INSERT INTO article VALUES(151,'Margarine',3);
INSERT INTO article VALUES(153,'Rapsöl',14);
INSERT INTO article VALUES(154,'Olivenöl',14);
INSERT INTO article VALUES(155,'Suppenwürfel',14);
INSERT INTO article VALUES(156,'Thunfisch',7);
INSERT INTO article VALUES(157,'Tomaten passiert',7);
INSERT INTO article VALUES(158,'Tomatenmark',7);
INSERT INTO article VALUES(159,'Senf',7);
INSERT INTO article VALUES(160,'Mayonnaise',7);
INSERT INTO article VALUES(161,'Becel',3);
INSERT INTO article VALUES(162,'Camembert',3);
INSERT INTO article VALUES(163,'Haloumi',3);
INSERT INTO article VALUES(164,'Milch',3);
INSERT INTO article VALUES(165,'Schlagobers',3);
INSERT INTO article VALUES(166,'Skyr',3);
INSERT INTO article VALUES(167,'Dörrpflaumen',14);
INSERT INTO article VALUES(168,'Hanfsamen',14);
INSERT INTO article VALUES(169,'Leinsamen',14);
INSERT INTO article VALUES(170,'Leinöl',14);
INSERT INTO article VALUES(171,'Müsli',14);
INSERT INTO article VALUES(172,'Rosinen',14);
INSERT INTO article VALUES(173,'Sonnenblumenkerne',14);
INSERT INTO article VALUES(174,'Chips',8);
INSERT INTO article VALUES(175,'Eiswaffeln',8);
INSERT INTO article VALUES(176,'Giotto',8);
INSERT INTO article VALUES(177,'Kekse',8);
INSERT INTO article VALUES(178,'Kokoskuppeln',8);
INSERT INTO article VALUES(179,'Lindt Schokolade',8);
INSERT INTO article VALUES(180,'Merci',8);
INSERT INTO article VALUES(181,'Schokolade',8);
INSERT INTO article VALUES(182,'Zuckerl',8);
INSERT INTO article VALUES(183,'Kräuter',5);
INSERT INTO article VALUES(184,'Fleischknödel',5);
INSERT INTO article VALUES(185,'Pizza',5);
INSERT INTO article VALUES(186,'Biskotten',17);
INSERT INTO article VALUES(187,'Cashewnüsse',8);
INSERT INTO article VALUES(188,'Nüsse',8);
INSERT INTO article VALUES(189,'Getrocknete Tomaten',7);
INSERT INTO article VALUES(190,'Haltbarmilch',7);
INSERT INTO article VALUES(191,'Knusperbrot',2);
INSERT INTO article VALUES(192,'Lasagneblätter',14);
INSERT INTO article VALUES(193,'Nutella',14);
INSERT INTO article VALUES(194,'Soda Patrone',11);
INSERT INTO article VALUES(195,'Vogelfutter',14);
INSERT INTO article VALUES(196,'1 Dummy',14);
INSERT INTO article VALUES(197,'Rasensamen',15);
INSERT INTO article VALUES(198,'Rasendünger',15);
INSERT INTO article VALUES(199,'Artikel',15);
INSERT INTO article VALUES(200,'zz_Obst',1);
INSERT INTO article VALUES(201,'zz_Gemüse',12);
INSERT INTO article VALUES(202,'zz_Gebäck',2);
INSERT INTO article VALUES(203,'zz_Gekühltes',3);
INSERT INTO article VALUES(204,'zz_Fleisch',4);
INSERT INTO article VALUES(205,'zz_Getränk',6);
INSERT INTO article VALUES(206,'zz_Konserven',7);
INSERT INTO article VALUES(207,'zz_Vorrat',14);
INSERT INTO article VALUES(208,'zz_Gewürz',9);
INSERT INTO article VALUES(209,'Opti',10);
INSERT INTO article VALUES(210,'zz_Backen',17);
INSERT INTO article VALUES(211,'zz_Gefrorenes',5);
INSERT INTO article VALUES(212,'zz_Naschen',8);
INSERT INTO article VALUES(213,'zz_Reinigung',10);
INSERT INTO article VALUES(214,'zz_Drogerie',11);
INSERT INTO article VALUES(215,'zz_Baumarkt',13);
INSERT INTO article VALUES(216,'zz_Garten',15);
INSERT INTO article VALUES(218,'Fischstäbchen',5);
INSERT INTO article VALUES(219,'Haferflocken ',14);
INSERT INTO article VALUES(220,'Küchenschwamm',11);
INSERT INTO article VALUES(221,'Klopapier ',11);
INSERT INTO article VALUES(222,'Essiggurken',7);
INSERT INTO article VALUES(223,'Preiselbeeren ',7);
INSERT INTO article VALUES(224,'Aspirin C',18);
INSERT INTO article VALUES(225,'Wick Hustensaft',18);
INSERT INTO article VALUES(226,'Apotheke 1',18);
INSERT INTO article VALUES(227,'Apotheke 2',18);
CREATE TABLE shopping_list (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	user_id INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO shopping_list VALUES(4,'Einkauf',3,'2024-11-29 15:39:58.100446');
INSERT INTO shopping_list VALUES(5,'Kaufen',1,'2024-11-29 18:24:20.173502');
CREATE TABLE shopping_list_item (
	shopping_list_id INTEGER NOT NULL, 
	article_id INTEGER NOT NULL, 
	quantity VARCHAR(20), 
	unit VARCHAR(20), 
	notes VARCHAR(200), 
	checked BOOLEAN, 
	PRIMARY KEY (shopping_list_id, article_id), 
	FOREIGN KEY(shopping_list_id) REFERENCES shopping_list (id), 
	FOREIGN KEY(article_id) REFERENCES article (id)
);
COMMIT;
