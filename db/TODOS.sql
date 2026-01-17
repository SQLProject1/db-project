CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) NOT NULL UNIQUE,
    password VARCHAR(250) NOT NULL
);

CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content VARCHAR(100),
    due DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE kriminelle ( 
foto INT AUTO_INCREMENT PRIMARY KEY,
    ID CHAR(7),
    Name VARCHAR(40) ,
    Geschlecht VARCHAR(10),
    Ethnie VARCHAR(20),
    Geburtsdatum CHAR(10),
    Geburtsort VARCHAR (100),
    Haarfarbe VARCHAR (25),
    Augenfarbe VARCHAR (25),
    Gewicht VARCHAR (10),
    Körpergrösse CHAR(10),
    Nationalität (35),
);

CREATE TABLE verbrechen (

    anklagepunkt INT AUTO_INCREMENT PRIMARY KEY,
    verbrechenstyp VARCHAR(20),
    geldsstrafe varchar(10),
    gefängniszeit CHAR(10),
    vergehen_oder_verbrechen BOOL
    
);

CREATE TABLE gefaengnis (
    gefängnis_ID INT AUTO_INCREMENT PRIMARY KEY,
    Ort varchar(67),
    Sicherheitslevel varchar(1)
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    test CHAR (67),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

    
    
