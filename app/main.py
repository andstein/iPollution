import os,os.path
import json
import time
import StringIO

from flask import Flask,request,jsonify,Response,render_template,redirect,url_for
from jinja2 import Template,FileSystemLoader,Environment

import config,plz,maps

app = Flask(__name__)

t0= time.time()
locator= plz.locateCH(config.plz_csv_file)
print 'loaded PLZ database in {ms} ms'.format( ms = int(1000 * (time.time()-t0)) )

t0= time.time()
images= []
for fname in os.listdir(config.images_dir):
    if maps.fname_re.match(fname):
        images.append( maps.mapImage(os.path.join(config.images_dir,fname)) )
print 'loaded {n} images in {ms} ms'.format( n = len(images), ms = int(1000 * (time.time()-t0)) )


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
    return render_template('index.html')



@app.route('/search')
def search():
#    return jsonify(data=locator.find(request.args.get('term','')))
    data  = locator.find(request.args.get('term',''))
    names = map(lambda x:x['ort'],data)
    return my_jsonify(names)


def coordinates_from_params():

    if 'location' in request.args:

        location= request.args.get('location')
        xs = locator.find(location)
        if len(xs) == 0:
            raise KeyError('location {0} not found in database'.format(location))

        return xs[0]['coord']

    elif 'plz' in request.args:

        plz= request.args.get('plz')
        x = locator.by_plz(plz)
        if x == None:
            raise KeyError('plz {0} not found in database'.format(plz))
        return x['coord']

    elif 'coord' in request.args:

        return map(int,request.args.get('coord').split(','))

    else:

        raise KeyError('must specify location/plz/coord')


@app.route('/values')
def get_values():

    e,n = None,None
    try:
        e,n= coordinates_from_params()
    except KeyError,e:
        return my_jsonify('error : ' + str(e))

    data = {}
    for img in images:
        try:
            data.setdefault(img.substance,{})[img.year] = img.value(e,n)
        except maps.MapException,x:
            data.setdefault('errors',[]).append('could not calculate {substance} in year {year} : {msg}'.format(
                substance = img.substance,
                year = img.year,
                msg = str(x)
                ))

    return my_jsonify(data)


@app.route('/dump')
def dump_image():

    e,n = None,None
    try:
        e,n= coordinates_from_params()
    except KeyError,e:
        return redirect(url_for('static',filename='img/invalid.png'))

    for img in images:
        if img.substance == request.args.get('substance') and \
            str(img.year) == request.args.get('year'):

            fileobj = StringIO.StringIO()
            img.dump(e,n,fileobj)
            content = fileobj.getvalue()
            fileobj.close()

            return Response( response=content, mimetype='image/png' )

########        print img.substance + '--' + str(img.year)

    return redirect(url_for('static',filename='img/not_found.png'))


if __name__ == '__main__':
    print 'open the following URL in your web browser:'
    app.debug= True
    app.run( port=os.environ.get('PORT',5000) )
#    app.run(port=8888)
#    app.run(host='0.0.0.0')

