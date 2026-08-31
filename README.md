# Expense Tracker
A simple **expense management web application** built with **Python, Flask, HTML, CSS, and JavaScript**. The project allows users to record, organize, and review their expenses through a straightforward web interface.

## 📌 What Is This Project?
The Expense Tracker is a beginner-to-intermediate software project designed to make it easier to keep track of personal spending.

Instead of manually maintaining expenses in a notebook or spreadsheet, users can enter their expenses through the web interface. The application processes the information through a Python backend and displays the results on the website.
The project was also created as a practical way to demonstrate how a **frontend and backend can work together in a web application**.

## ⚙️ How Does It Work?
The application follows a simple frontend-backend architecture:
1. The user interacts with the website through the **HTML/CSS/JavaScript frontend**.
2. Expense information is entered through the interface.
3. JavaScript sends the relevant information to the **Flask backend**.
4. Flask receives and processes the request using Python.
5. The expense-management logic handles the data.
6. The backend returns the appropriate response to the frontend.
7. JavaScript updates the webpage so the user can see the changes.

### Basic Architecture
```text
User
 │
 ▼
Frontend
HTML / CSS / JavaScript
 │
 │ HTTP Requests
 ▼
Flask Backend
 │
 ▼
Python Expense Logic
 │
 ▼
Response
 │
 ▼
Frontend
```
This separation makes the project easier to understand and provides experience with the basic structure used in modern web applications.

## 💡 Why Is It Useful?
Tracking expenses can help users understand where their money is going and develop better spending habits.
The application can be useful for:
* Recording daily expenses
* Keeping expenses organized
* Reviewing spending history
* Understanding spending patterns
* Practicing basic personal-finance management

More importantly, from a software-development perspective, the project demonstrates how a Python program can be turned into an interactive web application.

## 🛠️ Technologies Used
* **Python** – Backend programming and expense-management logic
* **Flask** – Web framework connecting the frontend and backend
* **HTML** – Page structure
* **CSS** – Website styling
* **JavaScript** – User interaction and communication with the backend
* **JSON / HTTP** – Data exchange between the frontend and backend

## ✨ Main Features
* Add and manage expenses
* View recorded expenses
* Organize expense information
* Interactive web interface
* Frontend-to-backend communication
* Python-based expense processing
* Flask API endpoints for application functionality

## 📂 Project Structure
```text
Expense-Tracker/
│
├── app.py
|── main.py
├── templates/
│   └── index.html
│
├── static/
│   ├── script.js
│   └── style.css
│
└── README.md
```
The exact structure may change as the project continues to be improved.

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone <https://github.com/vikramjitsinghdev/Expense-Tracker>
cd Expense-Tracker
```
### 2. Install Flask
```bash
pip install flask
```
### 3. Start the application
```bash
python app.py
```
### 4. Open the website
Once Flask starts, open the local address provided in the terminal, usually:
```text
http://127.0.0.1:5000
```
## 🎯 What I Learned

This project helped demonstrate several important software-engineering concepts, including:
* Building a web application with Flask
* Connecting a frontend to a Python backend
* Creating and using API endpoints
* Sending data between JavaScript and Python
* Handling user input
* Organizing a project into frontend and backend components
* Working with Git and GitHub
* Debugging communication between different parts of an application

## 🔮 Possible Future Improvements

The current project provides the foundation for a more complete expense-management application. Possible future improvements include:

* Persistent database storage
* User accounts and authentication
* Expense categories
* Monthly and yearly summaries
* Spending charts and visualizations
* Budget tracking
* Exporting expense data
* Improved responsive design
* More advanced filtering and search

## 📚 Project Purpose

This project was developed primarily as a **learning and portfolio project** to gain practical experience in Python web development, APIs, frontend-backend integration, and software organization.

It is intentionally kept manageable in scope while providing a foundation that can be expanded with more advanced features in the future.

## 👨‍💻 Author
**Vikram Jit Singh**
Software Engineering Student
University of New Brunswick
---
> **Note:** This project is intended for educational and portfolio purposes.
