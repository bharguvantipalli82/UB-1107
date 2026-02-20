from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ------------------------------- DATABASE -------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            fever REAL,
            bp INTEGER,
            sugar INTEGER,
            heart_rate INTEGER,
            oxygen INTEGER,
            risk_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------------------- ROUTES -------------------------------

@app.route("/")
def landing():
    return render_template("landing.jinja.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if not email or not password:
            error = "Please enter email and password"
        else:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, name FROM users WHERE email = ? AND password = ?", 
                           (email, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                return redirect(url_for("health"))
            else:
                error = "Invalid email or password"
    return render_template("login.jinja.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    success = ""
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        if not name or not email or not password:
            error = "All fields are required"
        elif password != confirm_password:
            error = "Passwords do not match"
        elif len(password) < 6:
            error = "Password must be at least 6 characters"
        else:
            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                               (name, email, password))
                conn.commit()
                conn.close()
                success = "Registration successful! Please login."
            except sqlite3.IntegrityError:
                error = "Email already exists"
    return render_template("register.jinja.html", error=error, success=success)

@app.route("/google-signin")
def google_signin():
    return redirect(url_for("register"))

@app.route("/health", methods=["GET", "POST"])
def health():
    if request.method == "POST":
        fever = float(request.form["fever"])
        bp = int(request.form["bp"])
        sugar = int(request.form["sugar"])
        heart_rate = int(request.form["heart_rate"])
        oxygen = int(request.form["oxygen"])
        return redirect(url_for("results",
                                fever=fever,
                                bp=bp,
                                sugar=sugar,
                                heart_rate=heart_rate,
                                oxygen=oxygen))
    return render_template("index.jinja.html")

@app.route("/results")
def results():
    fever = float(request.args.get("fever", 0))
    bp = int(request.args.get("bp", 0))
    sugar = int(request.args.get("sugar", 0))
    heart_rate = int(request.args.get("heart_rate", 0))
    oxygen = int(request.args.get("oxygen", 0))
    critical = 0
    moderate = 0
    solutions = []
    doctor = ""
    google_map_link = ""
    fever_condition = "normal"
    bp_condition = "normal"
    sugar_condition = "normal"
    heart_rate_condition = "normal"
    oxygen_condition = "normal"

    # Fever
    if fever > 38.5:
        critical += 1
        fever_condition = "critical"
        solutions.extend([
            " High fever detected - Seek medical help immediately",
            " Monitor your temperature every 2 hours",
            " Take fever-reducing medication as prescribed",
            " Stay hydrated with plenty of fluids",
            " Get adequate rest"
        ])
        doctor = "General Practitioner"
        google_map_link = "https://www.google.com/maps/search/General+Doctor+near+me"
    elif fever > 37.5:
        moderate += 1
        fever_condition = "moderate"
        solutions.extend([
            " Mild fever detected",
            " Monitor your temperature regularly",
            " Take fever-reducing medication if needed",
            " Stay hydrated",
            " Get plenty of rest"
        ])

    # BP
    if bp > 160:
        critical += 1
        bp_condition = "critical"
        solutions.extend([
            " Very high blood pressure - Immediate consultation needed",
            " Avoid salty foods completely",
            " Avoid excessive exercise",
            " Consult a cardiologist immediately",
            " Monitor blood pressure daily"
        ])
        doctor = "Cardiologist"
        google_map_link = "https://www.google.com/maps/search/Cardiologist+near+me"
    elif bp > 140:
        moderate += 1
        bp_condition = "moderate"
        solutions.extend([
            " High blood pressure detected",
            " Reduce salt intake significantly",
            " Exercise moderately",
            " Consult a cardiologist",
            " Monitor blood pressure regularly"
        ])

    # Sugar
    if sugar > 200:
        critical += 1
        sugar_condition = "critical"
        solutions.extend([
            " Very high sugar - Urgent medical attention required",
            " Avoid sugary foods completely",
            " Maintain strict healthy diet",
            " Monitor blood sugar levels frequently",
            " Consult endocrinologist immediately"
        ])
        doctor = "Endocrinologist"
        google_map_link = "https://www.google.com/maps/search/Endocrinologist+near+me"
    elif sugar > 150:
        moderate += 1
        sugar_condition = "moderate"
        solutions.extend([
            " Elevated sugar level detected",
            " Reduce sugary foods",
            " Maintain healthy diet",
            " Monitor blood sugar levels regularly",
            " Consult endocrinologist"
        ])

    # Heart Rate
    if heart_rate > 120:
        critical += 1
        heart_rate_condition = "critical"
        solutions.extend([
            " Very high heart rate - Seek help immediately",
            " Avoid excessive exercise",
            " Practice relaxation techniques",
            " Consult cardiologist immediately",
            " Monitor heart rate continuously"
        ])
        doctor = "Cardiologist"
        google_map_link = "https://www.google.com/maps/search/Cardiologist+near+me"
    elif heart_rate > 100:
        moderate += 1
        heart_rate_condition = "moderate"
        solutions.extend([
            " Slightly high heart rate detected",
            " Reduce physical activity",
            " Practice deep breathing exercises",
            " Consult cardiologist",
            " Monitor heart rate regularly"
        ])

    # Oxygen
    if oxygen < 90:
        critical += 1
        oxygen_condition = "critical"
        solutions.extend([
            " Low oxygen level - Emergency attention needed",
            " Use oxygen supplementation if prescribed",
            " Seek immediate medical attention",
            " Practice breathing exercises",
            " Monitor oxygen saturation continuously"
        ])
        doctor = "Pulmonologist"
        google_map_link = "https://www.google.com/maps/search/Pulmonologist+near+me"
    elif oxygen < 95:
        moderate += 1
        oxygen_condition = "moderate"
        solutions.extend([
            " Slightly low oxygen level detected",
            " Practice deep breathing exercises",
            " Avoid strenuous activities",
            " Monitor oxygen levels regularly",
            " Consult pulmonologist if persists"
        ])

    # Normal conditions - add general health advice
    if critical == 0 and moderate == 0:
        solutions.extend([
            " All vital signs are normal",
            " Stay hydrated throughout the day",
            " Maintain regular exercise routine",
            " Continue healthy balanced diet",
            " Get adequate sleep (7-8 hours)",
            " Schedule regular health checkups"
        ])

    # Risk Decision
    if critical >= 1:
        result = " CRITICAL CONDITION"
        risk_level = "Critical"
    elif moderate >= 2:
        result = " MODERATE CONDITION"
        risk_level = "Moderate"
    else:
        result = " NORMAL CONDITION"
        risk_level = "Normal"

    # ---------------- SAVE TO DATABASE ----------------
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO health_records 
        (fever, bp, sugar, heart_rate, oxygen, risk_level)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fever, bp, sugar, heart_rate, oxygen, risk_level))

    conn.commit()
    conn.close()
    # --------------------------------------------------

    return render_template("result.jinja.html",
                           result=result,
                           doctor=doctor,
                           google_map_link=google_map_link,
                           solutions=solutions,
                           fever=fever,
                           bp=bp,
                           sugar=sugar,
                           heart_rate=heart_rate,
                           oxygen=oxygen,
                           risk_level=risk_level,
                           fever_condition=fever_condition,
                           bp_condition=bp_condition,
                           sugar_condition=sugar_condition,
                           heart_rate_condition=heart_rate_condition,
                           oxygen_condition=oxygen_condition)

if __name__ == "__main__":
    app.run(debug=True)