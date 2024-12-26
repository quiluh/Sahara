from flask import Flask, render_template, request, send_file

from sqlalchemy import text, create_engine
from io import BytesIO
from PIL import Image
import io

import random

engine = create_engine("mysql+pymysql://SaharaAdmin:abcdefg123@localhost:3306/productdb",future=True)

app = Flask(__name__)

@app.route("/")
def Home():
    randomProducts = []
    with engine.connect() as connection:
        query = text("SELECT * FROM allproducts")
        result = connection.execute(query)
        for i in range(16):
            randomIn = random.randint(0,len(list(result))+1)
            if dict(list(result)[randomIn]) in randomProducts:
                i -= 1
            else:
                randomProducts.append(dict(list(result)[randomIn]))
    return render_template("home.html",randomProducts=randomProducts)

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

def getImageMimeType(imageBytes) -> str:
    image = Image.open(BytesIO(imageBytes))
    mimeType = Image.MIME[image.format]
    return mimeType

@app.route("/productImage/<int:productID>")
def productImage(productID:int):
    with engine.connect() as connection:
        query = text("SELECT displayImage FROM allproducts WHERE productID = :id")
        result = connection.execute(query, {"id": productID}).fetchone()
        
        if result and result[0]:
            return send_file(BytesIO(result[0]), mimetype=getImageMimeType(result[0]))
    return False

if __name__ == "__main__":
    app.run()