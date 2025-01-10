from flask import Flask, render_template, request, jsonify

from sqlalchemy import text, create_engine, inspect

import random

engine = create_engine("mysql+pymysql://SaharaAdmin:abcdefg123@localhost:3306/productdb",future=True)

app = Flask(__name__)

class Table:

    def __init__(self,tableName:str):
        self._name = tableName

        self._columns = [col["name"] for col in inspect(engine).get_columns(tableName)]
    
    @property
    def Name(self) -> str:
        return self._name
    
    @property
    def Columns(self) -> list[str]:
        return self._columns

class UserData:

    _cart = []
    _totalIncurrence = 0

    @classmethod
    def addToCart(cls,productID:int):
        with engine.connect() as connection:
            query = text("SELECT * FROM allproducts where productID = :id")
            result = connection.execute(query,{"id":productID}).fetchone()
        

    @classmethod
    def inCart(cls,productID:int,adding:bool) -> bool:
        pass

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
            "INSERT INTO allproducts (productName, productPrice, productImageName) VALUES (:name, :price, :imageName)"
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
    if data["result"] != "":
        with engine.connect() as connection:
            query = text("SELECT * FROM allproducts WHERE productName LIKE :search")
            result = list(connection.execute(query,{"search":f"{data['result']}%"}))
            columnIter = iter(Table("allproducts").Columns)
            for i in range(len(result)):
                result[i] = {next(columnIter):info for info in result[i]}
                columnIter = iter(Table("allproducts").Columns)
        return jsonify(result=result)
    
@app.route("/addToCart",methods=["POST"])
def handleAddToCart():
    data = request.get_json()

if __name__ == "__main__":
    app.run()