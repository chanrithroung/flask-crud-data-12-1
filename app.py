from flask import Flask, render_template, request, jsonify, redirect
import psycopg2
app = Flask(__name__)

DB_HOST = "127.0.0.1" # or localhost
DB_NAME = "db_12_1"
DB_USER = "postgres"
DB_PASSWORD =  "24022004"


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def index():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(""" SELECT * FROM users ORDER BY id ASC """)
    users = cursor.fetchall()
    return render_template("index.html", users=users)

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template("create.html")


@app.route("/submit")
def submit():
    first_name = request.args.get('first-name')
    last_name = request.args.get('last-name')
    email = request.args.get('email')

    con = get_db_connection()
    if con:
        cursor = con.cursor()
        query = f"""
                INSERT INTO users(first_name, last_name, email)
                VALUES ('{first_name}', '{last_name}', '{email}');
            """
        cursor.execute(query=query)
        con.commit()
        con.close()
        cursor.close()

        return redirect("/create")

@app.route("/update-user/<id>")
def update_user(id):
    con = get_db_connection()
    cursor = con.cursor()
    qeury = f"SELECT * FROM users WHERE id =  {id};"
    cursor.execute(query=qeury)
    con.commit()
    user = cursor.fetchall()
    cursor.close()
    con.close()
    return render_template('update.html', user=user)


@app.route("/update-submit", methods=["GET", "POST"])
def update_submit():
    id = request.form['id']
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    email = request.form['email']

    query = f"UPDATE users SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}' WHERE id = {id};"
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(query=query)
    con.commit()
    cursor.close()
    con.close()

    return redirect('list-users')


# Remove User
@app.route("/remove-user", methods=["GET", "POST"])
def remove_user():
    con = get_db_connection()
    cursor = con.cursor()

    id = request.form['remove-id']

    query = f"DELETE FROM users WHERE id = '{id}'"
    cursor.execute( query=query )

    con.commit()
    cursor.close()
    con.close()

    return redirect("/list-users")

@app.route("/list-users")
def list_users():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM users ORDER BY id ASC""")
    users = cursor.fetchall()
    return render_template("list_users.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)