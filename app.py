# Flask application for the Expense Tracker.
# Connects the HTML/JavaScript frontend to
# the Python backend and SQLite database.
from flask import (Flask,render_template,request,jsonify,session)
from datetime import datetime
#Import the Decimal library for data verification
from decimal import Decimal, InvalidOperation
import sqlite3
import os
# ============================================================
# FLASK APPLICATION
# ============================================================
app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY"
)
# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DATABASE = "expenses.db"
def get_db_connection():
    """
    Create and return a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE)
    # Allows database rows to be accessed using column names.
    connection.row_factory = sqlite3.Row
    return connection
def init_db():
    connection = get_db_connection()
    connection.execute("""
        PRAGMA foreign_keys = ON
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            total_budget REAL NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            unit_cost REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            payment TEXT NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)
    connection.commit()
    connection.close()
# ============================================================
# HOME ROUTE
# ============================================================
@app.route("/")
def home():
    """
    Display the main HTML application.
    """
    return render_template("index.html")
# ============================================================
# CONSTANTS
# ============================================================
PAYMENT_METHODS = [
    "credit",
    "debit",
    "cash",
    "other"
]
MAX_UNIT_COST = Decimal("1000000")
MAX_QUANTITY = 100000
MAX_BUDGET = Decimal("1000000000")
# ============================================================
# VALIDATION FUNCTIONS
# ============================================================
def validate_expense_data(data):
    """
    Validate and clean expense data received
    from the frontend.
    Returns:
        Dictionary containing validated data.
    Raises:
        ValueError if any input is invalid.
    """
    # --------------------------------------------------------
    # Make sure data exists
    # --------------------------------------------------------
    if not isinstance(data, dict):
        raise ValueError("Invalid request data.")
    # --------------------------------------------------------
    # Validate description
    # --------------------------------------------------------
    description = str(data.get("description", "")).strip()
    if not description:
        raise ValueError("Description cannot be empty.")
    # --------------------------------------------------------
    # Validate unit cost
    # --------------------------------------------------------
    unit_cost = data.get("unit_cost")
    if unit_cost is None:
        raise ValueError("Cost is required.")
    unit_cost_text = str(unit_cost).strip()
    # Prevent scientific notation.
    if "e" in unit_cost_text.lower():
        raise ValueError("Scientific notation is not allowed.")
    try:
        unit_cost = Decimal(unit_cost_text)
    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):
        raise ValueError("Cost must be a valid number.")
    # Reject NaN and Infinity.
    if not unit_cost.is_finite():
        raise ValueError("Cost must be a finite number.")
    # Cost must be positive.
    if unit_cost <= 0:
        raise ValueError("Cost must be greater than 0.")
    # Prevent absurdly large values.
    if unit_cost > MAX_UNIT_COST:
        raise ValueError("Cost is too large.")
    # --------------------------------------------------------
    # Validate category
    # --------------------------------------------------------
    category = str(data.get("category", "")).strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    if not category.replace(" ", "").isalpha():
        raise ValueError("Category must contain letters and spaces only.")
    # --------------------------------------------------------
    # Validate date
    # --------------------------------------------------------
    date = str(data.get("date", "")).strip()
    if not date:
        raise ValueError("Date cannot be empty.")
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date. Please use YYYY-MM-DD.")
    # --------------------------------------------------------
    # Validate payment method
    # --------------------------------------------------------
    payment = str(data.get("payment", "")).strip().lower()
    if payment not in PAYMENT_METHODS:
        raise ValueError(
            "Invalid payment method. "
            "Please enter credit, debit, cash, or other."
        )
    # --------------------------------------------------------
    # Validate quantity
    # --------------------------------------------------------
    amount_raw = data.get("amount")
    try:
        # Prevent values such as 2.5 from
        # accidentally being treated as 2.
        amount_text = str(amount_raw).strip()
        if not amount_text.isdigit():
            raise ValueError
        amount = int(amount_text)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a whole number.")
    if amount < 1:
        raise ValueError("Quantity must be at least 1.")
    if amount > MAX_QUANTITY:
        raise ValueError("Quantity is too large.")
    # --------------------------------------------------------
    # Return cleaned data
    # --------------------------------------------------------
    return {
        "description": description,
        "unit_cost": unit_cost,
        "category": category,
        "amount": amount,
        "date": date,
        "payment": payment
    }
# ============================================================
# DATABASE → JSON CONVERSION
# ============================================================
def expense_row_to_dict(row):
    """
    Convert a SQLite expense row into a dictionary
    suitable for the frontend.
    """
    unit_cost = float(row["unit_cost"])
    quantity = int(row["quantity"])
    total_cost = unit_cost * quantity
    return {
        "id": row["id"],
        "description": row["description"],
        "cost": total_cost,
        "unit_cost": unit_cost,
        "amount": quantity,
        "category": row["category"],
        "date": row["date"],
        "payment": row["payment"]
    }
def expenses_for_json(rows):
    """
    Convert multiple SQLite rows into JSON-compatible
    dictionaries.
    """
    return [
        expense_row_to_dict(row)
        for row in rows
    ]
# ===========================================================
# EXPENSE DATABASE FUNCTIONS
# ============================================================
def add_expense(data, user_id):
    validated = validate_expense_data(data)
    connection = get_db_connection()
    cursor = connection.execute("""
        INSERT INTO expenses (
            user_id,
            description,
            unit_cost,
            quantity,
            category,
            date,
            payment
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        validated["description"],
        float(validated["unit_cost"]),
        validated["amount"],
        validated["category"],
        validated["date"],
        validated["payment"]
    ))
    connection.commit()
    expense_id = cursor.lastrowid
    row = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    connection.close()
    return expense_row_to_dict(row)
def search_by_id(expense_id, user_id):
    connection = get_db_connection()
    row = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    connection.close()
    return row
def search_by_date(date, user_id):
    connection = get_db_connection()
    rows = connection.execute("""
        SELECT *
        FROM expenses
        WHERE date = ?
        AND user_id = ?
        ORDER BY id
    """, (date,user_id)).fetchall()
    connection.close()
    return rows
def edit_expense(expense_id,data,user_id):
    validated = validate_expense_data(data)
    connection = get_db_connection()
    existing = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    if existing is None:
        connection.close()
        raise ValueError("Expense not found.")
    connection.execute("""
        UPDATE expenses
        SET
            description = ?,
            unit_cost = ?,
            quantity = ?,
            category = ?,
            date = ?,
            payment = ?
        WHERE id = ?
        AND user_id = ?
    """, (
        validated["description"],
        float(validated["unit_cost"]),
        validated["amount"],
        validated["category"],
        validated["date"],
        validated["payment"],
        expense_id,
        user_id
    ))
    connection.commit()
    updated = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    connection.close()
    return expense_row_to_dict(updated)
def delete_expense(expense_id,user_id):
    """
    Delete an expense from SQLite.
    """
    connection = get_db_connection()
    # Retrieve the expense before deleting it.
    row = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    if row is None:
        connection.close()
        raise ValueError("Expense not found.")
    deleted_expense = expense_row_to_dict(row)
    connection.execute("""
        DELETE FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,))
    connection.commit()
    connection.close()
    return deleted_expense
# ============================================================
# BUDGET FUNCTIONS
# ============================================================
def get_tracker():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    connection = get_db_connection()
    row = connection.execute("""
        SELECT
            id,
            name,
            total_budget
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()
    connection.close()
    return row
def save_tracker(name, budget):
    connection = get_db_connection()
    user = connection.execute("""
        SELECT id
        FROM users
        WHERE name = ?
    """, (name,)).fetchone()
    if user is None:
        cursor = connection.execute("""
            INSERT INTO users (
                name,
                total_budget
            )
            VALUES (?, ?)
        """, (
            name,
            float(budget)
        ))
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]
        connection.execute("""
        UPDATE users
        SET total_budget = ?
        WHERE id = ?
    """, (
        float(budget),
        user_id
    ))
    connection.commit()
    connection.close()
    return user_id
def calculate_total_spent(user_id):
    connection = get_db_connection()
    result = connection.execute("""
        SELECT
            COALESCE(
                SUM(unit_cost * quantity),
                0
            ) AS total_spent
        FROM expenses
        WHERE user_id = ?
    """, (user_id,)).fetchone()
    connection.close()
    return float(result["total_spent"])
def get_budget_summary():
    tracker = get_tracker()
    if tracker is None:
        return {
            "total_budget": 0.0,
            "total_spent": 0.0,
            "remaining_budget": 0.0,
            "over_budget": False
        }
    user_id = tracker["id"]
    total_budget = float(tracker["total_budget"])
    total_spent = calculate_total_spent(user_id)
    remaining_budget = (total_budget - total_spent)
    return {
        "total_budget":
            total_budget,
        "total_spent":
            total_spent,
        "remaining_budget":
            remaining_budget,
        "over_budget":
            remaining_budget < 0
    }
# ============================================================
# API — START TRACKER
# ============================================================
@app.route("/api/start", methods=["POST"])
def start_tracker():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid request data."
            }), 400
        # ----------------------------------------------------
        # Validate name
        # ----------------------------------------------------
        name = str(data.get("name", "")).strip()
        if not name:
            return jsonify({
                "error": "Please enter your name."
            }), 400
        # ----------------------------------------------------
        # Validate budget
        # ----------------------------------------------------
        budget_raw = data.get("budget")
        if budget_raw is None:
            return jsonify({
                "error": "Please enter a budget."
            }), 400
        budget_text = str(budget_raw).strip()
        # Prevent scientific notation
        if "e" in budget_text.lower():
            return jsonify({
                "error":"Scientific notation is not allowed."
            }), 400
        try:
            budget = Decimal(budget_text)
        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):
            return jsonify({
                "error":"Please enter a valid budget."
            }), 400
        # Reject NaN / Infinity
        if not budget.is_finite():
            return jsonify({
                "error":"Budget must be a finite number."
            }), 400
        # Budget must be positive
        if budget <= 0:
            return jsonify({
                "error":"Budget must be greater than 0."
            }), 400
        # Maximum budget
        if budget > MAX_BUDGET:
            return jsonify({
                "error":"Budget is too large."
            }), 400
        # ----------------------------------------------------
        # Save user
        # ----------------------------------------------------
        user_id = save_tracker(
            name,
            budget
        )
        # Store current user in Flask session
        session["user_id"] = user_id
        session["user_name"] = name
        # ----------------------------------------------------
        # SUCCESS RESPONSE
        # ----------------------------------------------------
        return jsonify({
            "message":
                "Tracker started successfully.",
            "name":
                name,
            "budget":
                float(budget)
        })
    except Exception as error:
        print(
            "START TRACKER ERROR:",
            error
        )
        return jsonify({
            "error":
                "An internal server error occurred."
        }), 500
# ============================================================
# API — GET ALL EXPENSES
# ============================================================
@app.route("/api/expenses",methods=["GET"])
def get_expenses():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    connection = get_db_connection()
    rows = connection.execute("""
        SELECT *
        FROM expenses
        WHERE user_id = ?
        ORDER BY id
    """, (user_id,)).fetchall()
    connection.close()
    return jsonify(expenses_for_json(rows))
# ============================================================
# API — ADD EXPENSE
# ============================================================
@app.route("/api/expenses",methods=["POST"])
def create_expense():
    try:
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({
                "error":"Please start the tracker first."}), 401
        data = request.get_json()
        expense = add_expense(data,user_id)
        return jsonify(expense), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500
# ============================================================
# API — GET ONE EXPENSE
# ============================================================
@app.route("/api/expenses/<int:expense_id>",methods=["GET"])
def get_one_expense(expense_id):
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    connection = get_db_connection()
    row = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id,user_id)).fetchone()
    connection.close()
    if row is None:
        return jsonify({
            "error":"Expense not found."
        }), 404
    return jsonify(expense_row_to_dict(row))
# ============================================================
# API — SEARCH BY DATE
# ============================================================
@app.route("/api/expenses/date/<date>",methods=["GET"])
def get_expenses_by_date(date):
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        return jsonify({
            "error":"Invalid date. Please use YYYY-MM-DD."
        }), 400
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    rows = search_by_date(date,user_id)
    return jsonify(expenses_for_json(rows))
# ============================================================
# API — EDIT EXPENSE
# ============================================================
@app.route("/api/expenses/<int:expense_id>",methods=["PUT"])
def update_expense(expense_id):
    try:
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({
                "error":"Please start the tracker first."
            }), 401
        data = request.get_json()
        updated_expense = edit_expense(
            expense_id,
            data,
            user_id
        )
        return jsonify(updated_expense)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500
# ============================================================
# API — DELETE EXPENSE
# ============================================================
@app.route(
    "/api/expenses/<int:expense_id>",
    methods=["DELETE"]
)
def remove_expense(expense_id):
    try:
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({
                "error":"Please start the tracker first."
            }), 401
        deleted_expense = delete_expense(expense_id,user_id)
        return jsonify({
            "message":"Expense deleted successfully.",
            "expense":deleted_expense
        })
    except ValueError as error:
        return jsonify({"error": str(error)}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500
# ============================================================
# API — SORT BY DATE
# ============================================================
@app.route("/api/expenses/sort/date",methods=["GET"])
def sort_expenses_by_date():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    connection = get_db_connection()
    rows = connection.execute("""
        SELECT *
        FROM expenses
        WHERE user_id = ?
        ORDER BY date ASC
    """, (user_id,)).fetchall()
    connection.close()
    return jsonify(expenses_for_json(rows))
# ============================================================
# API — SORT BY ID
# ============================================================
@app.route("/api/expenses/sort/id",methods=["GET"])
def sort_expenses_by_id():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    connection = get_db_connection()
    rows = connection.execute("""
        SELECT *
        FROM expenses
        WHERE user_id = ?
        ORDER BY id ASC
    """, (user_id,)).fetchall()
    connection.close()
    return jsonify(expenses_for_json(rows))
# ============================================================
# API — BUDGET SUMMARY
# ============================================================
@app.route("/api/budget",methods=["GET"])
def budget_summary():
    summary = get_budget_summary()
    return jsonify(summary)
# ============================================================
# API — ITEMS VIEW
# ============================================================
@app.route(
    "/api/items",
    methods=["GET"]
)
def get_items():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({
            "error":"Please start the tracker first."
        }), 401
    connection = get_db_connection()
    rows = connection.execute("""
        SELECT
            description,
            unit_cost,
            date,
            quantity
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,)).fetchall()
    connection.close()
    items = []
    for row in rows:
        items.append({
            "item":row["description"],
            "unit_cost":float(row["unit_cost"]),
            "date":row["date"],
            "quantity":row["quantity"]
        })
    return jsonify(items)
# used to create a line chart for the users
@app.route("/api/chart-data", methods=["GET"])
def get_chart_data():

    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({
            "error": "Please start the tracker first."
        }), 401

    connection = get_db_connection()

    rows = connection.execute("""
        SELECT
            id,
            date,
            description,
            unit_cost,
            quantity,
            (unit_cost * quantity) AS total
        FROM expenses
        WHERE user_id = ?
        ORDER BY date ASC, id ASC
    """, (user_id,)).fetchall()

    user = connection.execute("""
        SELECT total_budget
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    connection.close()

    expenses_data = []

    for row in rows:
        expenses_data.append({
            "id": row["id"],
            "date": row["date"],
            "description": row["description"],
            "total": float(row["total"])
        })

    return jsonify({
        "budget": float(user["total_budget"]),
        "expenses": expenses_data
    })
@app.route("/api/budget/add",methods=["POST"])
def add_budget():
    try:
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({
                "error":"Please start the tracker first."
            }), 401
        data = request.get_json()
        amount_raw = data.get("amount")
        if amount_raw is None:
            return jsonify({
                "error":"Please enter an amount."
            }), 400
        amount_text = str(amount_raw).strip()
        if "e" in amount_text.lower():
            return jsonify({
                "error":"Scientific notation is not allowed."
            }), 400
        try:
            amount = Decimal(amount_text)
        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):
            return jsonify({
                "error":"Please enter a valid amount."
            }), 400
        if not amount.is_finite():
            return jsonify({
                "error":"Amount must be finite."
            }), 400
        if amount <= 0:
            return jsonify({
                "error":"Amount must be greater than 0."
            }), 400
        connection = get_db_connection()
        connection.execute("""
            UPDATE users
            SET total_budget = total_budget + ?
            WHERE id = ?
        """, (float(amount),user_id))
        connection.commit()
        user = connection.execute("""
                SELECT total_budget
                FROM users
                WHERE id = ?
            """, (user_id,)).fetchone()
        connection.close()
        return jsonify({
            "message":
                "Budget increased successfully.",
            "total_budget":
                float(user["total_budget"])
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500
# ============================================================
# START APPLICATION
# ============================================================
if __name__ == "__main__":
    # Create database/tables before
    # starting Flask.
    init_db()
    app.run(debug=True)