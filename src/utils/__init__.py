import redis as redis_py
from .helpers import serialize

redis = redis_py.StrictRedis(host='localhost', port=6379, db=0)
redis.set('log_servers', serialize(set()))
redis_uid_results_expiry_time_in_seconds = 172800  # == 2 days
