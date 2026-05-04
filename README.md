# 🏨 Hotel Reservation System

A desktop management suite built in Python that handles multi-hotel bookings, room availability tracking, and customer records using a relational SQLite database.

---

## 📸 Demo
![Application Screenshot or GIF](./path/to/your/demo-image.gif)
*Show the main dashboard or a guest being added to the database.*

## 🚀 Key Features
- **Dynamic Hotel Management**: Supports multiple properties, each with unique room types and pricing.
- **Smart Availability Logic**: Calculates real-time room stock across date ranges to prevent overbooking.
- **Relational Database**: A 4-table normalized schema (Hotels, Rooms, Customers, Reservations) ensures data integrity.
- **Bulk Data Ingestion**: Built-in support for importing customer records from **CSV files**.
- **Input Validation**: Integrated error handling for past-date bookings and invalid ID entries.

## 🛠️ Tech Stack
- **Language**: Python 3.13
- **GUI Framework**: Tkinter (Standard Library)
- **Database**: SQLite3
- **Tools**: datetime, csv, messagebox

## 🏗️ Technical Implementation
This project demonstrates several professional software engineering principles:
- **Object Oriented Design**: Utilizes a base DBbase class to abstract database connections, promoting code reuse across the application.
- **Transactional Integrity**: Implements a "Check-then-Commit" phase for reservations; no data is written until all requested dates are verified as available.
- **Safe SQL Queries**: Uses **parameterized queries** throughout to protect against SQL Injection.
- **State Management**: Manages complex GUI state transitions (Home -> Details -> Booking) within a single-window Tkinter application.


## 💻 Installation and Usage
To view the code in action or run it locally:

1. **Clone the repo**:
   ```bash
   git clone https://github.com
   ```
2. **Initialize the Database**:
   1. Uncomment the test lines in hotel_project.py or run your main script to generate hotel_reservation.sqlite.

3. **Run the App**:
   ```bash
   python3.13 GUI_hotel.py
   ```

---
*Created by Raisa Abrar - [Your LinkedIn/Portfolio Link]*
