from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False   # From Finance problem
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("postgresql://neondb_owner:npg_riYhyFIL37Mn@ep-wild-scene-adcomaf5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists
        if len(rows) != 1:
            return apology("Username doesn't Exist")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username")

        # Ensure username does not exist
        try:
            # Query database to store username
            id = db.execute("INSERT INTO users(username) VALUES(?)", request.form.get("username"))
        except ValueError:
            return apology("Username already Exists")

        # Remember which user has logged in
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/compare", methods=["POST"])
@login_required
def compare():

    # Set variables to store data in memory
    option1 = request.form.get("option1")
    option2 = request.form.get("option2")
    criteria = []

    # Ensure both options were submitted
    if not option1 or not option2:
        return apology("Invalid options")

    # Store the user-entered criterion and their weight
    for i in range(5):
        name = request.form.get(f"criterion{i}")
        weight = request.form.get(f"weight{i}")
        if name and weight:
            criteria.append({"name": name, "weight": int(weight)})   # Searched google to append

    # Ensure criteria & weight were submitted
    if not criteria:
        return apology("Invalid criterion/weight")

    # Send the data to next page and show the page
    return render_template("ratings.html", option1=option1, option2=option2, criteria=criteria)
    # Used ChatGPT to learn a way of carrying information across different pages of a web-application,
    # without storing it in a database yet.


@app.route("/result", methods=["POST"])
@login_required
def result():

    # Set variables to store data in memory (again)
    option1 = request.form.get("option1")
    option2 = request.form.get("option2")
    criteria = []
    ratings = []
    total1 = 0
    total2 = 0

    # Get all the information and user-entered ratings from the page
    criterion_names = request.form.getlist("criterion")   # Searched google to get list
    weights = request.form.getlist("weight")
    ratings1 = request.form.getlist("rating1")
    ratings2 = request.form.getlist("rating2")

    # Ensure ratings were submitted
    if "" in ratings1 or "" in ratings2:   # Searched google to check for empty elements in a list
        return apology("Invalid ratings")

    # Ensure that the submitted data is valid
    if not (option1 and option2 and not ("" in criterion_names or "" in weights)):
        return apology("Invalid Usage !")

    # Perform operations to get Total score
    for i in range(len(criterion_names)):
        weight = int(weights[i])
        r1 = int(ratings1[i])
        r2 = int(ratings2[i])

        criteria.append({"name": criterion_names[i], "weight": weight})
        ratings.append({"criterion": criterion_names[i], "rating1": r1, "rating2": r2})

        # Rating X Weight = Criterion Score
        r1 *= weight
        r2 *= weight

        total1 += r1
        total2 += r2

    if total1 == total2:
        winner = "Scores are Equal"
    elif total1 > total2:
        winner = option1
    else:
        winner = option2

    # Store all data in the Database for history
    db.execute("INSERT INTO decisions VALUES(?, ?, ?, ?, datetime(current_timestamp, 'localtime'))", session["user_id"], option1, option2, winner)

    return render_template("result.html", option1=option1, option2=option2, total1=total1, total2=total2, winner=winner)


@app.route("/history")
@login_required
def history():
    decisions = db.execute("SELECT * FROM decisions WHERE user_id = ? ORDER BY datetime DESC", session["user_id"])
    return render_template("history.html", decisions=decisions)
