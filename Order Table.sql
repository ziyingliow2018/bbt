CREATE TABLE Order(OrderID int NOT NULL, CustomerID int NOT NULL, DateTime TIMESTAMP, Base varchar(200), Toppings varchar(200), TotalPrice double(5, 2), Status varchar, PRIMARY KEY (OrderID), FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID));

SELECT * FROM Order;