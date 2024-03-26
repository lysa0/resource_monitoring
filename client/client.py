from flask import Flask, render_template
from pymongo import MongoClient
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)
username = 'username'
password = 'password'  # Only for test
authenticationDatabase = 'monitoring'

# monitoring_hosts=["192.168.100.5", "192.168.100.6", "localhost"]
monitoring_hosts = str(os.getenv("MONITORING_HOSTS")).split()
# print(f'Hosts for exporting metrics: {monitoring_hosts}')

# jdbc connection for mongodb
uri = f"mongodb://{username}:{password}@localhost:27017/?authSource={authenticationDatabase}"

client = MongoClient(uri)
db = client['monitoring']


@app.route('/')
def index():
    return "Welcome to monitoring dashboard!"


@app.route('/plot')
def plot():
    cpu_plot_url = {}
    ram_plot_url = {}
    for monitoring_host in monitoring_hosts:
        collection = db[f'metrics_{monitoring_host.replace(".", "_")}']
        cpu_data = collection.find({'metric': 'cpu_percent'})
        ram_data = collection.find({'metric': 'ram_percent'})

        # Creating data for plots
        # print(ram_data)
        cpu_values = [data['value'] for data in cpu_data]
        # print(cpu_values)
        ram_values = [data['value'] for data in ram_data]
        print(ram_values)

        # Creating plot for CPU and export to .png for j2 template
        plt.figure(figsize=(8, 3))
        plt.plot(cpu_values, label='CPU Usage (%)', color='blue')
        plt.xlabel('Time')
        plt.ylabel('Usage (%)')
        plt.title('CPU Usage Over Time')
        plt.legend()
        cpu_img = BytesIO()
        plt.savefig(cpu_img, format='png')
        cpu_img.seek(0)
        cpu_plot_url[monitoring_host] = base64.b64encode(cpu_img.getvalue()).decode()

        # Creating plot for RAM and export to .png for j2 template
        plt.figure(figsize=(8, 3))
        plt.plot(ram_values, label='RAM Usage (%)', color='green')
        plt.xlabel('Time')
        plt.ylabel('Usage (%)')
        plt.title('RAM Usage Over Time')
        plt.legend()
        ram_img = BytesIO()
        plt.savefig(ram_img, format='png')
        ram_img.seek(0)
        ram_plot_url[monitoring_host] = base64.b64encode(ram_img.getvalue()).decode()

    return render_template('plot.html.j2', monitoring_hosts=monitoring_hosts, cpu_plot_url=cpu_plot_url,
                           ram_plot_url=ram_plot_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=15001)
