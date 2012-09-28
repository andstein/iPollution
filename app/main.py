import os.path
import json

from flask import Flask,request,jsonify,Response
from jinja2 import Template,FileSystemLoader,Environment

import config,plz,maps

app = Flask(__name__)
jenv= Environment(loader=FileSystemLoader(config.template_dir))
locator= plz.locateCH(config.plz_csv_file)

def my_jsonify(data):
    content = json.dumps(data)
    mimetype = 'application/json'
    if request.args.get('callback'):
        content = '{callback}({content});'.format( 
                callback = request.args.get('callback'),
                content = content
                )
        mimetype = 'application/javascript'
    return Response(content, mimetype=mimetype)

@app.route('/')
def hello_world():
    return jenv.get_template('index.html').render()

@app.route('/search')
def search():
#    return jsonify(data=locator.find(request.args.get('term','')))
    data  = locator.find(request.args.get('term',''))
    names = map(lambda x:x['ort'],data)
    return my_jsonify(names)


@app.route('/values')
def get_values():
    locations = locator.find(request.args.get('location',''))
    if len(locations) == 0:
        return ''

    e,n = locations[0]['coord']

    data = {}
    for img in maps.images:
        data.setdefault(img.substance,{})[img.year] = img.value(e,n)

    return my_jsonify(data)

if __name__ == '__main__':
    print 'open the following URL in your web browser:'
    app.debug= True
    app.run()
#    app.run(port=8888)
#    app.run(host='0.0.0.0')

