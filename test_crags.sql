
-- Query: 

CREATE DATABASE meteoclimb;

CREATE TABLE test_crags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL,
    crag_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL)
;
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Andalucia','Alfarnatejo',36.96715924,-4.26560976);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Andalucia','Antigua Cantera de Torremolinos',36.62535406,-4.52489825);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Andalucia','Archidona',37.09291680,-4.36884592);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Andalucia','Bedmar La Serrezuela',37.82561574,-3.40589669);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Andalucia','Belmez',38.26335266,-5.19906484);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Aragon','Aguja de Escalete',42.37475641,-0.70636760);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Aragon','Albarracín',40.39892722,-1.41818170);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Aragon','Alcañiz',41.07828629,-0.13125428);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Aragon','Aldehuela de Liestos',41.06389184,-1.70123486);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Aragon','Alfambra',40.57168624,-1.01616794);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Asturias','Boveda de Fresnedo',43.38806915,-5.79978225);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Asturias','Canal del Texu',43.24347324,-4.83085927);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Asturias','Centro',43.28142938,-5.82797678);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Asturias','Cuchiellu de la Gezma',43.23030109,-4.74774588);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Asturias','Cueva del Mar',43.26302269,-6.00088769);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cantabria','Abiada',43.01932875,-4.30064150);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cantabria','Alsa',43.10781010,-4.01318385);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cantabria','Alto de San Cipriano',43.29262456,-4.12581648);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cantabria','Argüeso',43.03058010,-4.20227290);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cantabria','Asón',43.21189765,-3.57879180);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla la Mancha','Ayna',38.55578871,-2.07944837);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla la Mancha','Barranco de la Hoz',40.81857151,-2.02001992);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla la Mancha','Barranco de la Viana',41.04255260,-2.74978300);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla la Mancha','Buendia',40.37327576,-2.79400885);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla la Mancha','Castillo de Bayuela',40.10462815,-4.68470789);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla y Leon','Abioncillo',41.71047580,-2.86446254);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla y Leon','Añavieja',41.88238339,-1.98275668);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla y Leon','Arrabalde',42.10200327,-5.91328336);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla y Leon','Basconcillos del Tozo',42.70834530,-3.98550380);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Castilla y Leon','Boós-Valdenebro',41.59463018,-2.93143551);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cataluña','Amitges',42.58802259,1.02632148);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cataluña','Arboli',41.23765075,0.94598000);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cataluña','Arties',42.70518919,0.87060241);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cataluña','Banyadores',41.53807255,2.37834975);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Cataluña','Bauma de Can Solà',41.59830844,1.75150660);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Comunidad Valenciana','45 Grados',38.81624115,-0.21217045);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Comunidad Valenciana','Adsubia',38.85288177,-0.16838320);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Comunidad Valenciana','Agres',38.79600428,-0.49932899);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Comunidad Valenciana','Aixortà',38.70650379,-0.17481291);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Comunidad Valenciana','Alcalali',38.75602948,-0.05209262);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Extremadura','Alange',38.78600715,-6.26016088);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Extremadura','El Castellar',38.41911899,-6.44569080);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Extremadura','El Cerro',40.12281871,-5.95081801);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Extremadura','Las monjas',40.19005162,-5.81757493);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Extremadura','Puerto Peña',39.19923245,-5.21403075);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Galicia','A Coruña - Paseo Marítimo',43.38060902,-8.41042781);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Galicia','A Picaraña',42.18945387,-8.47990896);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Galicia','A Rúa: Roblido y Seadur',42.39241557,-7.15664527);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Galicia','Acantilados de Chanteiro',43.44442183,-8.31282291);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Galicia','Acantilados de Suevos 🚫',43.34081033,-8.49716016);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Baleares','Aparcamiento',39.32681369,3.15448101);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Baleares','C\'an Nyic',39.79174812,2.77708006);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Baleares','Ca\'n Torrat',39.68864270,2.71940445);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Baleares','Cala Barques',39.50078161,3.29925405);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Baleares','Cala Bota',39.47510335,3.28786366);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Canarias','El Hierro',27.74689435,-18.02053495);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Canarias','Fuerteventura',28.39038405,-14.17518380);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Canarias','Gran Canaria',27.95466930,-15.59083995);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Canarias','La Gomera',28.11849965,-17.22448385);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Islas Canarias','La Palma',28.65314775,-17.86581080);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('La Rioja','Anguiano',42.25921443,-2.76760127);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('La Rioja','Arnedillo',42.21340885,-2.23013495);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('La Rioja','Autol',42.21529936,-2.00570281);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('La Rioja','Clavijo',42.35009960,-2.42752480);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('La Rioja','Ezcaray',42.33267495,-3.00731201);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Madrid','Abantos',40.60505655,-4.14886455);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Madrid','Alto del Telégrafo',40.78317335,-4.01301835);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Madrid','Cadalso de los Vidrios',40.29952809,-4.41783071);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Madrid','El Vellón',40.77837662,-3.62805386);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Madrid','Emburriaderos',40.50152067,-3.72200915);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Murcia','Almorchón',38.21411128,-1.54475213);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Murcia','Alumbres',37.59937927,-0.92577717);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Murcia','Barranco del Marqués',38.43539700,-1.36270028);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Murcia','Benizar',38.26446080,-1.98534895);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Murcia','Cabezo de la Fuente',37.60395675,-0.77464530);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Navarra','Aitzondo',42.92743295,-1.96162014);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Navarra','Axkin Arrondo',43.15181500,-1.68173025);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Navarra','Belagua',42.95250765,-0.81871515);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Navarra','Bidankoze (Vidángoz)',42.79924621,-1.01215046);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Navarra','Dos Hermanas - Biaizpe (Irurtzun)',42.92794985,-1.82427625);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Pais Vasco','Adarra',43.20665925,-1.96033175);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Pais Vasco','Aguake',42.70637665,-2.39703200);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Pais Vasco','Aiako Harria',43.28864895,-1.78626315);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Pais Vasco','Aizkorri',43.20354381,-1.98348653);
INSERT INTO test_crags (`region_name`,`crag_name`,`latitude`,`longitude`) VALUES ('Pais Vasco','Alkiza',43.17130388,-2.12580239);
