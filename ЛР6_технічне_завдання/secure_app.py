from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    name = request.args.get("name", "")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # БЕЗПЕЧНО — параметризований SQL
    query = "SELECT * FROM students WHERE name LIKE ?"
    param = f"%{name}%"

    print("Executing SECURE:", query, param)

    c.execute(query, (param,))
    results = c.fetchall()

    return render_template("results.html", students=results, query=query)

app.run(debug=True)
