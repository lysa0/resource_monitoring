echo rsync on $1
rsync -r $WORK_DIR/agent $HOST_USER@$1:/tmp
