from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def createConnection():
    return pymysql.connect(
        host = "localhost",
        port = 3306,
        user = "SaharaAdmin",
        password="abcdefg123",
        db = "",
        cursorclass = pymysql.cursors.DictCursor
    )

@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/admin")
def Admin():
    return render_template("admin.html")

@app.route("/adminUpdate",methods=["POST"])
def adminUpdate():
    pass

if __name__ == "__main__":
    app.run(debug=True)