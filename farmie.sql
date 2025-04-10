-- Create the database
CREATE DATABASE IF NOT EXISTS Farmie;

-- Use the database
USE Farmie;

-- Create User table
CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create Farm table
CREATE TABLE Farm (
    farm_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Create Crop table
CREATE TABLE Crop (
    crop_id INT PRIMARY KEY AUTO_INCREMENT,
    crop_name VARCHAR(100) NOT NULL,
    crop_family VARCHAR(100) NOT NULL
);

-- Create Cultivate table (linking crops and farms)
CREATE TABLE Cultivate (
    crop_id INT,
    farm_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY (crop_id, farm_id),
    FOREIGN KEY (crop_id) REFERENCES Crop(crop_id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES Farm(farm_id) ON DELETE CASCADE
);
