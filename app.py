import email

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Secret key for session
app.secret_key = os.getenv("SECRET_KEY")


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection

# ---------------- HOME ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if not username.strip() or not email.strip() or not password:
         return "All fields are required!"

        if len(username.strip()) < 3:
         return "Username must contain at least 3 characters!"

        if len(password) < 6:
         return "Password must contain at least 6 characters!"

        if "@" not in email or "." not in email:
         return "Please enter a valid email address!"

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check existing email
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return "Email already registered!"

        # Hash password
        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            """,
            (username, email, hashed_password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Total reports
    cursor.execute("SELECT COUNT(*) AS total FROM threat_reports")
    total_reports = cursor.fetchone()["total"]

    # Open threats
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM threat_reports
        WHERE status = 'Open'
    """)
    open_threats = cursor.fetchone()["total"]

    # Critical threats
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM threat_reports
        WHERE severity = 'Critical'
    """)
    critical_threats = cursor.fetchone()["total"]

    # Resolved threats
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM threat_reports
        WHERE status = 'Resolved'
    """)
    resolved_threats = cursor.fetchone()["total"]

    # Threats by severity
    cursor.execute("""
        SELECT severity, COUNT(*) AS total
        FROM threat_reports
        GROUP BY severity
    """)
    severity_data = cursor.fetchall()

    # Recent reports
    cursor.execute("""
        SELECT *
        FROM threat_reports
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_reports = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_reports=total_reports,
        open_threats=open_threats,
        critical_threats=critical_threats,
        resolved_threats=resolved_threats,
        severity_data=severity_data,
        recent_reports=recent_reports
    )
# ---------------- THREAT REPORTS ----------------

@app.route("/threats")
def threats():
    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    severity = request.args.get("severity", "").strip()
    status = request.args.get("status", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM threat_reports
        WHERE 1=1
    """

    params = []

    if search:
        query += """
            AND (
                title LIKE %s
                OR description LIKE %s
                OR threat_type LIKE %s
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value
        ])

    if severity:
        query += " AND severity = %s"
        params.append(severity)

    if status:
        query += " AND status = %s"
        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, tuple(params))

    reports = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "threats.html",
        reports=reports,
        search=search,
        selected_severity=severity,
        selected_status=status
    )

# ---------------- ADD THREAT ----------------

@app.route("/threats/add", methods=["GET", "POST"])
def add_threat():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"].strip()
        description = request.form["description"].strip()
        threat_type = request.form["threat_type"].strip()
        severity = request.form["severity"].strip()
        status = request.form["status"].strip()
        source = request.form["source"].strip()

        # Required field validation
        if not title or not description or not threat_type:
            return "Please fill all required fields!"

        # Title validation
        if len(title) < 3:
            return "Threat title must contain at least 3 characters!"

        # Description validation
        if len(description) < 10:
            return "Description must contain at least 10 characters!"

        # Allowed values
        allowed_threat_types = [
            "Phishing",
            "Malware",
            "Ransomware",
            "SQL Injection",
            "DDoS",
            "Brute Force",
            "Data Breach",
            "Other"
        ]

        allowed_severity = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

        allowed_status = [
            "Open",
            "Investigating",
            "Resolved"
        ]

        # Threat type validation
        if threat_type not in allowed_threat_types:
            return "Invalid threat type!"

        # Severity validation
        if severity not in allowed_severity:
            return "Invalid severity value!"

        # Status validation
        if status not in allowed_status:
            return "Invalid status value!"

        # Database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO threat_reports
            (
                title,
                description,
                threat_type,
                severity,
                status,
                reported_by,
                source
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            title,
            description,
            threat_type,
            severity,
            status,
            session["username"],
            source
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("threats"))

    return render_template("add_threat.html")

# ---------------- EDIT THREAT ----------------

@app.route("/threats/edit/<int:report_id>", methods=["GET", "POST"])
def edit_threat(report_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # UPDATE
    if request.method == "POST":

        title = request.form["title"].strip()
        description = request.form["description"].strip()
        threat_type = request.form["threat_type"].strip()
        severity = request.form["severity"].strip()
        status = request.form["status"].strip()
        source = request.form["source"].strip()

        # Required field validation
        if not title or not description or not threat_type:

            cursor.close()
            connection.close()

            return "Please fill all required fields!"

        # Title validation
        if len(title) < 3:

            cursor.close()
            connection.close()

            return "Threat title must contain at least 3 characters!"

        # Description validation
        if len(description) < 10:

            cursor.close()
            connection.close()

            return "Description must contain at least 10 characters!"

        # Allowed values
        allowed_threat_types = [
            "Phishing",
            "Malware",
            "Ransomware",
            "SQL Injection",
            "DDoS",
            "Brute Force",
            "Data Breach",
            "Other"
        ]

        allowed_severity = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

        allowed_status = [
            "Open",
            "Investigating",
            "Resolved"
        ]

        # Threat type validation
        if threat_type not in allowed_threat_types:

            cursor.close()
            connection.close()

            return "Invalid threat type!"

        # Severity validation
        if severity not in allowed_severity:

            cursor.close()
            connection.close()

            return "Invalid severity value!"

        # Status validation
        if status not in allowed_status:

            cursor.close()
            connection.close()

            return "Invalid status value!"

        # Update database
        cursor.execute("""
            UPDATE threat_reports
            SET
                title = %s,
                description = %s,
                threat_type = %s,
                severity = %s,
                status = %s,
                source = %s
            WHERE id = %s
        """, (
            title,
            description,
            threat_type,
            severity,
            status,
            source,
            report_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("threats"))

    # GET - Fetch existing report
    cursor.execute(
        "SELECT * FROM threat_reports WHERE id = %s",
        (report_id,)
    )

    report = cursor.fetchone()

    cursor.close()
    connection.close()

    if not report:
        return "Threat report not found!"

    return render_template(
        "edit_threat.html",
        report=report
    )

# ---------------- DELETE THREAT ----------------

@app.route("/threats/delete/<int:report_id>")
def delete_threat(report_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM threat_reports WHERE id = %s",
        (report_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("threats"))

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)