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

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)