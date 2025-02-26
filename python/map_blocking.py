import argparse
import hazelcast
import threading
import time

def increment_pessimistic(client):
    map = client.get_map("map").blocking()

    for _ in range(10000):
        map.lock("value")
        try:
            temp = map.get("value")
            temp += 1
            map.put("value", temp)
        finally:
            map.unlock("value")

    client.shutdown()

def increment_optimistic(client):
    map = client.get_map("map").blocking()

    for _ in range(10000):
        old = map.get("value")
        while not map.replace_if_same("value", old, old+1):
            old = map.get("value")

    client.shutdown()

def increment_noblocking(client):
    map = client.get_map("map").blocking()

    for _ in range(10000):
        temp = map.get("value")
        temp += 1
        map.put("value", temp)

    client.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hazelcast Increment Example")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', '--none', action='store_true', help='No locking')
    group.add_argument('-o', '--optimistic', action='store_true', help='Optimistic locking')
    group.add_argument('-p', '--pessimistic', action='store_true', help='Pessimistic locking')

    args = parser.parse_args()

    client = hazelcast.HazelcastClient()
    map = client.get_map("map").blocking()
    map.put_if_absent("value", 0)

    threads=[]
    for _ in range(3):
        temp_client = hazelcast.HazelcastClient()
        thread = threading.Thread(target=(increment_pessimistic if args.pessimistic else
                                          increment_optimistic if args.optimistic else
                                          increment_noblocking),
                                  args=(temp_client,))
        threads.append(thread)

    st_time = time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()

    final_value = map.get("value")
    print(f"The value: {final_value}\nTime: {end_time-st_time}")
    map.put("value", 0)

    client.shutdown()