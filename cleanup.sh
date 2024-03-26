set -x
#set -e

source env.sh

docker stop resource_monitoring_db
#docker exec resource_monitoring_db "rm -f /data/db/*"
docker rm resource_monitoring_db
sudo rm -rf /tmp/resource_monitoring
for MONITORING_HOST in $MONITORING_HOSTS; do
  ssh $HOST_USER@$MONITORING_HOST "pkill -f agent.py || rm -r /tmp/agent"
  echo $MONITORING_HOST
done
pkill -f agent.py
pkill -f exporter.py
pkill -f client.py
#rm -r $WORK_DIR/agent/agent
rm -r $WORK_DIR/exporter/exporter
rm -r $WORK_DIR/client/client
