import sqlite3
from flask import Flask, render_template, request, redirect, session
import joblib
from features import extract_features  # Step 4.2 function

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- TEMP DATA ----------------
users = {}          # { email : password }
history_data = []   # history list

# ---------------- LOAD ML MODEL ----------------
model = joblib.load("url_model.pkl")


# ---------------- INDEX ----------------
@app.route('/')
def index():
    return redirect('/login')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # ---------------- DB CHECK ----------------
        import sqlite3
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Check if user exists with email and password
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect('/home')
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        import sqlite3
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "User already exists"
        else:
            # Insert new user into database
            cursor.execute("""
            INSERT INTO users (name, email, password, notifications, dark_mode)
            VALUES (?, ?, ?, 1, 0)
            """, (name, email, password))
            conn.commit()
            conn.close()
            return redirect('/login')

        conn.close()

    return render_template('register.html', error=error)

# ---------------- HOME ----------------
@app.route('/home')
def home():

    if 'user' not in session:
        return redirect('/login')

    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dark_mode FROM users WHERE email=?", (session['user'],))
    dark = cursor.fetchone()[0]

    conn.close()

    return render_template('home.html', dark=dark)


# ---------------- CHECK ----------------
@app.route('/check', methods=['GET', 'POST'])
def check():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        url = request.form.get('website_url')

        if not url:
            return render_template('check.html', error="Please enter a URL")

        # ---------------- ML PREDICTION ----------------
        features = extract_features(url)
        X = [list(features.values())]  # convert to list for model
        pred = model.predict(X)[0]     # 0 = safe, 1 = phishing

        analysis = {
            "Website": url,
            "Risk": "HIGH" if pred == 1 else "LOW",
            "Scam": "Yes" if pred == 1 else "No",
            "Suspicious_keywords": "Found" if features["suspicious_words"] > 0 else "None",
            "Payment_safe": "No" if pred == 1 else "Yes"
        }

        # ---------------- Step 2.4: Check repeated malicious URL ----------------
        existing = [h for h in history_data if h["site"] == url and h["risk"] == "HIGH"]
        if existing:
            analysis["Notification"] = "⚠️ This site was previously flagged as malicious!"
        else:
            analysis["Notification"] = ""
        
        

        # Save to session and history
        session['analysis'] = analysis
        import sqlite3
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user, site, risk) VALUES (?, ?, ?)",
               (session['user'], url, analysis["Risk"]))
        conn.commit()
        conn.close()

        return redirect('/result')

    return render_template('check.html')


@app.route('/dashboard')
def dashboard():
    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM history WHERE risk='LOW'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM history WHERE risk='HIGH'")
    malicious = cursor.fetchone()[0]

    cursor.execute("""
        SELECT site, COUNT(*) as c FROM history 
        WHERE risk='HIGH'
        GROUP BY site ORDER BY c DESC LIMIT 5
    """)
    top_urls = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', total=total, safe=safe, malicious=malicious, top_urls=top_urls)
# ---------------- HISTORY ----------------
@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Fetch history for logged-in user
    cursor.execute("SELECT site, risk, date FROM history WHERE user=? ORDER BY date DESC",
                   (session['user'],))
    history_data = cursor.fetchall()
    conn.close()

    return render_template('history.html', history=history_data)


# ---------------- PROFILE ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'user' not in session:
        return redirect('/login')

    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Get current user details first
    cursor.execute("SELECT id, name, email, notifications, dark_mode FROM users WHERE email=?", (session['user'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        notifications = 1 if request.form.get('notifications') else 0
        dark_mode = 1 if request.form.get('dark_mode') else 0

        user_id = user[0]   # get ID

        cursor.execute("""
        UPDATE users
        SET name=?, email=?, notifications=?, dark_mode=?
        WHERE id=?
        """, (name, email, notifications, dark_mode, user_id))

        conn.commit()

        # update session if email changed
        session['user'] = email

        return redirect('/profile?updated=1')  # IMPORTANT

    conn.close()


    user_data = {
        "name": user[1],
        "email": user[2],
        "notifications": bool(user[3]),
        "dark_mode": bool(user[4])
    }

    return render_template('profile.html', user=user_data, dark=user_data["dark_mode"])
# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from your extension

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get("website_url") if data else None
    if not url:
        return {"error":"No URL provided"}, 400

    # ML prediction code
    features = extract_features(url)
    X = [list(features.values())]
    pred = model.predict(X)[0]  # 0 = safe, 1 = phishing

    analysis = {
        "Website": url,
        "Risk": "HIGH" if pred==1 else "LOW",
        "Scam": "Yes" if pred==1 else "No",
        "Suspicious_keywords": "Found" if features["suspicious_words"] > 0 else "None",
        "Payment_safe": "No" if pred==1 else "Yes"
    }

    return analysis

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)

import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", [table[0] for table in tables])

conn.close()