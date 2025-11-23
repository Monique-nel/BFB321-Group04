-- USER TABLE
CREATE TABLE "User" (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    Classification TEXT CHECK (Classification IN ('Customer', 'Vendor', 'MarketAdministrator')) NOT NULL
);

-- CUSTOMER TABLE
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    Preferences TEXT,
    FOREIGN KEY (UserID) REFERENCES "User"(UserID)
);

-- VENDOR TABLE
CREATE TABLE Vendor (
    VendorID INTEGER PRIMARY KEY AUTOINCREMENT,
    VendorName TEXT NOT NULL,
    VendorStallDescription TEXT,
    VendorLocation TEXT,
    VendorContactNumber TEXT,
    VendorOfferingType TEXT,
    VendorDescriptionPicture BLOB,
    VendorWebsite TEXT,
    VendorFacebook TEXT,
    VendorInstagram TEXT,
    VendorLogo BLOB,
    UserID INTEGER NOT NULL,
    FOREIGN KEY (UserID) REFERENCES "User"(UserID)
);

-- MARKET ADMINISTRATOR TABLE
CREATE TABLE MarketAdministrator (
    MarketAdministratorID INTEGER PRIMARY KEY AUTOINCREMENT,
    ContactNumber TEXT,
    UserID INTEGER NOT NULL,
    FOREIGN KEY (UserID) REFERENCES "User"(UserID)
);

-- MARKET TABLE
CREATE TABLE Market (
    MarketID INTEGER PRIMARY KEY AUTOINCREMENT,
    MarketName TEXT NOT NULL,
    MarketDescription TEXT,
    MarketLocationLink TEXT,
    MarketLocation TEXT,
    MarketEntryFee TEXT,
    MarketDate DATETIME,
    MarketDays TEXT,
    MarketPoster BLOB,
    MarketInstagram TEXT,
    MarketFacebook TEXT,
    MarketMap BLOB,
    MarketAdministratorID INTEGER,
    FOREIGN KEY (MarketAdministratorID) REFERENCES MarketAdministrator(MarketAdministratorID)
);

-- ASSIGNED STALL TABLE
CREATE TABLE AssignedStall (
    StallID INTEGER PRIMARY KEY AUTOINCREMENT,
    MarketID INTEGER NOT NULL,
    StallMarketSection TEXT,
    VendorID INTEGER NOT NULL,
    VendorAlternateID INTEGER,
    FOREIGN KEY (MarketID) REFERENCES Market(MarketID),
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID)
);

-- EVENTS TABLE
CREATE TABLE Events (
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName TEXT NOT NULL,
    EventDescription TEXT,
    EventDate DATETIME,
    EventDays TEXT,
    EventBookingLink TEXT,
    EventPoster BLOB,
    MarketID INTEGER NOT NULL,
    FOREIGN KEY (MarketID) REFERENCES Market(MarketID)
);

-- PRODUCT TABLE
CREATE TABLE "Product" (
    "ProductID"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "ProductName"  TEXT NOT NULL,
    "ProductPrice" REAL NOT NULL,
    "VendorID"     INTEGER NOT NULL,
    FOREIGN KEY("VendorID") REFERENCES "Vendor"("VendorID")
);