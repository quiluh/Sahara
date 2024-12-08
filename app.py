from flask import Flask, render_template, request, send_file

from sqlalchemy import text, create_engine
from io import BytesIO
from PIL import Image
import io

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

    image = Image.open(request.form["productImage"])
    image = image.resize((500,500),Image.LANCZOS)

    imageByte = io.BytesIO()
    image.save(imageByte, format=image.format)
    imageByte = imageByte.getvalue()

    with engine.connect() as connection:
        query = text("INSERT INTO allproducts (id, name, price, image) VALUES (:id, :name, :price, :image)")
        connection.execute(query, {"id": id, "name": name, "price": price, "image": imageByte})
    
    return True

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
    app.run(debug=True)