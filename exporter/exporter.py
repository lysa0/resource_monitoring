from flask import Flask
import requests
from pymongo import MongoClient
import schedule
import time
from datetime import datetime
import os

app = Flask(__name__)
username = 'username'
password = 'password'  # Only for test
authenticationDatabase = 'monitoring'

# monitoring_hosts=["192.168.100.5", "192.168.100.6", "localhost"]
monitoring_hosts = str(os.getenv("MONITORING_HOSTS")).split()
# print(f'Hosts for exporting metrics: {monitoring_hosts}')

agent_port = "15000"

# jdbc connection for mongodb
uri = f"mongodb://{username}:{password}@localhost:27017/?authSource={authenticationDatabase}"

client = MongoClient(uri)

# check connection and list db names
# print(client.list_database_names())

db = client['monitoring']


def collect_data(monitoring_host):
    print(monitoring_host)
    collection = db[f'metrics_{monitoring_host.replace(".", "_")}']
    monitoring_app_url = f'http://{monitoring_host}:{agent_port}'
    ram_response = requests.get(f'{monitoring_app_url}/ram')
    cpu_response = requests.get(f'{monitoring_app_url}/cpu')

    # write data to mongo db
    timestamp = datetime.utcnow()
    if ram_response.status_code == 200:
        ram_data = ram_response.json()
        collection.insert_one({'timestamp': timestamp, 'metric': 'ram_percent', 'value': ram_data['ram_percent']})

    if cpu_response.status_code == 200:
        cpu_data = cpu_response.json()
        collection.insert_one({'timestamp': timestamp, 'metric': 'cpu_percent', 'value': cpu_data['cpu_percent']})


def collect_all_data():
    for monitoring_host in monitoring_hosts:
        collect_data(monitoring_host)


@app.route('/')
def index():
    return "Welcome to metrics exporter!"


if __name__ == '__main__':
    # scheduler
    schedule.every(1).second.do(collect_all_data)

    # checking scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)
