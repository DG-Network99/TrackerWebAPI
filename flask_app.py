from flask import Flask, render_template, request, redirect
from threading import Thread
import asyncio
from sql import full_productbase
from mongo_db import get_products, get_products2

app = Flask('')

@app.route('/')
async def index():
#   return "Hi there, the website is live"
    return redirect("https://amzn.to/42ZRUvW")

@app.route("/userproducts/<user_id>")
async def home(user_id):
    data = await get_products(user_id)
    return render_template('home.html', data = data)

@app.route("/product/<tracking_id>")
async def product(tracking_id):

    data = get_products2(tracking_id)
    return render_template('product.html', data=data)


# @app.route("/hello/<input>")
# def url_route(input):
#    products = asyncio.run(full_productbase(input))
#    products_list = []

#    for product in products:
#         print(product.product_name)
#         products_list.append(product.product_name)
#    #return products_list
#    return render_template('index.html',products = products_list)

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)    