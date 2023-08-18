from flask import Flask, jsonify, request
from flask_cors import CORS

import modules.downloader as granules
import modules.plot_loader as plotter


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/granules")
def allGranules():
	dataframe = granules.getAll()
	return dataframe.to_json(orient='records', default_handler=str)

@app.route("/download", methods=['POST'])
def download():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        url = json['url']
        name = json['name']
        result = granules.download(url, name)
        return result
    else:
        return 'Content-Type not supported!'
    
@app.route("/mineral-map/<fileName>", methods=['GET'])
def getMineralMap(fileName):
	html = plotter.mineralMap(fileName + '.nc', 2)
	return html

if __name__ == '__main__':
    app.run()
