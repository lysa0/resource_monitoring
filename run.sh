set -x
#set -e

source env.sh

bash db/rund.sh
bash utils/prepare.sh

for MONITORING_HOST in $MONITORING_HOSTS; do
  echo run agent on $MONITORING_HOST
  ssh $HOST_USER@$MONITORING_HOST "cd /tmp/agent; nohup bash run.sh > agent.log 2>&1 &"

  for i in {1..10}; do
    echo "Checking agent health $i..."
    curl $MONITORING_HOST:15000
    if [ $? -eq 0 ]; then break; fi
    sleep 5s
  done
done

(
  cd $WORK_DIR/exporter
  nohup bash run.sh >exporter.log 2>&1 &
)
(
  cd $WORK_DIR/client
  nohup bash run.sh >client.log 2>&1 &
)

for i in {1..10}; do
  echo "Checking dashboard health $i..."
  curl localhost:15001
  if [ $? -eq 0 ]; then break; fi
  sleep 3s
done

echo "http://localhost:15001/plot"
