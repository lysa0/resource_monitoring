from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to monitoring agent!"

@app.route('/cpu')
def cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return jsonify(cpu_percent=cpu_percent)

@app.route('/ram')
def ram_usage():
    memory = psutil.virtual_memory()
    ram_percent = memory.percent
    return jsonify(ram_percent=ram_percent)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=15000)
