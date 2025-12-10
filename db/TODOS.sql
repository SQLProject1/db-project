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

CREATE TABLE kriminellen ( 
foto INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) ,
    geburtsdatum CHAR(10),
    rasse VARCHAR(20),
    haftstatus BOOL,
    geschlecht VARCHAR(10)
);

CREATE TABLE verbrechen (
    anklagepunkt INT AUTO_INCREMENT PRIMARY KEY,
    verbrechenstyp VARCHAR(20),
    geldsstrafe FLOAT,
    gefängniszeit CHAR(10),
    vergehen_oder_verbrechen BOOL,
    
);

CREATE TABLE gefängnis (
    efängnis_ID INT AUTO_INCREMENT PRIMARY KEY,
    Ort varchar(67),
    Sicherheitslevel varchar(1),
);
    
    
