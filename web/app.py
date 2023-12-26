from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output')
def read_file():
    file_path = '/app/data/result/output.txt'
    try:
        with open(file_path, 'r') as file:
            return file.read(), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return str(e), 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
