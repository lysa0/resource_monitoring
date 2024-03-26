docker run -d \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=rootPassXXX \
  -v /tmp/resource_monitoring:/data/db \
  --name resource_monitoring_db \
  -p 27017:27017 \
  mongo:7.0.7
