import redis
conn = redis.Redis('localhost')

user1 = {"Croatia": "Zagreb", "Bahamas": "Nassau"}
conn.mset(user1)
print(conn.get("Bahamas"))
print(conn.keys())
#hgetall("localhost:56854717")

# print(user1)
# conn.hset("pythonDict", str(user1))

# #conn.hset("pythonDict", bytes(str(user2).encode()))

# conn.hgetall("pythonDict")