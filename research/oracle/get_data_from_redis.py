# api + redis persistent
import redis

if __name__ == "__main__":
    conn = redis.Redis('localhost')
    # for i in conn.keys():
    #     print(i)
    #     print(conn.get(i)) 
        
    # get the last one
    last_time = list(conn.keys())[-1] 
    last_orderbook = conn.get(last_time)

