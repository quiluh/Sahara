from flask import Flask, render_template, request, send_file, jsonify

from sqlalchemy import text, create_engine

import random

engine = create_engine("mysql+pymysql://SaharaAdmin:abcdefg123@localhost:3306/productdb",future=True)

app = Flask(__name__)

@app.route("/")
def Home():
    randomIn = []
    rows,columns = (4,4) # COLUMNS HAVE TO BE FACTOR OF 12
    randomProducts = [[None for i in range(columns)] for o in range(rows)]
    with engine.connect() as connection:
        query = text("SELECT * FROM allproducts")
        result = list(connection.execute(query))
        while len(randomIn) != rows*columns:
            index = random.randint(0,len(result)-1)
            if index not in randomIn:
                randomIn.append(index)
    randomIn = iter(randomIn)
    for i in randomProducts:
        for o in range(len(i)):
            i[o] = result[next(randomIn)]
    return render_template("home.html",randomProducts=randomProducts,columnKey={1:"col-sm-12",2:"col-sm-6",3:"col-sm-4",4:"col-sm-3",6:"col-sm-2",12:"col-sm-1"})

@app.route("/admin")
def Admin():
    return render_template("admin.html")

@app.route("/adminUpdate", methods=["POST"])
def adminUpdate():
    name = request.form["productName"]
    price = request.form["productPrice"]
    imageName = request.form["productImageName"]

    with engine.connect() as connection:
        query = text(
            "INSERT INTO allproducts (productName, productPrice, productImage) VALUES (:name, :price, :imageName)"
        )
        connection.execute(query, {"name": name, "price": price, "imageName": imageName})
        connection.commit()

    return render_template("admin.html")

@app.route("/product/<int:productID>")
def Product(productID:int):
    with engine.connect() as connection:
        query = text("SELECT * FROM allproducts WHERE productID = :id")
        result = connection.execute(query,{"id":productID}).fetchone()
    return render_template("product.html",product=result)

@app.route("/processSearch",methods=["POST"])
def processSearch():
    data = request.get_json()
    with engine.connect() as connection:
        query = text("SELECT * FROM allproducts WHERE productName LIKE :search")
        result = list(connection.execute(query,{"search":f"%{data['result']}%"}))
        result = [list(row) for row in result]
    return jsonify(result=result)

if __name__ == "__main__":
    app.run()