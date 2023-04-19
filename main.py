from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template
from flask_cors import cross_origin
from urllib.request import urlopen
import logging
import pymongo

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)


@app.route("/")
@cross_origin()
def show_index():
    return render_template("index.html")


@app.route("/details", methods=["GET", "POST"])
@cross_origin()
def contents():
    if request.method == "POST":
        try:
            query = request.form["content"].replace(" ", "")
            flipkart_url = f"https://www.flipkart.com/search?q={query}"
            url_client = urlopen(flipkart_url)
            page = url_client.read()
            soup = bs(page, "html.parser")
            products = soup.find_all("div", {"class": "_4rR01T"})
            prices = soup.find_all("div", {"class": "_30jeq3 _1_WHN1"})
            results = []
            for i in range(len(products)):
                product_name = products[i].text.strip()
                product_price = prices[i].text.strip()

                my_dict = {
                    "Product": product_name,
                    "Price": product_price
                }

                results.append(my_dict)

            try:
                client = pymongo.MongoClient("mongodb+srv://Himraj:My$MongodB$@cluster0.prceeb8.mongodb.net/test")
                db = client["flipkart_price_scrapper"]
                data_collection = db["product_prices"]
                data_collection.insert_many(results)
            except Exception as e:
                logging.info(e)


            return render_template("result.html", results=results[0:(len(results) - 1)])

        except Exception as e:
            logging.info(e)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
