from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
import Quandl

# This is a init commit from yutong
app = Flask(__name__)

# restful api
api = Api(app)


class StockPrice(Resource):
    def put(self):
        stock_sticker = "WIKI/" + request.form['stocksticker']
        stockdata = Quandl.get(stock_sticker, returns="numpy", trim_start="2015-01-01", trim_end="2015-01-31")
        return {"stockdata": list(stockdata.Close)}


api.add_resource(StockPrice, '/stockprice')


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
