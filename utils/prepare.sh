echo $MOTITORING_HOSTS

# Create user for monitoring
for i in {1..5}; do
  echo "Trying $i to create user in DB..."
  docker exec resource_monitoring_db mongosh --username root --password rootPassXXX --authenticationDatabase=admin monitoring --eval "$(cat $WORK_DIR/utils/create_user.js)"
  if [ $? -eq 0 ]; then break; fi
  sleep 2s
done
# Copy agent app for every host
for MONITORING_HOST in $MONITORING_HOSTS; do
  echo $MONITORING_HOST
  bash $WORK_DIR/utils/rsync.sh $MONITORING_HOST
done
