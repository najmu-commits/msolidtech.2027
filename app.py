
import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def load_env_file():
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()


# =========================================================
# MYSQL DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = int(os.environ.get("DB_PORT", 3306))


def has_db_config():
    return all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME])


def get_db_connection():
    if not has_db_config():
        raise RuntimeError("Database is not configured. Set DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME in the environment or .env file.")

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


# =========================================================
# CREATE DATABASE TABLE
# =========================================================

def create_database():
    if not has_db_config():
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(50),
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


create_database()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("home.html")


# =========================================================
# ABOUT
# =========================================================

@app.route("/About")
def About():
    return render_template("About.html")


# =========================================================
# SERVICES
# =========================================================

@app.route("/Service")
def Service():
    return render_template("Service.html")


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        if not has_db_config():
            return render_template("contact.html", error="Database is not configured yet. Add DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME in your environment or .env file.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO feedback (name, email, phone, message)
            VALUES (%s, %s, %s, %s)
        """, (name, email, phone, message))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("contact"))

    return render_template("contact.html")


# =========================================================
# SOFTWARE DEVELOPMENT
# =========================================================

@app.route("/software")
def software():
    return render_template("software.html")


# =========================================================
# CYBER SECURITY
# =========================================================

@app.route("/cyber-security")
def cyber():
    return render_template("cyber.html")


# =========================================================
# PORTFOLIO
# =========================================================

@app.route("/Portfolio")
def Portfolio():
    return render_template("Portfolio.html")


# =========================================================
# PRIVACY POLICY
# =========================================================

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# =========================================================
# TERMS
# =========================================================

@app.route("/terms")
def terms():
    return render_template("terms.html")


# =========================================================
# AI
# =========================================================

@app.route("/tai")
def ai():
    return render_template("ai.html")


# =========================================================
# FEEDBACK / ADMIN PAGE
# =========================================================

@app.route("/feedback")
def feedback():

    if not has_db_config():
        return render_template("feedback.html", feedbacks=[])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, phone, message
        FROM feedback
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "feedback.html",
        feedbacks=data
    )


# =========================================================
# RUN APPLICATION LOCALLY
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
