from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask successfully installed!'

if __name__ == '__main__':
    print 'open the following URL in your web browser:'
    app.run()

