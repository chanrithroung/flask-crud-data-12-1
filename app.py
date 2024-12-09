from flask import Flask, render_template
app = Flask(__name__)

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template("create.html")

# @app.route("/submit")


if __name__ == "__main__":
    app.run(debug=True)