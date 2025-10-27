# Mzanzi Market

The Mzanzi Market project, completed in accoordance with the BFB 321 module requirements, is a web application that adresses the communication gap between Farmers Markets, Vendors and Customers in the South African Supply chain context. This repository contains the code and resources for the project to demonstrate core marketplace features: product listing, browsing, user interactions and basic order flow. Multiple coding languages and features were used in project completion. 

## Project owners
The application was developed in accordance with the BFB 321 module requirements, by Group 04. The developers are:
- **Monique Nel** (Project lead): u23614057
- **Beate du Plessis** : u04659075
- **Izé Rautenbach** : u23539489
- **Lana van Rooyen** : u23524342 
## Features
- User authenitication, registration and management
- User detail pages
- Product listing and detail pages
- Admin area for product management (create / edit / remove)
- Search and Filter functionality 
- Market and Vendor catalogue
- Market and Vendor management dashboard
- Order management functionality
- Direct communication and connection between users 
- Basic data analytics for users


## System Architechture 

The application consists of a three-layer integrated architecture, consisting of a frontend, backend and database, to ensure functionality. 
- **Frontend** -> Built with Bootstrap, HTML and CSS for an attractive and responsive interface
- **Backend** -> Not yet applicable for this submission, but built with Flask and Python functionality
- **Integrated Database** -> The database was created using SQLite, and stores users, markets, vendors, and product information.  

## User experience 

Ize, please add the wireframes here later 


## Database Design and Setup

The databases used for this project is  discussed below and contains the setup, layout, sample data and visualisation, and an ERD. 

---

### Using SQLite Command Line

1. Open command prompt/terminal in the project directory
2. Run the SQL commands:
   ```bash
   Mzanzi.db < Mzanzi.sql
   ```
The database includes 8 tables, those containing data are listed below:

### Tables

1. **users**:  
   Stores information for all users registered on the Mzanzi Market platform.  
   Each user has an assigned role that defines their permissions and interactions in the system.  
   - **Fields include**: `UserID`, `Username`, `Email`, `Password`, `Classification`  
   - **Classification types**:  
     - *MarketAdministrator*: manages market listings, events, and vendors  
     - *Vendor*: manages stalls, offerings, and event participation  
     - *Customer*: browses markets, views events, and connects with vendors  

2. **markets**:  
   Represents the various community markets featured on the platform.  
   Each market entry provides location, scheduling, and contact information, as well as links to its social media pages.  
   - **Fields include**: `MarketID`, `MarketName`, `MarketDescription`, `MarketLocation`, `MarketLocationLink`, `MarketEntryFee`, `MarketDate`, `MarketDays`, `MarketPoster`, `MarketInstagram`, `MarketFacebook`, `MarketMap`, `MarketAdministratorID`  
   - **Purpose**: Enables administrators to list and promote markets with comprehensive detail for customers and vendors.  

3. **vendors**:  
   Contains details for all participating vendors operating at different markets.  
   Each vendor is linked to a `UserID` (classified as a Vendor) and may operate at multiple markets.  
   - **Fields include**: `VendorID`, `VendorName`, `VendorStallDescription`, `VendorLocation`, `VendorContactNumber`, `VendorOfferingType`, `VendorDescriptionPicture`, `VendorWebsite`, `VendorFacebook`, `VendorInstagram`, `VendorLogo`, `UserID`  
   - **Purpose**: Allows customers to discover unique stalls, products, and artisans across South African markets.  

4. **events**:  
   Lists special market events, themed festivals, or seasonal gatherings associated with a specific market.  
   Each event provides booking links, promotional posters, and details about the date and day of the week.  
   - **Fields include**: `EventID`, `EventName`, `EventDescription`, `EventDate`, `EventDays`, `EventBookingLink`, `EventPoster`, `MarketID`  
   - **Purpose**: Promotes upcoming market events, enabling customers to view details and vendors to participate in event opportunities.  

---

### Relationships

The Mzanzi Market database follows a **relational structure** that connects users, markets, vendors, and events:

- **users → markets**:  
  Each market is managed by one user classified as a *Market Administrator*.  

- **users → vendors**:  
  Each vendor profile is owned by one user classified as a *Vendor*.  

- **markets → vendors**:  
  Vendors are associated with markets where they operate (via `VendorLocation` or cross-references).  

- **markets → events**:  
  Each event is hosted by a specific market (linked through `MarketID` as a foreign key).  

This ensures referential integrity and allows efficient querying of related information — for example, displaying all events hosted at a particular market or showing all vendors under one administrator.

---

## Sample Data

The database includes sample data for testing and demonstration purposes:

- **4 Market Administrators**: Admin1, BeateDup, Gloria, Sheldoor  
- **3 Markets**:  
  1. *4 Ways Farmers Market* — Modderfontein, Johannesburg (Entry Fee: R20)  
  2. *Pretoria Boeremark* — Silverton, Pretoria  
  3. *Montana Family Market* — Montana, Pretoria  
- **3 Events**:  
  1. *Flavors of Africa Food Festival* — Celebrating African cuisine with live demos and tasting stations  
  2. *Mzansi Music & Market Nights* — Evening market with food trucks and live local music  
  3. *Spring Craft & Handmade Fair* — Showcasing handmade goods and local artisans  
- **3 Vendors**: Peach & Pip, BumbleBean, DaisyDot  
- **3 Customers**: Sarah, Ietsie, BiancaNel  

---

## Example Event Data

| EventID | EventName | EventDate | EventDays | MarketID |
|----------|------------|------------|------------|-----------|
| 1 | Flavors of Africa Food Festival | 14 September 2025 | Saturday | 1 |
| 2 | Mzansi Music & Market Nights | 18 October 2025 | Friday | 2 |
| 3 | Spring Craft & Handmade Fair | 22 September 2025 | Sunday | 3 |

Each event record includes:
- A detailed event description (activities, entertainment, food themes)  
- A Google Forms booking or registration link  
- A promotional poster image for marketing  
- A foreign key (`MarketID`) linking the event to its host market  

---

## Data Visualisation
Insert this code into Mzanzi.sql to see current tables.
```bash
SELECT * FROM "User";
SELECT * FROM "Market";
SELECT * FROM "Vendor";
SELECT * FROM "Events";
```


The Relationship between the different entities in the database is explored in the ERD below.  
![ERD in PNG format](https://github.com/Monique-nel/BFB321-Group04/blob/main/ERD%20Reviewed.png?raw=true)


## Repository Structure 
- **static/** -> Holds the CSS, JS and Images
- **templates/** -> HTML templates and Flask
- **Something something** -> Flask main application file
- **Mzanzi.sql** -> Database models
- **README.md** -> Application description and explaination  of setup


## Getting started

Prerequisites
- Node 14+ and npm (if using Node)
- Or the appropriate runtime for your chosen stack
- Database service configured (MongoDB, Postgres, etc.)

Quick start (Node + npm example)
1. Clone the repo
    git clone <repository-url>
2. Install dependencies
    cd mzanzi-market
    npm install
3. Environment
    - Copy .env.example to .env and update DB / API keys
4. Run locally
    npm run dev
5. Open http://localhost:3000 (or configured port)

Adjust the commands to match your actual project scripts.

## Development
- Follow the project's branching and commit message conventions.
- Run linters and formatters before pushing.
- Use feature branches and open pull requests for review.

Common commands (replace as needed)
- npm run lint
- npm run test
- npm run build

## Testing
- Unit tests for core modules
- Integration tests for API endpoints
- Frontend component tests (if applicable)

Run tests:
npm test

## Deployment
- Build production assets: npm run build
- Deploy backend to your chosen host (Heroku, Vercel, AWS, Azure)
- Configure environment variables on the host

## Contributing
- Fork the repo
- Create a feature branch
- Open a pull request with a clear description of changes
- Ensure tests pass and code is linted

<a href="https://www.instagram.com/montana_family_market/" class="text-dark fs-6">
                  <img src="images/instagram.png" alt="instagram" height="30" class="me-4">
                </a>

## License
Specify a license (e.g., MIT). Add a LICENSE file to the repository.

## Contact
Project maintained for BFB 321 — University of Pretoria.
For questions, open an issue or contact the project owner listed in the repository.

## Database Setup

### Using SQLite Command Line

1. Open command prompt/terminal in the project directory
2. Run the SQL commands:
   ```bash
   Mzanzi.db < Mzanzi.sql
   ```
The database includes 8 tables, those containing data are listed below:

### Tables

1. **users**:  
   Stores information for all users registered on the Mzanzi Market platform.  
   Each user has an assigned role that defines their permissions and interactions in the system.  
   - **Fields include**: `UserID`, `Username`, `Email`, `Password`, `Classification`  
   - **Classification types**:  
     - *MarketAdministrator*: manages market listings, events, and vendors  
     - *Vendor*: manages stalls, offerings, and event participation  
     - *Customer*: browses markets, views events, and connects with vendors  

2. **markets**:  
   Represents the various community markets featured on the platform.  
   Each market entry provides location, scheduling, and contact information, as well as links to its social media pages.  
   - **Fields include**: `MarketID`, `MarketName`, `MarketDescription`, `MarketLocation`, `MarketLocationLink`, `MarketEntryFee`, `MarketDate`, `MarketDays`, `MarketPoster`, `MarketInstagram`, `MarketFacebook`, `MarketMap`, `MarketAdministratorID`  
   - **Purpose**: Enables administrators to list and promote markets with comprehensive detail for customers and vendors.  

3. **vendors**:  
   Contains details for all participating vendors operating at different markets.  
   Each vendor is linked to a `UserID` (classified as a Vendor) and may operate at multiple markets.  
   - **Fields include**: `VendorID`, `VendorName`, `VendorStallDescription`, `VendorLocation`, `VendorContactNumber`, `VendorOfferingType`, `VendorDescriptionPicture`, `VendorWebsite`, `VendorFacebook`, `VendorInstagram`, `VendorLogo`, `UserID`  
   - **Purpose**: Allows customers to discover unique stalls, products, and artisans across South African markets.  

4. **events**:  
   Lists special market events, themed festivals, or seasonal gatherings associated with a specific market.  
   Each event provides booking links, promotional posters, and details about the date and day of the week.  
   - **Fields include**: `EventID`, `EventName`, `EventDescription`, `EventDate`, `EventDays`, `EventBookingLink`, `EventPoster`, `MarketID`  
   - **Purpose**: Promotes upcoming market events, enabling customers to view details and vendors to participate in event opportunities.  

---

### Relationships

The Mzanzi Market database follows a **relational structure** that connects users, markets, vendors, and events:

- **users → markets**:  
  Each market is managed by one user classified as a *Market Administrator*.  

- **users → vendors**:  
  Each vendor profile is owned by one user classified as a *Vendor*.  

- **markets → vendors**:  
  Vendors are associated with markets where they operate (via `VendorLocation` or cross-references).  

- **markets → events**:  
  Each event is hosted by a specific market (linked through `MarketID` as a foreign key).  

This ensures referential integrity and allows efficient querying of related information — for example, displaying all events hosted at a particular market or showing all vendors under one administrator.

---

## Sample Data

The database includes sample data for testing and demonstration purposes:

- **4 Market Administrators**: Admin1, BeateDup, Gloria, Sheldoor  
- **3 Markets**:  
  1. *4 Ways Farmers Market* — Modderfontein, Johannesburg (Entry Fee: R20)  
  2. *Pretoria Boeremark* — Silverton, Pretoria  
  3. *Montana Family Market* — Montana, Pretoria  
- **3 Events**:  
  1. *Flavors of Africa Food Festival* — Celebrating African cuisine with live demos and tasting stations  
  2. *Mzansi Music & Market Nights* — Evening market with food trucks and live local music  
  3. *Spring Craft & Handmade Fair* — Showcasing handmade goods and local artisans  
- **3 Vendors**: Peach & Pip, BumbleBean, DaisyDot  
- **3 Customers**: Sarah, Ietsie, BiancaNel  

---

## Example Event Data

| EventID | EventName | EventDate | EventDays | MarketID |
|----------|------------|------------|------------|-----------|
| 1 | Flavors of Africa Food Festival | 14 September 2025 | Saturday | 1 |
| 2 | Mzansi Music & Market Nights | 18 October 2025 | Friday | 2 |
| 3 | Spring Craft & Handmade Fair | 22 September 2025 | Sunday | 3 |

Each event record includes:
- A detailed event description (activities, entertainment, food themes)  
- A Google Forms booking or registration link  
- A promotional poster image for marketing  
- A foreign key (`MarketID`) linking the event to its host market  

---

## Data Visualisation
Insert this code into Mzanzi.sql to see current tables.
```bash
SELECT * FROM "User";
SELECT * FROM "Market";
SELECT * FROM "Vendor";
SELECT * FROM "Events";
```
