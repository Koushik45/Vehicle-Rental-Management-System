-- Users table to store user information
CREATE DATABASE project;
USE project;
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Invoices table to store invoice information
CREATE TABLE Invoices (
    InvoiceID INT PRIMARY KEY,
    StartDate DATE,
    EndDate DATE,
    TotalAmount DECIMAL(10, 2),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Users(UserID)
);

-- Customers table to store customer information
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    UserID INT,
    PhoneNumber VARCHAR(15),
    Address VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Insurance table to store insurance information
CREATE TABLE Insurance (
    InsuranceID INT PRIMARY KEY,
    CoverageType VARCHAR(255) NOT NULL,
    UserID INT,
    InvoiceID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);



-- Vehicles table to store vehicle information
CREATE TABLE Vehicles (
    VehicleID INT PRIMARY KEY AUTO_INCREMENT,
    VehicleType VARCHAR(255) NOT NULL,
    Brand VARCHAR(255),
    Model VARCHAR(255),
    Price DECIMAL(10, 2),
    InsuranceID INT,
    Available BOOLEAN DEFAULT TRUE,  -- Added Available column
    FOREIGN KEY (InsuranceID) REFERENCES Insurance(InsuranceID)
);



-- Reservations table to store reservation information
CREATE TABLE Reservations (
    ResID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    VehicleID INT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);

-- Create a table to represent the n:m relationship between Reservations and Vehicles
CREATE TABLE ReservationVehicle (
    ResID INT,
    VehicleID INT,
    BookingStatus VARCHAR(255),
    FOREIGN KEY (ResID) REFERENCES Reservations(ResID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);


-- Trigger to ensure EndDate is greater than StartDate when inserting a new reservation
DELIMITER //
CREATE TRIGGER check_end_date_insert
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    IF NEW.EndDate <= NEW.StartDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'End date must be greater than start date';
    END IF;
END;
//
DELIMITER ;

-- Trigger to ensure EndDate is greater than StartDate when updating an existing reservation
DELIMITER //
CREATE TRIGGER check_end_date_update
BEFORE UPDATE ON Reservations
FOR EACH ROW
BEGIN
    IF NEW.EndDate <= NEW.StartDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'End date must be greater than start date';
    END IF;
END;
//
DELIMITER ;

-- Trigger to prevent deleting a user with active reservations
DELIMITER //
CREATE TRIGGER prevent_delete_user
BEFORE DELETE ON Users
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM Reservations WHERE UserID = OLD.UserID AND EndDate >= CURDATE()) > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete user with active reservations';
    END IF;
END;
//
DELIMITER ;


-- Trigger to prevent deleting a vehicle with active reservations
DELIMITER //
CREATE TRIGGER prevent_delete_vehicle
BEFORE DELETE ON Vehicles
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM Reservations WHERE VehicleID = OLD.VehicleID AND EndDate >= CURDATE()) > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete vehicle with active reservations';
    END IF;
END;
//
DELIMITER ;




-- Procedure to cancel a reservation
DELIMITER //
CREATE PROCEDURE CancelReservation(IN res_id INT)
BEGIN
    DELETE FROM Reservations WHERE ResID = res_id;
END;
//
DELIMITER ;



ALTER TABLE Users ADD COLUMN Role VARCHAR(255) DEFAULT 'user';

