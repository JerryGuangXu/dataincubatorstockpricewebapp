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



@app.route('/stockplot',methods=['POST'])
def stockplot():
    import numpy as np
    stock_sticker = "WIKI/" + request.form['stocksticker']
    checkeditems = request.form.getlist('check')
    colors = ["A6CEE3", "#B2DF8A", "#33A02C", "#FB9A99"]
    import datetime
    now = datetime.datetime.now()
    #get last day of last month
    lastday = now.replace(day=1)-datetime.timedelta(days=1)
    lastdaystr = lastday.strftime("%Y-%m-%d")
    firstday = lastday.replace(day=1)
    firstdaystr = firstday.strftime("%Y-%m-%d")
    try:
        stockdata = Quandl.get(stock_sticker, returns="numpy", trim_start=firstdaystr, trim_end=lastdaystr)
        from bokeh.plotting import figure, show, output_file, vplot
        from bokeh.embed import components
        plot = figure(x_axis_type = "datetime")
        plot.title = "Data from Quandle WIKI set"
        plot.xaxis.axis_label = 'Date'
        plot.yaxis.axis_label = 'Price'
        for i in range(len(checkeditems)):
            plot.line(stockdata.Date,stockdata[checkeditems[i]], color=colors[i], legend=checkeditems[i])
        script, div = components(plot)
        return render_template('graph.html',script=script, div=div, text=stock_sticker)
    except:
        errormessage = "Dataset Not Found, Try a different Ticker Symbol"
        return render_template('index.html', errormessage=errormessage)

if __name__ == '__main__':
    app.run()
