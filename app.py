from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response
)

import sqlite3
import random
import csv
import io
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "agrisetu_secret_key"

DATABASE = "database.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def fetch_all(query, values=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, values)
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_one(query, values=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, values)
    row = cur.fetchone()
    conn.close()
    return row


def execute_query(query, values=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():

    conn = get_db()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # FARMERS
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,
        mobile TEXT NOT NULL,

        age INTEGER,
        gender TEXT,

        aadhaar TEXT,

        village TEXT NOT NULL,
        district TEXT NOT NULL,

        land REAL NOT NULL,
        crop TEXT NOT NULL,

        subsidy TEXT NOT NULL,

        eligible INTEGER NOT NULL,
        issued INTEGER DEFAULT 0,
        balance INTEGER NOT NULL,

        status TEXT DEFAULT 'Pending',

        latitude REAL,
        longitude REAL,

        bank TEXT,
        account TEXT,
        ifsc TEXT
    )
    """)

    # ------------------------------------------------------
    # HISTORY
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        farmer_id INTEGER,

        quantity INTEGER,

        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(farmer_id)
        REFERENCES farmers(id)
    )
    """)

    # ------------------------------------------------------
    # INVENTORY
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        item TEXT UNIQUE,

        quantity INTEGER
    )
    """)

    # ------------------------------------------------------
    # DEFAULT INVENTORY
    # ------------------------------------------------------

    count = cursor.execute(
        "SELECT COUNT(*) FROM inventory"
    ).fetchone()[0]

    if count == 0:

        inventory = [

            ("Rice Seeds",5000),
            ("Wheat Seeds",4500),
            ("DAP Fertilizer",4200),
            ("Urea",4600),
            ("Organic Fertilizer",3500),
            ("Pesticide",3000),
            ("Sprayer",800),
            ("Drip Kit",600),
            ("Water Pump",400),
            ("Tractor Subsidy",150)

        ]

        cursor.executemany(
            """
            INSERT INTO inventory(
                item,
                quantity
            )
            VALUES(?,?)
            """,
            inventory
        )

    farmer_count = cursor.execute(
        "SELECT COUNT(*) FROM farmers"
    ).fetchone()[0]

    if farmer_count == 0:

        names = [
            "Arun","Ajith","Kumar","Ramesh","Suresh",
            "Ganesh","Hari","Prakash","Dinesh","Rahul",
            "Saravanan","Mohan","Karthik","Vijay","Gokul",
            "Lakshmi","Priya","Divya","Meena","Nisha",
            "Ramya","Revathi","Monika","Anitha","Swathi",
            "Deepa","Bhavani","Janani","Sneha","Kavya"
        ]

        villages = [
            "Tambaram","Chromepet","Pallavaram",
            "Madipakkam","Velachery","Sholinganallur",
            "Kelambakkam","Guduvanchery","Vandalur",
            "Perungalathur","Medavakkam","Navalur",
            "Siruseri","Porur","Ambattur",
            "Avadi","Poonamallee","Anna Nagar",
            "T Nagar","Mylapore","Adyar",
            "Nanganallur","Selaiyur",
            "Mudichur","Padur",
            "Thaiyur","Karanai",
            "Semmenchery","Sembakkam"
        ]       
        districts = [

            "Chennai",
            "Chengalpattu",
            "Kanchipuram",
            "Thiruvallur",
            "Vellore",
            "Salem",
            "Erode",
            "Madurai",
            "Trichy",
            "Coimbatore",
            "Thanjavur",
            "Nagapattinam",
            "Villupuram",
            "Cuddalore",
            "Dharmapuri",
            "Krishnagiri",
            "Tirunelveli",
            "Thoothukudi",
            "Namakkal",
            "Karur"

        ]

        crops = [

            "Rice",
            "Wheat",
            "Sugarcane",
            "Cotton",
            "Groundnut",
            "Banana",
            "Millets",
            "Turmeric",
            "Maize",
            "Coconut",
            "Onion",
            "Tomato",
            "Brinjal",
            "Chilli",
            "Mango"

        ]

        subsidies = [

            "Rice Seeds",
            "Wheat Seeds",
            "DAP Fertilizer",
            "Urea",
            "Organic Fertilizer",
            "Pesticide",
            "Sprayer",
            "Drip Kit",
            "Water Pump",
            "Tractor Subsidy"

        ]

        banks = [

            "State Bank of India",
            "Indian Bank",
            "Canara Bank",
            "Bank of Baroda",
            "Punjab National Bank",
            "Indian Overseas Bank",
            "Union Bank of India",
            "HDFC Bank",
            "ICICI Bank",
            "Axis Bank"

        ]

        # ------------------------------------------------------
        # CREATE 300 DUMMY FARMERS
        # ------------------------------------------------------

        for i in range(1, 301):

            name = random.choice(names) + " " + str(i)

            mobile = "9" + "".join(
                random.choice("0123456789")
                for _ in range(9)
            )

            age = random.randint(21, 70)

            gender = random.choice([
                "Male",
                "Female"
            ])

            aadhaar = "".join(
                random.choice("0123456789")
                for _ in range(12)
            )

            village = random.choice(villages)

            district = random.choice(districts)

            land = round(
                random.uniform(0.50, 10.00),
                2
            )

            crop = random.choice(crops)

            subsidy = random.choice(subsidies)

            eligible = random.randint(20, 100)

            issued = random.randint(
                0,
                eligible
            )

            balance = eligible - issued

            if balance == 0:
                status = "Completed"
            else:
                status = "Pending"

            # Tamil Nadu Coordinates

            latitude = round(
                random.uniform(10.20, 13.40),
                6
            )

            longitude = round(
                random.uniform(77.20, 80.30),
                6
            )

            bank = random.choice(banks)

            account = "".join(
                random.choice("0123456789")
                for _ in range(12)
            )

            ifsc = "SBIN0" + "".join(
                random.choice("0123456789")
                for _ in range(6)
            )

            cursor.execute(
                """
                INSERT INTO farmers(

                    name,
                    mobile,
                    age,
                    gender,
                    aadhaar,
                    village,
                    district,
                    land,
                    crop,
                    subsidy,
                    eligible,
                    issued,
                    balance,
                    status,
                    latitude,
                    longitude,
                    bank,
                    account,
                    ifsc

                )

                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,(name,mobile,age,gender,aadhaar,village,district,land,crop,subsidy,eligible,issued,balance,status,latitude,longitude,bank,account,ifsc)

            )

        

        # ------------------------------------------------------
        # CREATE DEFAULT HISTORY
        # ------------------------------------------------------

        for farmer_id in range(1, 301):

            records = random.randint(1, 4)

            for _ in range(records):

                quantity = random.randint(5, 50)

                cursor.execute(
                    """
                    INSERT INTO history(
                        farmer_id,
                        quantity
                    )
                    VALUES(?,?)
                    """,
                    (
                        farmer_id,
                        quantity
                    )
                )

    # ------------------------------------------------------
    # SAVE DATABASE
    # ------------------------------------------------------

    conn.commit()
    conn.close()


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

if not os.path.exists(DATABASE):
    initialize_database()


# ==========================================================
# LOGIN REQUIRED DECORATOR
# ==========================================================

from functools import wraps

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "admin" not in session:

            flash("Please login first.", "warning")

            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if (
            username == ADMIN_USERNAME
            and
            password == ADMIN_PASSWORD
        ):

            session["admin"] = username

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid Username or Password",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )
# ==========================================================
# REGISTER FARMER
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        aadhaar = request.form["aadhaar"]

        village = request.form["village"]
        district = request.form["district"]

        land = float(request.form["land"])
        crop = request.form["crop"]

        subsidy = request.form["subsidy"]

        eligible = int(request.form["eligible"])

        latitude = float(request.form["latitude"]) if request.form["latitude"] else None
        longitude = float(request.form["longitude"]) if request.form["longitude"] else None

        bank = request.form["bank"]
        account = request.form["account"]
        ifsc = request.form["ifsc"]

        issued = 0
        balance = eligible
        status = "Pending"

        execute_query(
            """
            INSERT INTO farmers(
                name,
                mobile,
                age,
                gender,
                aadhaar,
                village,
                district,
                land,
                crop,
                subsidy,
                eligible,
                issued,
                balance,
                status,
                latitude,
                longitude,
                bank,
                account,
                ifsc
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                name,
                mobile,
                age,
                gender,
                aadhaar,
                village,
                district,
                land,
                crop,
                subsidy,
                eligible,
                issued,
                balance,
                status,
                latitude,
                longitude,
                bank,
                account,
                ifsc
            )
        )

        flash("Farmer registered successfully.","success")

        return redirect(url_for("farmers"))

    return render_template("register.html")


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    total_farmers = fetch_one(
        "SELECT COUNT(*) total FROM farmers"
    )["total"]

    total_issued = fetch_one(
        "SELECT SUM(issued) total FROM farmers"
    )["total"] or 0

    pending = fetch_one(
        "SELECT COUNT(*) total FROM farmers WHERE status='Pending'"
    )["total"]

    completed = fetch_one(
        "SELECT COUNT(*) total FROM farmers WHERE status='Completed'"
    )["total"]

    inventory = fetch_all(
        """
        SELECT *
        FROM inventory
        ORDER BY item
        """
    )

    recent = fetch_all(
        """
        SELECT *
        FROM farmers
        ORDER BY id DESC
        LIMIT 10
        """
    )

    return render_template("dashboard.html",total_farmers=total_farmers,total_issued=total_issued,pending=pending,completed=completed,inventory=inventory,recent=recent )


# ==========================================================
# FARMERS
# ==========================================================

@app.route("/farmers")
@login_required
def farmers():

    search = request.args.get("search","").strip()

    query = """
    SELECT *
    FROM farmers
    WHERE 1=1
    """

    params = []

    if search:

        query += """
        AND(
            name LIKE ?
            OR mobile LIKE ?
            OR village LIKE ?
            OR district LIKE ?
            OR crop LIKE ?
            OR subsidy LIKE ?
        )
        """

        s = f"%{search}%"

        params.extend([s,s,s,s,s,s])

    query += " ORDER BY id DESC"

    farmers = fetch_all(query, tuple(params))

    return render_template(
        "farmers.html",
        farmers=farmers,
        search=search
    )
# ==========================================================
# FARMER DETAILS
# ==========================================================

@app.route("/farmer/<int:id>")
@login_required
def farmer_details(id):

    farmer = fetch_one(
        "SELECT * FROM farmers WHERE id=?",
        (id,)
    )

    if farmer is None:

        flash("Farmer not found.", "danger")

        return redirect(url_for("farmers"))

    history = fetch_all(
        """
        SELECT *
        FROM history
        WHERE farmer_id=?
        ORDER BY date DESC
        """,
        (id,)
    )

    return render_template(
        "farmer_details.html",
        farmer=farmer,
        history=history
    )


# ==========================================================
# DELETE FARMER
# ==========================================================

@app.route("/delete_farmer/<int:id>")
@login_required
def delete_farmer(id):

    execute_query(
        "DELETE FROM history WHERE farmer_id=?",
        (id,)
    )

    execute_query(
        "DELETE FROM farmers WHERE id=?",
        (id,)
    )

    flash(
        "Farmer deleted successfully.",
        "success"
    )

    return redirect(url_for("farmers"))


# ==========================================================
# EDIT FARMER
# ==========================================================

@app.route("/edit_farmer/<int:id>", methods=["GET","POST"])
@login_required
def edit_farmer(id):

    farmer = fetch_one(
        "SELECT * FROM farmers WHERE id=?",
        (id,)
    )

    if farmer is None:

        flash("Farmer not found.","danger")

        return redirect(url_for("farmers"))

    if request.method=="POST":

        name=request.form["name"]
        mobile=request.form["mobile"]
        age=int(request.form["age"])
        gender=request.form["gender"]
        aadhaar=request.form["aadhaar"]

        village=request.form["village"]
        district=request.form["district"]

        land=float(request.form["land"])
        crop=request.form["crop"]

        subsidy=request.form["subsidy"]

        eligible=int(request.form["eligible"])

        latitude=float(request.form["latitude"]) if request.form["latitude"] else None

        longitude=float(request.form["longitude"]) if request.form["longitude"] else None

        bank=request.form["bank"]
        account=request.form["account"]
        ifsc=request.form["ifsc"]

        issued=farmer["issued"]

        if issued>eligible:
            issued=eligible

        balance=eligible-issued

        status="Completed" if balance==0 else "Pending"

        execute_query(
            """
            UPDATE farmers
            SET
                name=?,
                mobile=?,
                age=?,
                gender=?,
                aadhaar=?,
                village=?,
                district=?,
                land=?,
                crop=?,
                subsidy=?,
                eligible=?,
                issued=?,
                balance=?,
                status=?,
                latitude=?,
                longitude=?,
                bank=?,
                account=?,
                ifsc=?
            WHERE id=?
            """,
            (
                name,
                mobile,
                age,
                gender,
                aadhaar,
                village,
                district,
                land,
                crop,
                subsidy,
                eligible,
                issued,
                balance,
                status,
                latitude,
                longitude,
                bank,
                account,
                ifsc,
                id
            )
        )

        flash(
            "Farmer updated successfully.",
            "success"
        )

        return redirect(
            url_for("farmer_details",id=id)
        )

    return render_template(
        "edit_farmer.html",
        farmer=farmer
    )
# ==========================================================
# ISSUE SUBSIDY
# ==========================================================

@app.route("/issue/<int:id>", methods=["GET", "POST"])
@login_required
def issue(id):

    farmer = fetch_one(
        "SELECT * FROM farmers WHERE id=?",
        (id,)
    )

    if farmer is None:
        flash("Farmer not found.", "danger")
        return redirect(url_for("farmers"))

    inventory = fetch_all(
        """
        SELECT *
        FROM inventory
        ORDER BY item
        """
    )

    if request.method == "POST":

        item = request.form["item"]
        quantity = int(request.form["quantity"])

        stock = fetch_one(
            "SELECT * FROM inventory WHERE item=?",
            (item,)
        )

        if stock is None:
            flash("Item not found.", "danger")
            return redirect(url_for("issue", id=id))

        if quantity > stock["quantity"]:
            flash("Not enough stock available.", "danger")
            return redirect(url_for("issue", id=id))

        balance = farmer["balance"]

        if quantity > balance:
            flash("Quantity exceeds remaining eligible subsidy.", "danger")
            return redirect(url_for("issue", id=id))

        new_stock = stock["quantity"] - quantity

        execute_query(
            """
            UPDATE inventory
            SET quantity=?
            WHERE item=?
            """,
            (
                new_stock,
                item
            )
        )

        new_issued = farmer["issued"] + quantity
        new_balance = farmer["eligible"] - new_issued

        if new_balance == 0:
            status = "Completed"
        else:
            status = "Pending"

        execute_query(
            """
            UPDATE farmers
            SET
                issued=?,
                balance=?,
                status=?
            WHERE id=?
            """,
            (
                new_issued,
                new_balance,
                status,
                id
            )
        )

        execute_query(
            """
            INSERT INTO history(
                farmer_id,
                quantity
            )
            VALUES(?,?)
            """,
            (
                id,
                quantity
            )
        )

        flash("Subsidy issued successfully.", "success")

        return redirect(url_for("farmer_details", id=id))

    return render_template(
        "issue.html",
        farmer=farmer,
        inventory=inventory
    )


# ==========================================================
# INVENTORY
# ==========================================================

@app.route("/inventory")
@login_required
def inventory():

    items = fetch_all(
        """
        SELECT *
        FROM inventory
        ORDER BY item
        """
    )

    return render_template(
        "inventory.html",
        inventory=items
    )


# ==========================================================
# UPDATE INVENTORY
# ==========================================================

@app.route("/update_inventory/<int:id>", methods=["POST"])
@login_required
def update_inventory(id):

    quantity = int(request.form["quantity"])

    execute_query(
        """
        UPDATE inventory
        SET quantity=?
        WHERE id=?
        """,
        (
            quantity,
            id
        )
    )

    flash("Inventory updated successfully.", "success")

    return redirect(url_for("inventory"))


# ==========================================================
# HISTORY
# ==========================================================

@app.route("/history")
@login_required
def history():

    records = fetch_all(
        """
        SELECT
            history.id,
            farmers.name,
            farmers.subsidy,
            history.quantity,
            history.date
        FROM history
        JOIN farmers
        ON history.farmer_id = farmers.id
        ORDER BY history.date DESC
        """
    )

    return render_template(
        "history.html",
        history=records
    )


# ==========================================================
# EXPORT CSV
# ==========================================================

@app.route("/export")
@login_required
def export():

    farmers = fetch_all(
        "SELECT * FROM farmers ORDER BY id"
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Name",
        "Mobile",
        "Village",
        "District",
        "Crop",
        "Subsidy",
        "Eligible",
        "Issued",
        "Balance",
        "Status"
    ])

    for farmer in farmers:

        writer.writerow([
            farmer["id"],
            farmer["name"],
            farmer["mobile"],
            farmer["village"],
            farmer["district"],
            farmer["crop"],
            farmer["subsidy"],
            farmer["eligible"],
            farmer["issued"],
            farmer["balance"],
            farmer["status"]
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=farmers.csv"
        }
    )
# ==========================================================
# MAP
# ==========================================================

@app.route("/map")
@login_required
def map_view():

    farmers = fetch_all(
        """
        SELECT
            id,
            name,
            village,
            district,
            crop,
            subsidy,
            latitude,
            longitude,
            status
        FROM farmers
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
        """
    )

    return render_template(
        "map.html",
        farmers=farmers
    )


# ==========================================================
# SEARCH API (OPTIONAL)
# ==========================================================

@app.route("/api/farmers")
@login_required
def farmers_api():

    farmers = fetch_all(
        """
        SELECT
            id,
            name,
            village,
            district,
            crop,
            subsidy,
            eligible,
            issued,
            balance,
            latitude,
            longitude,
            status
        FROM farmers
        """
    )

    data = []

    for farmer in farmers:

        data.append({
            "id": farmer["id"],
            "name": farmer["name"],
            "village": farmer["village"],
            "district": farmer["district"],
            "crop": farmer["crop"],
            "subsidy": farmer["subsidy"],
            "eligible": farmer["eligible"],
            "issued": farmer["issued"],
            "balance": farmer["balance"],
            "latitude": farmer["latitude"],
            "longitude": farmer["longitude"],
            "status": farmer["status"]
        })

    return data


# ==========================================================
# 404 ERROR
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        render_template("404.html"),
        404
    )


# ==========================================================
# 500 ERROR
# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return (
        render_template("500.html"),
        500
    )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )