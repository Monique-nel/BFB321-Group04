INSERT INTO "User" (Username, Email, Password, Classification)
VALUES ('Admin1', 'admin@market.com', '12345', 'MarketAdministrator');

INSERT INTO MarketAdministrator (ContactNumber, UserID)
VALUES ('0821234567', 1);

INSERT INTO Market (MarketName, MarketDescription, MarketLocation)
VALUES ('Mzanzi Market', 'A vibrant local market.', 'Pretoria');