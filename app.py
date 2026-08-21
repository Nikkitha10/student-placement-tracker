
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "database/placement.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_role TEXT NOT NULL,
            package TEXT,
            location TEXT,
            application_date TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()

    return render_template("index.html", companies=companies)


@app.route("/add", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        package = request.form["package"]
        location = request.form["location"]
        application_date = request.form["application_date"]
        status = request.form["status"]

        conn = get_db()

        conn.execute("""
            INSERT INTO companies
            (company_name, job_role, package, location, application_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company_name,
            job_role,
            package,
            location,
            application_date,
            status
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_company.html")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_company(id):

    conn = get_db()

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        package = request.form["package"]
        location = request.form["location"]
        application_date = request.form["application_date"]
        status = request.form["status"]

        conn.execute("""
            UPDATE companies
            SET company_name = ?,
                job_role = ?,
                package = ?,
                location = ?,
                application_date = ?,
                status = ?
            WHERE id = ?
        """, (
            company_name,
            job_role,
            package,
            location,
            application_date,
            status,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    company = conn.execute(
        "SELECT * FROM companies WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_company.html", company=company)


@app.route("/delete/<int:id>")
def delete_company(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM companies WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)