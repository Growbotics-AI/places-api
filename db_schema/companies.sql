CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    place_id INT,
    name VARCHAR(255),
    website VARCHAR(255),
    email VARCHAR(255),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

