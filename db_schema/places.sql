CREATE TABLE places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position POINT NOT NULL,
    title VARCHAR(255),
    address VARCHAR(255),
    category ENUM('DIGITAL_FACTORY', 'ROBOSMITH', 'TECHNO_FARMER'),
    SPATIAL INDEX (position)
);

