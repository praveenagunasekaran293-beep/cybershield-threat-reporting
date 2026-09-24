# CyberShield – Cyber Threat Reporting & Incident Management System

## Overview

CyberShield is a Python Flask and MySQL-based web application designed to report, manage, search, and monitor cybersecurity threats.

The system provides user authentication, threat report management, CRUD operations, search and filtering, dashboard statistics, and threat severity visualization.

---

## Features

- User Registration and Login
- Password Hashing
- Session-based Authentication
- Cyber Threat Reporting
- Create, Read, Update and Delete (CRUD) Operations
- Search Threat Reports
- Filter by Severity and Status
- Dashboard Statistics
- Threat Severity Chart
- Recent Threat Reports
- Input Validation
- MySQL Database Integration
- Environment Variable Configuration

---

## Technologies Used

- Python
- Flask
- MySQL
- XAMPP
- HTML5
- Bootstrap 5
- JavaScript
- Chart.js
- python-dotenv
- Werkzeug

---

## System Modules

### 1. User Authentication

Users can register an account and securely log in to the system.

Passwords are stored using password hashing instead of plain text.

### 2. Dashboard

The dashboard displays:

- Total Threat Reports
- Open Threats
- Critical Threats
- Resolved Threats
- Threat Severity Chart
- Recent Threat Reports

### 3. Threat Management

Users can:

- Add new threat reports
- View threat reports
- Edit existing reports
- Delete reports

### 4. Search and Filtering

Threat reports can be searched using:

- Threat title
- Description
- Threat type

Reports can also be filtered by:

- Severity
- Status

---

## Supported Threat Types

- Phishing
- Malware
- Ransomware
- SQL Injection
- DDoS
- Brute Force
- Data Breach
- Other

---

## Severity Levels

- Low
- Medium
- High
- Critical

---

## Status Levels

- Open
- Investigating
- Resolved

---

## Project Structure

```text
CyberShield/
│
├── venv/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── threats.html
│   ├── add_threat.html
│   └── edit_threat.html
│
├── static/
│
├── screenshots/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── cybershield_db.sql
└── README.md

Database

The application uses MySQL through XAMPP.

Database Name
cybershield_db
Tables
users
threat_reports

The SQL database structure is provided in:

cybershield_db.sql

Installation
1. Clone the Repository
git clone https://github.com/<your-username>/cybershield-threat-reporting.git

Move into the project folder:

cd cybershield-threat-reporting
2. Create Virtual Environment
python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate
3. Install Required Packages
pip install -r requirements.txt
4. Start XAMPP

Open XAMPP Control Panel and start:

Apache
MySQL
5. Create Database

Open:

http://localhost/phpmyadmin

Create the database:

cybershield_db

Import:

cybershield_db.sql
6. Configure Environment Variables

Create a .env file in the project root.

Example:

SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=cybershield_db

Do not share or upload private credentials.

7. Run the Application

Activate the virtual environment and run:

python app.py

The application will be available at:

http://127.0.0.1:5000

Security Measures

CyberShield includes several basic security practices:

Password hashing using Werkzeug
Parameterized SQL queries
Session-based authentication
Input validation
Restricted threat type values
Restricted severity values
Restricted status values
Environment variables for database configuration
.env excluded from Git using .gitignore

CRUD Operations

The application supports complete CRUD functionality.

Create  → Add Threat Report
Read    → View Threat Reports
Update  → Edit Threat Report
Delete  → Delete Threat Report

uture Enhancements

Possible future improvements include:

Role-based access control
Email notifications
Advanced analytics
PDF report generation
Threat intelligence API integration
Automated threat classification
AI-based threat analysis
Incident response workflow
Admin management panel

Project Purpose

This project was developed as an academic cybersecurity web application to demonstrate the integration of Python Flask, MySQL database management, authentication, CRUD operations, validation, and dashboard-based cybersecurity monitoring.

