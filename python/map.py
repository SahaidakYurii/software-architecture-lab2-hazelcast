import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    map = client.get_map("distribMap").blocking()

    for i in range(1000):
        map.put(i, i)

    print("successfully inserted data")

    client.shutdown()
