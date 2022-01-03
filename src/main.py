from flask import Flask, jsonify
from scrapper import ScrapeData

app = Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def start():
    return "<h1>Peter's Server</h1>"


@app.route('/<committee>/<year>', methods=['GET'])
def return_data(committee, year):
    data = ScrapeData(committee=committee, year=year)
    return jsonify(data.scrape())


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
