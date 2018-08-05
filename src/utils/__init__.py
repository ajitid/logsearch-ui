import redis as redis_py
from .helpers import serialize

redis = redis_py.StrictRedis(host='localhost', port=6379, db=0)
redis.set('log_servers', serialize(set()))
