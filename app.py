from flask import Flask, render_template, request, send_file, jsonify

from sqlalchemy import text, create_engine
from io import BytesIO
from PIL import Image
import io

import random

engine = create_engine("mysql+pymysql://SaharaAdmin:abcdefg123@localhost:3306/productdb",future=True)

app = Flask(__name__)

def getImageMimeType(imageBytes) -> str:
    image = Image.open(BytesIO(imageBytes))
    mimeType = Image.MIME[image.format]
    return mimeType

@app.route("/productImage/<int:productID>")
def productImage(productID:int):
    with engine.connect() as connection:
        query = text("SELECT productImage FROM allproducts WHERE productID = :id")
        result = connection.execute(query, {"id": productID}).fetchone()
        
        if result and result[0]:
            return send_file(BytesIO(result[0]), mimetype=getImageMimeType(result[0]))
    return False

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

    image = Image.open(request.files["productImage"])

    imageByte = io.BytesIO()
    image.save(imageByte, format=image.format)
    imageByte = imageByte.getvalue()

    with engine.connect() as connection:
        query = text(
            "INSERT INTO allproducts (productName, productPrice, productImage) VALUES (:name, :price, :image)"
        )
        connection.execute(query, {"name": name, "price": price, "image": imageByte})
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
        for row in result:
            for i in range(len(row)):
                if isinstance(row[i],bytes):
                    row[i] = row[i].decode("utf-8")
        print(result)
    return jsonify(result=result)

if __name__ == "__main__":
    app.run()