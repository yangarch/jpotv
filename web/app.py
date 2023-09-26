from flask import Flask, render_template
import time

app = Flask(__name__)

#cache variable
cache_content = None
cache_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output')
def read_file():
    global cache_content
    global cache_time

    current_time = time.time()
    if current_time - cache_time > 3600:

        file_path = '../result/output.txt'
        try:
            with open(file_path, 'r') as file:
                return file.read(), 200, {'Content-Type': 'text/plain'}
        except Exception as e:
            return str(e), 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
