CREATE TABLE individuals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    place_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

