# Parts Supplier Database Application

A lightweight Flask-based web application for interacting with a classic Supplier–Parts–Shipments (SPS) database.  
The app allows users to:

- View all suppliers, parts, and shipments  
- Insert predefined shipments  
- Reseed the database  
- Run custom queries (suppliers by part number, increase supplier status, etc.)  
- Display query results cleanly using Bootstrap modals

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+

- MySQL Server and MySQL Workbench

- pip (Python package manager)

- Optional: virtualenv for isolated environments

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/supplier-database.git
cd supplier-database
```
### 2. Start MySQL Server

Launch your MySQL Server instance using MySQL Workbench or the command line. <br>
IMPORTANT: You must update the password in app.py to your local database password.

### 3. Install Dependencies

It’s recommended to use a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate        # On Windows
source venv/bin/activate     # On macOS/Linux
```

Open a terminal in the project’s root folder and install dependencies:
```bash
pip install -r requirements.txt
```
### 4. Run the Application

Start the Flask app:
```bash
python app.py
```
Then open your browser and go to:
```text
http://127.0.0.1:5000
```
### 5. Initialize the Database

The database suppliers_and_parts will be created and seeded by clicking the Start Over button at the bottom.
