# Mzanzi Market

The Mzanzi Market project, completed in accordance with the BFB 321 module requirements, is a web application that addresses the communication gap between Farmers Markets, Vendors and Customers in the South African Supply chain context. This repository contains the code and resources for the project, demonstrating core marketplace features: product listing, browsing, and user interactions.

## Team members and roles
The application was developed in accordance with the BFB 321 module requirements, for **Mr Ibrahim Akanbi** and Mr **Thabang Ngwenya** by **Project Group 04.** The developers are:
| Name | Student ID | Role | GitHub Username |
| :--- | :--- | :--- | :--- |
| **Monique Nel** | u23614057 | Project Lead | Monique-nel | 
| **Beate du Plessis** | u04659075 | Developer | B |
| **Izé Rautenbach** | u23539489 | Developer | I |
| **Lana van Rooyen** | u23524342 | Developer | L |

## Task Allocation
The project workload was distributed as follows:

* **Monique Nel**
    * *Core Responsibilities:* Project management, frontend design, backend logic, Jinja coding, route management
    
* **Beate du Plessis**
    * *Core Responsibilities:* Database setup, database Management and Database integration

* **Izé Rautenbach**
    * *Core Responsibilities:* CSS Styling, Vendors page

* **Lana van Rooyen**
    * *Core Responsibilities:* Documentation, database design
- 
## Features
- User authentication, registration and management
- User detail pages
- Product listing and detail pages
- Admin area for product management (create / edit / remove)
- Search and Filter functionality 
- Market and Vendor catalogue
- Market and Vendor management dashboard
- Order management functionality
- Direct communication and connection between users 
- Basic data analytics for users


## System Architecture 

The application has a three-layer architecture comprising a frontend, backend, and database to ensure functionality. 
- **Frontend** -> Built with Bootstrap, HTML and CSS for an attractive and responsive interface
- **Backend** -> Not yet applicable for this submission, but will be built with Flask and Python functionality
- **Integrated Database** -> The database was created using SQLite, and stores users, markets, vendors, events and product information.  

## User experience 
Please find the application wireframes at the link below: 

https://www.figma.com/design/f7aLnVRKclcaV32dRpTcuk/BFB-website-design?node-id=0-1&t=Y2KUCGWX4J2IAIZk-1


## Database Design and Setup

The databases used for this project are discussed below and include the setup, layout, sample data, visualisation, and an ERD. 

---

### Database setup using SQLite Command Line

1. Open the command prompt/terminal in the project directory
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
   Each market entry includes location, scheduling, and contact information, along with links to its social media pages.  
   - **Fields include**: `MarketID`, `MarketName`, `MarketDescription`, `MarketLocation`, `MarketLocationLink`, `MarketEntryFee`, `MarketDate`, `MarketDays`, `MarketPoster`, `MarketInstagram`, `MarketFacebook`, `MarketMap`, `MarketAdministratorID`  
   - **Purpose**: Enables administrators to list and promote markets with comprehensive detail for customers and vendors.  

3. **vendors**:  
   Contains details for all participating vendors operating in different markets.  
   Each vendor is linked to a `UserID` (classified as a Vendor) and may operate at multiple markets.  
   - **Fields include**: `VendorID`, `VendorName`, `VendorStallDescription`, `VendorLocation`, `VendorContactNumber`, `VendorOfferingType`, `VendorDescriptionPicture`, `VendorWebsite`, `VendorFacebook`, `VendorInstagram`, `VendorLogo`, `UserID`  
   - **Purpose**: Allows customers to discover unique stalls, products, and artisans across South African markets.  

4. **events**:  
   List special market events, themed festivals, or seasonal gatherings associated with a specific market.  
   Each event provides booking links, promotional posters, and details about the date and day of the week.  
   - **Fields include**: `EventID`, `EventName`, `EventDescription`, `EventDate`, `EventDays`, `EventBookingLink`, `EventPoster`, `MarketID`  
   - **Purpose**: Promotes upcoming market events, enabling customers to view details and vendors to participate in event opportunities.  

---

### Relationships

The Mzanzi Market database follows a **relational structure** that connects users, markets, vendors, and events:

- **users → markets**:  
  Each market is managed by a single user, designated as *Market Administrator*.  

- **users → vendors**:  
  Each vendor profile is owned by one user classified as a *Vendor*.  

- **markets → vendors**:  
  Vendors are associated with markets where they operate (via `VendorLocation` or cross-references).  

- **markets → events**:  
  Each event is hosted by a specific market (linked through `MarketID` as a foreign key).  

This ensures referential integrity and enables efficient querying of related information — for example, displaying all events hosted at a particular market or showing all vendors under a single administrator.

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
Insert this code into Mzanzi.sql to see the tables filled with sample data.
```bash
SELECT * FROM "User";
SELECT * FROM "Market";
SELECT * FROM "Vendor";
SELECT * FROM "Events";
```

## Entity Relationship Diagram

The Relationships between the entities in the database are explored in the ERD below. The ERD was created in MySQL Workbench.  
![ERD in PNG format](https://github.com/Monique-nel/BFB321-Group04/blob/main/ERD%20Reviewed.png?raw=true)


## File Structure
```
├── static/                      # Holds CSS, JS, and images
├── templates/                   # HTML templates rendered by Flask
│   ├── images/                  # Template-related images
│   ├── About.html               # About page
│   ├── EventForm.html           # Event creation form
│   ├── events.html              # List of all events
│   ├── FAQ.html                 # Frequently asked questions page
│   ├── generalpolicies.html     # Market policies and rules
│   ├── home.html                # Home page
│   ├── login.html               # User login page
│   ├── register.html            # New user registration page
│   ├── userpage.html            # User dashboard
│   ├── vendors.html             # Vendor dashboard
│   ├── marketrequestform.html   # Market request submission form
│   ├── vendorrequestform.html   # Vendor request submission form
│   ├── map_4way.html            # Map for Fourways market
│   ├── map_hazelwood.html       # Map for Hazelwood market
│   ├── map_irene.html           # Map for Irene market
│   ├── map_montana.html         # Map for Montana market
│   ├── map_pretoria.html        # Map for Pretoria market
│   ├── map_vintage.html         # Map for Vintage market
│
├── Mzanzi.db                    # SQLite database
├── Mzanzi.sql                   # Database schema and sample data
├── __pycache__/                 # Compiled Python cache files
└── README.md                    # This file
```

## Getting started

Setting up the Mzanzi Market Application locally consists of the following steps: 
- Clone the repository to your local drive
- Open *home.html* in your web browser
- Navigate through the app to reach the necessary functionality.
- Click on the **User Icon** found in the Navigation bar to register or sign in

## Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5  
- **Backend:** Flask (Python) *(in progress)*  
- **Database:** SQLite  
- **Design Tools:** Figma, MySQL Workbench

## Browser Compatibility

The application works with all modern browsers that support HTML5 and CSS3, including:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License
Please note this project is currently only for academic use and is the Intellectual Property of the Application Developers and the University of Pretoria.

## Contact
Project maintained for BFB 321 — University of Pretoria.
For questions, open an issue or contact the project owner listed in the repository.


