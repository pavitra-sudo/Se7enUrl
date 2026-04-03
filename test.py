

redis_client.set("test_key", "hello")
value = redis_client.get("test_key")

print(value)