import hazelcast
import threading
import argparse

def producer(client, i):
    queue = client.get_queue("queue").blocking()

    for val in range(1, 101):
        queue.put(val)
        print(f"Producer {i} wrote: {val}")

    queue.put(-1)
    client.shutdown()

def consumer(client, i):
    queue = client.get_queue("queue").blocking()
    vals = []

    val = queue.take()
    while val != -1:
        vals.append(val)
        val = queue.take()


    print(f"Consumer {i} read\n\t{vals}")

    queue.put(-1)
    client.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hazelcast Increment Example")

    parser.add_argument('-c', '--consumers', type=int, default=2, help='Number of consumers')
    parser.add_argument('-p', '--producers', type=int, default=1, help='Number of producers')

    args = parser.parse_args()

    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()

    threads = [threading.Thread(target=consumer, args=(hazelcast.HazelcastClient(),i,)) for i in range(args.consumers)] + \
              [threading.Thread(target=producer, args=(hazelcast.HazelcastClient(),i,)) for i in range(args.producers)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    queue.destroy()
    client.shutdown()