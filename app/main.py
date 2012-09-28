import os.path
import json

from flask import Flask,request,jsonify,Response,render_template
from jinja2 import Template,FileSystemLoader,Environment

import config,plz

app = Flask(__name__)
locator= plz.locateCH(config.plz_csv_file)

@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/search')
def search():
#    return jsonify(data=locator.find(request.args.get('term','')))
    data  = locator.find(request.args.get('term',''))
    names = map(lambda x:x['ort'],data)
    return Response(json.dumps(names),mimetype='application/json')

if __name__ == '__main__':
    print 'open the following URL in your web browser:'
    app.debug= True
    app.run()

