start_node() {
  local port=$1
  hz start -c config.xml -p $port &
  local pid=$!
  echo "Started node on port $port with PID: $pid"
}

case "$1" in
  -s|--start)
    echo "Starting Hazelcast nodes..."

    start_node 5701
    start_node 5702
    start_node 5703

    echo "Hazelcast nodes started."
    ;;
  -k|--kill)
    echo "Killing Hazelcast nodes..."

    pkill -f 'hazelcast'

    echo "Hazelcast nodes killed."
    ;;
  *)
    echo "Usage: $0 -s|--start | -k|--kill"
    exit 1
    ;;
esac