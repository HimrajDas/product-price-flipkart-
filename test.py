from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


app = Flask(__name__)


def info():
    query = "iphone12"
    url = f"https://www.flipkart.com/search?q={query}"
    client = urlopen(url)
    page = client.read()
    soup = bs(page, "html.parser")
    products = soup.find_all("div", {"class": "_4rR01T"})
    prices = soup.find_all("div", {"class": "_30jeq3 _1_WHN1"})
    results = []
    my_dict = {}

    for i in range(len(products)):
        name = products[i].text.strip()
        price = prices[i].text





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)