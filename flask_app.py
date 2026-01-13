from flask import Flask, redirect, render_template, request, url_for, flash
from dotenv import load_dotenv
import os
import re
import git
import hmac
import hashlib
from db import db_read, db_write
from auth import login_manager, authenticate, register_user
from flask_login import login_user, logout_user, login_required, current_user
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Load .env variables
load_dotenv()
W_SECRET = os.getenv("W_SECRET")

# Init flask app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# Init auth
login_manager.init_app(app)
login_manager.login_view = "login"

# DON'T CHANGE
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

# DON'T CHANGE
@app.post('/update_server')
def webhook():
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo('./mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    return 'Unauthorized', 401

# Auth routes
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = authenticate(
            request.form["username"],
            request.form["password"]
        )
        if user:
            login_user(user)
            return redirect(url_for("insert_data"))
        error = "Benutzername oder Passwort ist falsch."
    return render_template(
        "auth.html",
        title="In dein Konto einloggen",
        action=url_for("login"),
        button_label="Einloggen",
        error=error,
        footer_text="Noch kein Konto?",
        footer_link_url=url_for("register"),
        footer_link_label="Registrieren"
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ok = register_user(username, password)
        if ok:
            return redirect(url_for("login"))
        error = "Benutzername existiert bereits."
    return render_template(
        "auth.html",
        title="Neues Konto erstellen",
        action=url_for("register"),
        button_label="Registrieren",
        error=error,
        footer_text="Du hast bereits ein Konto?",
        footer_link_url=url_for("login"),
        footer_link_label="Einloggen"
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("insert_data"))

@app.route("/add_post", methods=["POST"])
@login_required
def add_post():
    title = request.form["title"]
    content = request.form["content"]
    sql = """
        INSERT INTO posts (title, content, user_id)
        VALUES (%s, %s, %s)
    """
    params = (title, content, current_user.id)
    db_write(sql, params)
    flash("Post erfolgreich hinzugefügt!", "success")
    return redirect(url_for("insert_data"))

# NEW ROUTE: Add generic data to any table
"""@app.route("/add_data", methods=["POST"])
@login_required
def add_data():
    table = request.form.get("table")
    if not table:
        flash("Keine Tabelle angegeben.", "error")
        return redirect(url_for("insert_data"))
    
    # Get all form data except table and csrf_token
    data = {key: value for key, value in request.form.items() 
            if key not in ["table", "csrf_token"]}
    
    if not data:
        flash("Keine Daten zum Hinzufügen.", "error")
        return redirect(url_for("insert_data"))
    
    # Build SQL query dynamically
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    params = tuple(data.values())
    
    try:
        db_write(sql, params)
        flash(f"Daten erfolgreich zu {table} hinzugefügt!", "success")
    except Exception as e:
        flash(f"Fehler beim Hinzufügen der Daten: {str(e)}", "error")
    
    return redirect(url_for("insert_data"))
"""

@app.route("/")
def insert_data():
    # Fetch existing posts to show on the front page
    sql = "SELECT * FROM posts ORDER BY created_at DESC"
    posts = db_read(sql)
    
    # You can also fetch other tables if needed
    # For example, if you have a 'todos' table:
    # todos = db_read("SELECT * FROM todos ORDER BY created_at DESC")
    
    return render_template("insert_data.html", posts=posts)

@app.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    description = request.form["description"]
    due_date = request.form.get("due_date")  # Optional
    priority = request.form.get("priority", "medium")
    
    sql = """
        INSERT INTO todos (description, due_date, priority, user_id)
        VALUES (%s, %s, %s, %s)
    """
    params = (description, due_date, priority, current_user.id)
    db_write(sql, params)
    flash("Todo erfolgreich hinzugefügt!", "success")
    return redirect(url_for("insert_data"))
#if __name__ == "__main__":
    app.run()



@app.route("/kriminelle", methods=["POST"])
@login_required
def add_kriminelle():
    name = request.form["name"]
    geburtsdatum = request.form["geburtsdatum"]
    rasse = request.form["rasse"]
    haftstatus = 1 if request.form.get("haftstatus") else 0
    geschlecht = request.form["geschlecht"]

    db_write("""
        INSERT INTO kriminelle
        (name, geburtsdatum, rasse, haftstatus, geschlecht)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, geburtsdatum, rasse, haftstatus, geschlecht))

    return redirect(url_for("insert_data"))

@app.route("/verbrechen", methods=["POST"])
@login_required
def add_verbrechen():
    verbrechenstyp = request.form["verbrechenstyp"]
    geldstrafe = request.form["geldstrafe"]
    gefaengniszeit = request.form["gefaengniszeit"]
    vergehen = 1 if request.form.get("vergehen") else 0

    db_write("""
        INSERT INTO verbrechen
        (verbrechenstyp, geldsstrafe, gefängniszeit, vergehen_oder_verbrechen)
        VALUES (%s, %s, %s, %s)
    """, (verbrechenstyp, geldstrafe, gefaengniszeit, vergehen))

@app.route("/gefaengnis", methods=["POST"])
@login_required
def add_gefaengnis():
    ort = request.form["ort"]
    sicherheitslevel = request.form["sicherheitslevel"]

    db_write(
        "INSERT INTO gefaengnis (Ort, Sicherheitslevel) VALUES (%s, %s)",
        (ort, sicherheitslevel)
    )

# ---------------------------
# Generic "insert into any table" page
# ---------------------------

def _row_get(row, key, idx=None):
    """db_read may return dict rows (cursor(dictionary=True)) or tuples; support both."""
    if isinstance(row, dict):
        return row.get(key)
    if idx is not None:
        return row[idx]
    return None

def _quote_ident(name: str) -> str:
    """Safely quote an identifier with backticks (table/column)."""
    return "`" + name.replace("`", "``") + "`"

def _parse_enum_set(column_type: str):
    """
    column_type like: enum('a','b') or set('x','y')
    Returns list of values or None.
    """
    if not column_type:
        return None
    m = re.match(r"^(enum|set)\((.*)\)$", column_type.strip(), flags=re.IGNORECASE)
    if not m:
        return None
    inner = m.group(2)
    vals = re.findall(r"'((?:\\'|[^'])*)'", inner)
    return [v.replace("\\'", "'") for v in vals]

def _list_tables():
    rows = db_read("""
        SELECT TABLE_NAME
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        ORDER BY TABLE_NAME
    """)
    return [_row_get(r, "TABLE_NAME", 0) for r in rows]

def _get_columns(table_name: str):
    rows = db_read("""
        SELECT
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            EXTRA,
            CHARACTER_MAXIMUM_LENGTH
        FROM information_schema.columns
        WHERE table_schema = DATABASE()
          AND table_name = %s
        ORDER BY ORDINAL_POSITION
    """, (table_name,))

    cols = []
    for r in rows:
        col_name = _row_get(r, "COLUMN_NAME", 0)
        data_type = (_row_get(r, "DATA_TYPE", 1) or "").lower()
        column_type = _row_get(r, "COLUMN_TYPE", 2) or ""
        is_nullable = _row_get(r, "IS_NULLABLE", 3) or "YES"
        col_default = _row_get(r, "COLUMN_DEFAULT", 4)
        extra = (_row_get(r, "EXTRA", 5) or "").lower()
        max_len = _row_get(r, "CHARACTER_MAXIMUM_LENGTH", 6)

        # Skip auto-generated columns
        if "auto_increment" in extra or "generated" in extra:
            continue

        # Decide widget/input type
        enum_opts = _parse_enum_set(column_type)
        if enum_opts:
            input_type = "select"
        elif data_type in ("text", "mediumtext", "longtext"):
            input_type = "textarea"
        elif data_type in ("datetime", "timestamp"):
            input_type = "datetime-local"
        elif data_type in ("date",):
            input_type = "date"
        elif data_type in ("time",):
            input_type = "time"
        elif data_type in ("int", "bigint", "smallint", "mediumint", "tinyint", "decimal", "float", "double"):
            # Treat tinyint(1) as checkbox (common MySQL boolean pattern)
            if data_type == "tinyint" and "(1)" in column_type.replace(" ", ""):
                input_type = "checkbox"
            else:
                input_type = "number"
        else:
            input_type = "text"

        required = (is_nullable == "NO" and col_default is None)

        cols.append({
            "name": col_name,
            "data_type": data_type,
            "column_type": column_type,
            "required": required,
            "default": col_default,
            "input_type": input_type,
            "max_len": max_len,
            "enum_options": enum_opts or [],
        })

    return cols

@app.route("/insert_data", methods=["GET", "POST"])
@login_required
def insert_data():
    tables = _list_tables()

    # Which table is selected?
    selected_table = request.args.get("table") if request.method == "GET" else request.form.get("table")
    if selected_table and selected_table not in tables:
        flash("Unbekannte Tabelle.", "error")
        return redirect(url_for("insert_data"))

    columns = _get_columns(selected_table) if selected_table else []

    if request.method == "POST":
        if not selected_table:
            flash("Bitte zuerst eine Tabelle auswählen.", "error")
            return redirect(url_for("insert_data"))

        if not columns:
            flash("Für diese Tabelle wurden keine einfügbaren Spalten gefunden (evtl. nur AUTO_INCREMENT/GENERATED).", "error")
            return redirect(url_for("insert_data", table=selected_table))

        insert_cols = []
        values = []

        for c in columns:
            name = c["name"]
            itype = c["input_type"]

            # Checkboxes submit only when checked
            if itype == "checkbox":
                val = 1 if request.form.get(name) == "on" else 0
            else:
                val = request.form.get(name, "").strip()
                if val == "":
                    val = None

            # Required check
            if c["required"] and val is None:
                flash(f"Feld '{name}' ist erforderlich.", "error")
                return redirect(url_for("insert_data", table=selected_table))

            # Convert datetime-local "YYYY-MM-DDTHH:MM" -> "YYYY-MM-DD HH:MM:SS"
            if val is not None and c["data_type"] in ("datetime", "timestamp"):
                if "T" in val:
                    val = val.replace("T", " ")
                if len(val) == 16:  # no seconds
                    val = val + ":00"

            insert_cols.append(name)
            values.append(val)

        cols_sql = ", ".join(_quote_ident(c) for c in insert_cols)
        placeholders = ", ".join(["%s"] * len(insert_cols))
        sql = f"INSERT INTO {_quote_ident(selected_table)} ({cols_sql}) VALUES ({placeholders})"

        try:
            db_write(sql, tuple(values))
            flash(f"Eintrag in '{selected_table}' gespeichert.", "success")
        except Exception as e:
            logging.exception("Insert failed")
            flash(f"Insert fehlgeschlagen: {e}", "error")

        return redirect(url_for("insert_data", table=selected_table))

    return render_template(
        "insert_data.html",
        tables=tables,
        selected_table=selected_table,
        columns=columns,
    )




if __name__ == "__main__":
    app.run()






