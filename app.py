from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"
DB = "database.db"

def get_db():
    return sqlite3.connect(DB)

# ---------- DB INIT ----------
def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
        """)
        db.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            status TEXT
        )
        """)
init_db()

# ---------- HTML ----------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Consent App</title>
<style>
body { font-family: Arial; background:#eef2f7; }
.card {
    background:white;
    padding:20px;
    margin:15px auto;
    width:350px;
    border-radius:10px;
    box-shadow:0 5px 15px rgba(0,0,0,.2);
}
button {
    padding:8px 14px;
    border:none;
    border-radius:6px;
    cursor:pointer;
}
.login { background:#007bff; color:white; }
.logout { background:#dc3545; color:white; }
.request { background:#28a745; color:white; }
.accept { background:#28a745; color:white; }
.reject { background:#dc3545; color:white; }
</style>
</head>
<body>

<div class="card">
{% if not user %}
<form method="post">
<input type="hidden" name="action" value="login">
<input name="username" placeholder="Your name" required>
<br><br>
<button class="login">Login</button>
</form>
{% else %}
<h3>Welcome {{ user }}</h3>
<form method="post">
<input type="hidden" name="action" value="logout">
<button class="logout">Logout</button>
</form>
{% endif %}
</div>

{% if user %}

<h3 style="text-align:center;">People</h3>
{% for u in users %}
<div class="card">
<b>{{ u }}</b><br><br>
<form method="post">
<input type="hidden" name="action" value="request">
<input type="hidden" name="receiver" value="{{ u }}">
<button class="request">Request Contact</button>
</form>
</div>
{% endfor %}

<h3 style="text-align:center;">Incoming Requests</h3>
{% for r in incoming %}
<div class="card">
<b>{{ r[0] }}</b> wants your contact<br><br>
<form method="post" style="display:inline;">
<input type="hidden" name="action" value="accept">
<input type="hidden" name="req_id" value="{{ r[1] }}">
<button class="accept">Accept</button>
</form>
<form method="post" style="display:inline;">
<input type="hidden" name="action" value="reject">
<input type="hidden" name="req_id" value="{{ r[1] }}">
<button class="reject">Reject</button>
</form>
</div>
{% endfor %}

<h3 style="text-align:center;">Accepted</h3>
{% for a in accepted %}
<div class="card">
<b>{{ a }}</b> 📞 +254700000000
</div>
{% endfor %}

{% endif %}
</body>
</html>
"""

CURRENT_USER = None

# ---------- ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def home():
    global CURRENT_USER
    db = get_db()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            username = request.form.get("username")
            db.execute("INSERT OR IGNORE INTO users(username) VALUES(?)", (username,))
            db.commit()
            CURRENT_USER = username

        elif action == "logout":
            CURRENT_USER = None

        elif action == "request":
            receiver = request.form.get("receiver")
            db.execute(
                "INSERT INTO requests(sender, receiver, status) VALUES(?,?,?)",
                (CURRENT_USER, receiver, "pending")
            )
            db.commit()

        elif action == "accept":
            req_id = request.form.get("req_id")
            db.execute("UPDATE requests SET status='accepted' WHERE id=?", (req_id,))
            db.commit()

        elif action == "reject":
            req_id = request.form.get("req_id")
            db.execute("UPDATE requests SET status='rejected' WHERE id=?", (req_id,))
            db.commit()

        return redirect(url_for("home"))

    users = [u[0] for u in db.execute("SELECT username FROM users").fetchall() if u[0] != CURRENT_USER]

    incoming = db.execute(
        "SELECT sender, id FROM requests WHERE receiver=? AND status='pending'",
        (CURRENT_USER,)
    ).fetchall()

    accepted = [r[0] for r in db.execute(
        "SELECT receiver FROM requests WHERE sender=? AND status='accepted'",
        (CURRENT_USER,)
    ).fetchall()]

    return render_template_string(
        HTML,
        user=CURRENT_USER,
        users=users,
        incoming=incoming,
        accepted=accepted
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

