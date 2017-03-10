# -*- coding: utf-8 -*-
import redis
import json

if __name__ == "__main__":
    import settings

if __name__ == "__main__":
    proxy_list = open(settings.REDIS_PROXY_LIST_KEY, 'w')
    proxy_valid_list = open(settings.REDIS_PROXY_VALID_LIST_KEY, 'w')
    r = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT)
    for proxy in r.smembers(settings.REDIS_PROXY_LIST_KEY):
        _json = json.loads(proxy)
        proxy_list.write('http://{0}:{1}\n'.
            format(_json['ipAddress'], _json['port']))
    for proxy in r.zrange(settings.REDIS_PROXY_VALID_LIST_KEY, 0, -1):
        _json = json.loads(proxy)
        proxy_valid_list.write('http://{0}:{1}\n'.
            format(_json['ipAddress'], _json['port']))
