from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response
)

import sqlite3
import random
import csv
import io
import os

app = Flask(__name__)
app.secret_key = "agrisetu_secret_key"

DATABASE = "database.db"


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

    cursor = conn.cursor()

    cursor.execute(query, values)

    rows = cursor.fetchall()

    conn.close()

    return rows


def fetch_one(query, values=()):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(query, values)

    row = cursor.fetchone()

    conn.close()

    return row


def execute_query(query, values=()):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(query, values)

    conn.commit()

    conn.close()


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================
def initialize_database():

    conn = get_db()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # FARMERS TABLE
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
    # HISTORY TABLE
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
    # INVENTORY TABLE
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        item TEXT,

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

        inventory_items = [

            ("Rice Seeds",5000),
            ("Wheat Seeds",4500),
            ("DAP Fertilizer",4200),
            ("Urea",4600),
            ("Organic Fertilizer",3600),
            ("Pesticide",3100),
            ("Sprayer",900),
            ("Drip Kit",650),
            ("Water Pump",500),
            ("Tractor Subsidy",200)

        ]

        cursor.executemany(

            """
            INSERT INTO inventory(
                item,
                quantity
            )
            VALUES(?,?)
            """,

            inventory_items

        )

    # ------------------------------------------------------
    # CHECK FARMERS
    # ------------------------------------------------------

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
            "Siruseri","Porur","Ambattur","Avadi",
            "Poonamallee","Anna Nagar","T Nagar",
            "Mylapore","Thiruvanmiyur","Red Hills",
            "Urapakkam","Maraimalai Nagar",
            "Kundrathur","Alandur","Kovilambakkam",
            "Pammal","Adyar","Sembakkam",
            "Nanganallur","Tambaram East",
            "Tambaram West","Selaiyur",
            "Mudichur","Mambakkam",
            "Thaiyur","Karanai",
            "Padur","Semmenchery"

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
        # CREATE 300 FARMERS
        # ------------------------------------------------------

        for i in range(1, 301):

            name = random.choice(names) + " " + str(i)

            mobile = "9" + "".join(
                random.choice("0123456789")
                for _ in range(9)
            )

            age = random.randint(21, 70)

            gender = random.choice(["Male", "Female"])

            aadhaar = "".join(
                random.choice("0123456789")
                for _ in range(12)
            )

            village = random.choice(villages)

            district = random.choice(districts)

            land = round(random.uniform(0.5, 10), 2)

            crop = random.choice(crops)

            subsidy = random.choice(subsidies)

            eligible = random.randint(20, 100)

            issued = random.randint(0, eligible)

            balance = eligible - issued

            status = "Completed" if balance == 0 else "Pending"

            latitude = round(random.uniform(8.0, 13.5), 6)

            longitude = round(random.uniform(76.0, 80.5), 6)

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
        # ------------------------------------------------------
        # DEFAULT HISTORY
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
    # SAVE CHANGES
    # ------------------------------------------------------

    conn.commit()
    conn.close()

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

if not os.path.exists(DATABASE):

    initialize_database()


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================================
# LOGIN
# ==========================================================


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        flash("Login Successful!", "success")

        return redirect(url_for("dashboard"))

    return render_template("login.html")

# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    flash("Logged out successfully.", "success")

    return redirect(url_for("login"))


# ==========================================================
# REGISTER FARMER
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        aadhaar = request.form["aadhaar"]

        district = request.form["district"]
        village = request.form["village"]
        subsidy = request.form["subsidy"]

        crop = request.form["crop"]
        land = request.form["land"]

        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        bank = request.form["bank"]
        account = request.form["account"]
        ifsc = request.form["ifsc"]

        issued = 0
        eligible = int(request.form["eligible"])

        balance = eligible

        status = "Pending"
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
             
             INSERT INTO farmers
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
             
             VALUES
             (
             ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
             )
             
             """,
             
             (
             name,
             age,
             gender,
             mobile,
             aadhaar,
             district,
             village,
             crop,
             land,
             latitude,
             longitude,
             bank,
             account,
             ifsc
             )
             
        )
        conn.commit()
        conn.close()

        

        flash("Farmer Registered Successfully!", "success")

        return redirect(url_for("farmers"))

    return render_template("register.html")
# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    total_farmers = fetch_one(
        "SELECT COUNT(*) AS total FROM farmers"
    )["total"]

    total_issued = fetch_one(
        "SELECT SUM(issued) AS total FROM farmers"
    )["total"]

    if total_issued is None:
        total_issued = 0

    pending = fetch_one(
        "SELECT COUNT(*) AS total FROM farmers WHERE status='Pending'"
    )["total"]

    completed = fetch_one(
        "SELECT COUNT(*) AS total FROM farmers WHERE status='Completed'"
    )["total"]

    inventory = fetch_all(
        """
        SELECT *
        FROM inventory
        ORDER BY item_name
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

    return render_template(

        "dashboard.html",

        total_farmers=total_farmers,

        total_issued=total_issued,

        pending=pending,

        completed=completed,

        inventory=inventory,

        recent=recent

    )


# ==========================================================
# FARMERS
# ==========================================================

@app.route("/farmers")
def farmers():

    search = request.args.get("search", "").strip()

    if search:

        farmers = fetch_all(

            """

            SELECT *

            FROM farmers

            WHERE

                name LIKE ?

                OR mobile LIKE ?

                OR village LIKE ?

                OR district LIKE ?

                OR crop LIKE ?

                OR subsidy LIKE ?

            ORDER BY id

            """,

            (

                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%"

            )

        )

    else:

        farmers = fetch_all(

            """

            SELECT *

            FROM farmers

            ORDER BY id

            """

        )

    return render_template(

        "farmers.html",

        farmers=farmers,

        search=search

    )


# ==========================================================
# FARMER DETAILS
# ==========================================================

@app.route("/farmer/<int:id>")
def farmer_details(id):

    farmer = fetch_one(

        """

        SELECT *

        FROM farmers

        WHERE id=?

        """,

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

    return redirect(

        url_for("farmers")

    )


# ==========================================================
# EDIT FARMER
# ==========================================================

@app.route("/edit_farmer/<int:id>", methods=["GET", "POST"])
# ==========================================================
# EDIT FARMER
# ==========================================================

@app.route("/edit_farmer/<int:id>", methods=["GET", "POST"])
def edit_farmer(id):

    farmer = fetch_one(
        "SELECT * FROM farmers WHERE id=?",
        (id,)
    )

    if farmer is None:

        flash("Farmer not found.", "danger")

        return redirect(url_for("farmers"))

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

        latitude = (
            float(request.form["latitude"])
            if request.form["latitude"]
            else None
        )

        longitude = (
            float(request.form["longitude"])
            if request.form["longitude"]
            else None
        )

        bank = request.form["bank"]
        account = request.form["account"]
        ifsc = request.form["ifsc"]

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
                latitude,
                longitude,
                bank,
                account,
                ifsc,
                id
            )
        )

        flash("Farmer details updated successfully.", "success")

        return redirect(url_for("farmer_details", id=id))

    return render_template(
        "edit_farmer.html",
        farmer=farmer
    )
#===========================================================
# ISSUE SUBSIDY
# ==========================================================

@app.route("/issue/<int:id>", methods=["GET", "POST"])
def issue(id):

    farmer = fetch_one(

        "SELECT * FROM farmers WHERE id=?",

        (id,)

    )

    if farmer is None:

        flash("Farmer not found.", "danger")

        return redirect(url_for("farmers"))

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        if quantity <= 0:

            flash("Enter a valid quantity.", "warning")

            return redirect(url_for("issue", id=id))

        if quantity > farmer["balance"]:

            flash("Quantity exceeds remaining balance.", "danger")

            return redirect(url_for("issue", id=id))

        item = fetch_one(

            "SELECT * FROM inventory WHERE item_name=?",

            (farmer["subsidy"],)

        )

        if item is None:

            flash("Inventory item not found.", "danger")

            return redirect(url_for("inventory"))

        if item["available_stock"] < quantity:

            flash("Insufficient stock.", "danger")

            return redirect(url_for("issue", id=id))

        new_issued = farmer["issued"] + quantity

        new_balance = farmer["balance"] - quantity

        status = "Completed"

        if new_balance > 0:

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

            UPDATE inventory

            SET

                available_stock = available_stock - ?

            WHERE item_name=?

            """,

            (

                quantity,

                farmer["subsidy"]

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

        flash(

            "Subsidy Issued Successfully.",

            "success"

        )

        return redirect(

            url_for("farmer_details", id=id)

        )

    return render_template(

        "issue.html",

        farmer=farmer

    )


# ==========================================================
# HISTORY
# ==========================================================

@app.route("/history")
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

        records=records

    )


# ==========================================================
# INVENTORY
# ==========================================================

@app.route("/inventory")
def inventory():

    items = fetch_all(

        """

        SELECT *

        FROM inventory

        ORDER BY item_name

        """

    )

    return render_template(

        "inventory.html",

        items=items

    )


# ==========================================================
# EXPORT CSV
# ==========================================================

@app.route("/export")
def export():

    farmers = fetch_all(

        "SELECT * FROM farmers"

    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",
        "Name",
        "Mobile",
        "Village",
        "District",
        "Land",
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
            farmer["land"],
            farmer["crop"],
            farmer["subsidy"],
            farmer["eligible"],
            farmer["issued"],
            farmer["balance"],
            farmer["status"]

        ])

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

            status,

            latitude,

            longitude

        FROM farmers

        ORDER BY name

        """

    )

    return render_template(

        "map.html",

        farmers=farmers

    )
# ==========================================================
# 404 ERROR PAGE
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ), 404


# ==========================================================
# 500 ERROR PAGE
# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return render_template(

        "500.html"

    ), 500


# ==========================================================
# CONTEXT PROCESSOR
# ==========================================================

@app.context_processor
def inject_app_name():

    return {

        "app_name": "AgriSetu"

    }


# ==========================================================
# CACHE CONTROL
# ==========================================================

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = \
        "no-cache, no-store, must-revalidate"

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


# ==========================================================
# RUN APPLICATION
# ==========================================================
# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    if not os.path.exists(DATABASE):
        initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )