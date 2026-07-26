# AgriSetu
# 🌾 AgriSetu
### Smart Agricultural Subsidy Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![Leaflet](https://img.shields.io/badge/Leaflet-GIS-green?style=for-the-badge&logo=leaflet)

</p>

---

# 📖 Overview

AgriSetu is a web-based Agricultural Subsidy Management System developed to digitize and simplify the distribution of government agricultural subsidies. It enables administrators to register farmers, manage subsidy inventory, issue subsidies transparently, visualize farmer locations through GIS mapping, and generate downloadable reports.

The system minimizes paperwork, improves transparency, and provides efficient inventory management through an easy-to-use dashboard.

Demo video and Live demo at end of readme

---

# 🎯 Problem Statement

Traditional agricultural subsidy distribution relies heavily on manual paperwork, making the process slow, inefficient, and difficult to monitor.

Major challenges include:

- Manual farmer registration
- Lack of centralized farmer database
- Poor inventory tracking
- Non-transparent subsidy distribution
- Difficulty generating reports
- No geographical visualization of beneficiaries

---

# 💡 Proposed Solution

AgriSetu provides a centralized digital platform that enables:

- Digital farmer registration
- Secure subsidy distribution
- Real-time inventory management
- GIS-based farmer location visualization
- Distribution history tracking
- CSV report generation
- Dashboard analytics for administrators

---

# ✨ Key Features

## 👨‍🌾 Farmer Management
- Register farmers
- Edit farmer details
- Search farmers
- Delete records

## 🌱 Subsidy Management
- Issue agricultural subsidies
- Track subsidy distribution
- Maintain complete subsidy history

## 📦 Inventory Management
- Manage fertilizer inventory
- Track available stock
- Automatic stock updates after subsidy distribution

## 🗺 GIS Mapping
- Display farmer locations
- Interactive map using Leaflet
- Better geographical monitoring

## 📊 Dashboard
- Farmer statistics
- Inventory summary
- Recent activities
- Distribution overview

## 📄 Report Generation
- Export farmer records
- CSV report download
- Printable records

---

# 🏗 System Architecture

```
                 Administrator
                       │
                       ▼
             Flask Web Application
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Farmer Module   Inventory Module   GIS Module
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                SQLite Database
                       │
                       ▼
         Dashboard • Reports • CSV Export
```

---

# 🛠 Tech Stack

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Backend
- Python
- Flask

## Database
- SQLite

## GIS
- Leaflet.js
- OpenStreetMap

## Tools
- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```
AgriSetu
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── database.db
├── app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/RAHIMA-NILOFER/AgriSetu.git
```

## Navigate

```bash
cd AgriSetu
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 🔄 Workflow

```
Administrator Login
        │
        ▼
Dashboard
        │
        ▼
Register Farmer
        │
        ▼
Store Farmer Details
        │
        ▼
Issue Subsidy
        │
        ▼
Inventory Updated Automatically
        │
        ▼
Subsidy History Saved
        │
        ▼
GIS Map Updated
        │
        ▼
Generate CSV Reports
```

---

# 📸 Application Modules

- Login
- Dashboard
- Farmer Registration
- Farmer Management
- Inventory Management
- Subsidy Distribution
- GIS Map
- History
- CSV Export

---

# 🌟 Advantages

- Paperless farmer management
- Transparent subsidy distribution
- Automatic inventory updates
- GIS visualization
- Faster report generation
- Secure centralized database
- Easy-to-use interface
- Improved administrative efficiency

---

# 🚀 Future Enhancements

- Aadhaar/e-KYC verification
- SMS notification service
- Mobile application
- Cloud deployment
- Multi-language support
- AI-based subsidy recommendation
- Farmer self-service portal
- Advanced analytics dashboard

---

# 👨‍💻 Developed By

**Rahima Nilofer**

B.E. Computer Science and Engineering

Prince Shri Venkateshwara Padmavathy Engineering College

---

#Watch Demo Video 

**https://youtu.be/hHPgV6MTkp4?si=DBAn96P2o8C522wb**

---
#live prototype

**https://rahima2008.pythonanywhere.com**
