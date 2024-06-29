from flask import Flask, render_template, request

from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://SaharaAdmin:abcdefg123@localhost:3306/productdb")

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/admin")
def Admin():
    return render_template("admin.html")

@app.route("/adminUpdate",methods=["POST"])
def adminUpdate():
    id = request.form["productID"]
    name = request.form["productName"]
    price = request.form["productPrice"]
    image = request.form["productImage"].read()

    with engine.connect() as connection:
        query = text("INSERT INTO allproducts (id, name, price, image) VALUES (:id, :name, :price, :image)")
        connection.execute(query, {"id": id, "name": name, "price": price, "image": image})
    
    return True

if __name__ == "__main__":
    app.run(debug=True)